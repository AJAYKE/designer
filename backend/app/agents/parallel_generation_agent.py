import asyncio
from typing import List, Dict, Any, AsyncGenerator
from langchain_core.runnables import RunnableConfig
from langgraph.store.base import BaseStore
from datetime import datetime
import time

from app.models.conversation_state import ConversationState, ConversationPhase
from app.models.design_state import GeneratedScreen, ScreenType, DesignMetadata
from app.services.multi_model_llm_service import MultiModelLLMService
from app.services.s3_service import S3Service
from app.services.code_parser import CodeParser
from app.services.image_processor import ImageProcessor

async def parallel_generation_agent(
    state: ConversationState,
    config: RunnableConfig,
    *,
    store: BaseStore,
) -> ConversationState:
    """
    Generate all approved screens in parallel with shared context and progress tracking
    """
    
    print(f"🚀 Parallel Generation Agent: Starting parallel generation for {state['thread_id']}")
    
    try:
        user_id = config["configurable"]["user_id"]
        design_plan = state.get("design_plan", {})
        screens = design_plan.get("screens", [])
        selected_model = state.get("selected_model", "openai:gpt-4")
        
        if not screens:
            raise ValueError("No screens to generate")
        
        # Extract shared context for consistent generation
        shared_context = await _extract_shared_context(state, user_id, store)
        
        # Initialize progress tracking
        progress_tracker = {
            "total_screens": len(screens),
            "completed_screens": 0,
            "failed_screens": 0,
            "current_operations": {},
            "start_time": time.time()
        }
        
        # Generate all screens in parallel
        generated_screens = []
        async for progress_update in _generate_screens_parallel(
            screens, 
            shared_context, 
            selected_model, 
            state, 
            user_id,
            store
        ):
            # Update progress and yield intermediate state
            if progress_update["type"] == "screen_complete":
                generated_screens.append(progress_update["screen"])
                progress_tracker["completed_screens"] += 1
            elif progress_update["type"] == "screen_failed":
                progress_tracker["failed_screens"] += 1
            
            # Update conversation state with progress
            current_progress = (progress_tracker["completed_screens"] / progress_tracker["total_screens"]) * 100
            
            updated_state = {
                **state,
                "phase": ConversationPhase.GENERATING,
                "generation_progress": {
                    **progress_tracker,
                    "overall_progress": current_progress,
                    "generated_screens": generated_screens
                },
                "generated_screens": generated_screens,
                "updated_at": datetime.utcnow().isoformat()
            }
            
            # Yield progress update (for streaming)
            yield updated_state
        
        # Final completion state
        total_time = time.time() - progress_tracker["start_time"]
        
        final_state = {
            **state,
            "phase": ConversationPhase.COMPLETE,
            "generated_screens": generated_screens,
            "generation_progress": {
                **progress_tracker,
                "overall_progress": 100,
                "total_generation_time_ms": int(total_time * 1000),
                "average_screen_time_ms": int((total_time * 1000) / len(screens)) if screens else 0
            },
            "updated_at": datetime.utcnow().isoformat()
        }
        
        # Store completion context
        namespace = ("completions", user_id)
        await store.aput(
            namespace,
            f"parallel_generation_{state['thread_id']}",
            {
                "data": f"Completed parallel generation of {len(generated_screens)} screens",
                "screens": [s.screen_id for s in generated_screens],
                "total_time_ms": int(total_time * 1000),
                "model_used": selected_model,
                "timestamp": datetime.utcnow().isoformat()
            }
        )
        
        yield final_state
        
    except Exception as e:
        print(f"❌ Parallel Generation Error: {str(e)}")
        yield {
            **state,
            "phase": ConversationPhase.ERROR,
            "error_message": f"Parallel generation failed: {str(e)}",
            "updated_at": datetime.utcnow().isoformat()
        }


async def _generate_screens_parallel(
    screens: List[Dict[str, Any]],
    shared_context: Dict[str, Any],
    model: str,
    state: ConversationState,
    user_id: str,
    store: BaseStore
) -> AsyncGenerator[Dict[str, Any], None]:
    """Generate all screens simultaneously with progress updates"""
    
    # Create semaphore to limit concurrent generations (prevent overwhelming)
    semaphore = asyncio.Semaphore(3)  # Max 3 concurrent generations
    
    # Create individual generation tasks
    generation_tasks = []
    for screen_config in screens:
        task = asyncio.create_task(
            _generate_individual_screen_with_semaphore(
                semaphore,
                screen_config,
                shared_context,
                model,
                state,
                user_id,
                store
            )
        )
        generation_tasks.append(task)
    
    # Process completed screens as they finish
    completed_count = 0
    async for completed_task in asyncio.as_completed(generation_tasks):
        try:
            result = await completed_task
            completed_count += 1
            
            if result["success"]:
                yield {
                    "type": "screen_complete",
                    "screen": result["screen"],
                    "progress": completed_count / len(screens) * 100
                }
            else:
                yield {
                    "type": "screen_failed", 
                    "error": result["error"],
                    "screen_id": result.get("screen_id"),
                    "progress": completed_count / len(screens) * 100
                }
                
        except Exception as e:
            completed_count += 1
            yield {
                "type": "screen_failed",
                "error": str(e),
                "progress": completed_count / len(screens) * 100
            }


async def _generate_individual_screen_with_semaphore(
    semaphore: asyncio.Semaphore,
    screen_config: Dict[str, Any],
    shared_context: Dict[str, Any],
    model: str,
    state: ConversationState,
    user_id: str,
    store: BaseStore
) -> Dict[str, Any]:
    """Generate a single screen with semaphore control"""
    
    async with semaphore:
        return await _generate_individual_screen(
            screen_config,
            shared_context,
            model,
            state,
            user_id,
            store
        )


async def _generate_individual_screen(
    screen_config: Dict[str, Any],
    shared_context: Dict[str, Any],
    model: str,
    state: ConversationState,
    user_id: str,
    store: BaseStore
) -> Dict[str, Any]:
    """Generate a single screen with full processing pipeline"""
    
    start_time = time.time()
    screen_id = screen_config.get("screen_id", f"screen_{int(time.time())}")
    
    try:
        # Create screen metadata
        screen_metadata = DesignMetadata(
            screen_id=screen_id,
            screen_type=ScreenType(screen_config["screen_type"]),
            title=screen_config["title"],
            description=screen_config["description"],
            estimated_tokens=screen_config.get("estimated_tokens", 2000),
            generation_order=screen_config.get("generation_order", 1)
        )
        
        # Create generation prompt with shared context
        generation_prompt = await _create_contextualized_prompt(
            screen_metadata,
            shared_context,
            state.get("prompt_config", {}),
            user_id,
            store
        )
        
        # Generate code using selected model
        llm_service = MultiModelLLMService()
        generated_code = await llm_service.generate_screen_code(
            generation_prompt,
            screen_metadata.screen_type,
            model
        )
        
        # Parse generated code
        code_parser = CodeParser()
        parsed_code = code_parser.parse_generated_code(generated_code)
        
        # Process images if needed
        images = []
        if parsed_code.get("html"):
            image_processor = ImageProcessor()
            image_requirements = image_processor.extract_image_requirements(parsed_code["html"])
            
            if image_requirements:
                # Limit to 3 images per screen to prevent slowdown
                for req in image_requirements[:3]:
                    try:
                        # This could be made parallel too
                        from app.services.unsplash_service import UnsplashService
                        unsplash = UnsplashService()
                        img_results = await unsplash.search_images(req["query"], count=1)
                        images.extend([img.dict() for img in img_results])
                    except:
                        continue
                
                # Inject images into HTML
                parsed_code["html"] = image_processor.inject_images(parsed_code["html"], images)
        
        generation_time = int((time.time() - start_time) * 1000)
        
        # Create generated screen object
        generated_screen = GeneratedScreen(
            screen_id=screen_id,
            metadata=screen_metadata,
            html_code=parsed_code.get("html", ""),
            css_classes=parsed_code.get("css", ""),
            javascript=parsed_code.get("js", ""),
            images=images,
            generation_time_ms=generation_time,
            token_usage=len(generated_code.split()) * 1.3  # Rough estimate
        )
        
        # Store in S3 (this could also be made parallel)
        s3_service = S3Service()
        s3_url = await s3_service.store_generated_screen(
            thread_id=state["thread_id"],
            message_id=state.get("message_id", "parallel_gen"),
            screen=generated_screen
        )
        generated_screen.s3_url = s3_url
        
        # Store generation context
        namespace = ("parallel_generations", user_id)
        await store.aput(
            namespace,
            f"screen_{screen_id}",
            {
                "data": f"Generated {screen_metadata.screen_type} screen in parallel",
                "generation_time_ms": generation_time,
                "model_used": model,
                "timestamp": datetime.utcnow().isoformat()
            }
        )
        
        return {
            "success": True,
            "screen": generated_screen,
            "generation_time_ms": generation_time
        }
        
    except Exception as e:
        print(f"❌ Individual Screen Generation Error ({screen_id}): {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "screen_id": screen_id
        }


async def _extract_shared_context(
    state: ConversationState,
    user_id: str,
    store: BaseStore
) -> Dict[str, Any]:
    """Extract shared context for consistent generation across all screens"""
    
    # Get user's design preferences and history
    namespace = ("user_context", user_id)
    user_preferences = await store.asearch(namespace, query="design preferences", limit=10)
    
    # Extract prompt configuration
    prompt_config = state.get("prompt_config", {})
    design_plan = state.get("design_plan", {})
    
    # Build shared context
    shared_context = {
        "user_requirements": state.get("design_requirements", ""),
        "design_strategy": design_plan.get("generation_strategy", ""),
        "user_context": design_plan.get("user_context", ""),
        
        # Style consistency
        "theme": prompt_config.get("style", {}).get("theme", "light"),
        "accent_color": prompt_config.get("style", {}).get("accent_color", "blue"),
        "style_approach": prompt_config.get("style", {}).get("style", "minimalist"),
        
        # Typography consistency
        "heading_font": prompt_config.get("typography", {}).get("heading_font", "inter"),
        "body_font": prompt_config.get("typography", {}).get("body_font", "inter"),
        "font_scale": prompt_config.get("typography", {}).get("heading_size", "32-40px"),
        
        # Platform and responsive approach
        "platform": prompt_config.get("platform", "web"),
        "responsive_strategy": "mobile-first",
        
        # User preferences from history
        "user_preferences": [p.value.get("data", "") for p in user_preferences],
        
        # Brand and content context
        "brand_context": prompt_config.get("brand_context", ""),
        "content_context": prompt_config.get("content_context", "")
    }
    
    return shared_context


async def _create_contextualized_prompt(
    screen_metadata: DesignMetadata,
    shared_context: Dict[str, Any],
    prompt_config: Dict[str, Any],
    user_id: str,
    store: BaseStore
) -> str:
    """Create a detailed prompt for screen generation with shared context"""
    
    prompt = f"""
# Parallel Screen Generation Task

You are generating the **{screen_metadata.screen_type.value}** screen as part of a multi-screen application. This screen is being generated alongside other screens, so consistency is critical.

## Screen Details
- **Type**: {screen_metadata.screen_type.value}
- **Title**: {screen_metadata.title}
- **Description**: {screen_metadata.description}

## Shared Design Context (CRITICAL - Maintain Consistency)
- **User Requirements**: {shared_context.get('user_requirements', 'Not specified')}
- **Design Strategy**: {shared_context.get('design_strategy', 'Standard approach')}
- **Theme**: {shared_context.get('theme', 'light')} mode
- **Accent Color**: {shared_context.get('accent_color', 'blue')}
- **Visual Style**: {shared_context.get('style_approach', 'minimalist')}
- **Typography**: {shared_context.get('heading_font', 'inter')} headings, {shared_context.get('body_font', 'inter')} body
- **Platform**: {shared_context.get('platform', 'web')}

## Consistency Requirements

1. **Color Palette**: Use the {shared_context.get('accent_color', 'blue')} accent consistently
2. **Typography**: Maintain font hierarchy with {shared_context.get('heading_font', 'inter')}
3. **Component Style**: Follow {shared_context.get('style_approach', 'minimalist')} design principles
4. **Responsive Approach**: Mobile-first design
5. **Navigation**: Ensure this screen fits within the overall app navigation

## Technical Requirements

Generate production-ready code with:
- **Semantic HTML5** with proper landmarks and accessibility
- **Tailwind CSS utilities only** (no external frameworks)
- **Vanilla JavaScript** for interactions
- **WCAG 2.1 AA compliance**
- **Consistent naming conventions** across screens

## Response Format

```html
[Complete HTML structure for the {screen_metadata.screen_type.value} screen]
```

```css
[Custom CSS only if absolutely necessary]
```

```javascript
[JavaScript for interactions if needed]
```

Focus on creating a cohesive {screen_metadata.screen_type.value} screen that seamlessly integrates with the overall application design.
"""
    
    return prompt.strip()
