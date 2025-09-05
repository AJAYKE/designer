from langchain_core.runnables import RunnableConfig
from langgraph.store.base import BaseStore
from app.models.design_state import DesignState, GeneratedScreen, GenerationPhase
from app.services.s3_service import S3Service
from app.services.token_tracker import TokenTracker
from datetime import datetime
import time
from app.services.code_parser import CodeParser
from app.services.llm_service import LLMService
from app.services.image_processor import ImageProcessor
from app.services.unsplash_service import UnsplashService

async def generation_agent(
    state: DesignState,
    config: RunnableConfig,
    *,
    store: BaseStore,
) -> DesignState:
    """
    Generate individual screens with streaming support and S3 storage
    """
    print(f"⚡ Screen Generator: Generating screen {state['current_screen_index'] + 1}")
    
    try:
        user_id = config["configurable"]["user_id"]
        current_index = state["current_screen_index"]
        design_plan = state["design_plan"]
        
        if current_index >= len(design_plan.screens):
            # All screens generated
            return {
                **state,
                "phase": GenerationPhase.COMPLETE,
                "overall_progress": 100,
                "current_screen_progress": 100,
                "updated_at": datetime.utcnow().isoformat()
            }
        
        current_screen_meta = design_plan.screens[current_index]
        
        # Initialize generation
        start_time = time.time()
        
        # Create generation prompt for this specific screen
        generation_prompt = await _create_screen_prompt(
            current_screen_meta,
            state["prompt_config"],
            user_id,
            store
        )
        
        # Generate code using enhanced LLM service with streaming
        llm_service = LLMService()
        generated_code = await llm_service.generate_screen_code(
            generation_prompt,
            current_screen_meta.screen_type
        )
        
        # Track token usage
        token_tracker = TokenTracker()
        tokens_used = await token_tracker.count_tokens(generated_code)
        
        # Parse generated code
        
        code_parser = CodeParser()
        parsed_code = code_parser.parse_generated_code(generated_code)
        
        # Process images if needed
        
        image_processor = ImageProcessor()
        images = []
        if parsed_code["html"]:
            image_requirements = image_processor.extract_image_requirements(parsed_code["html"])
            if image_requirements:
                
                unsplash = UnsplashService()
                for req in image_requirements[:3]:  # Limit images
                    try:
                        img_results = await unsplash.search_images(req["query"], count=1)
                        images.extend([img.dict() for img in img_results])
                    except:
                        continue
                
                # Inject images into HTML
                parsed_code["html"] = image_processor.inject_images(parsed_code["html"], images)
        
        generation_time = int((time.time() - start_time) * 1000)
        
        # Create generated screen object
        generated_screen = GeneratedScreen(
            screen_id=current_screen_meta.screen_id,
            metadata=current_screen_meta,
            html_code=parsed_code["html"],
            css_classes=parsed_code["css"],
            javascript=parsed_code["js"],
            images=images,
            generation_time_ms=generation_time,
            token_usage=tokens_used
        )
        
        # Store in S3
        s3_service = S3Service()
        s3_url = await s3_service.store_generated_screen(
            thread_id=state["thread_id"],
            message_id=state["message_id"],
            screen=generated_screen
        )
        generated_screen.s3_url = s3_url
        
        # Update state
        updated_screens = state["generated_screens"] + [generated_screen]
        next_index = current_index + 1
        
        # Calculate progress
        screen_progress = 100  # Current screen complete
        overall_progress = min(95, 20 + (next_index / len(design_plan.screens)) * 75)
        
        # Update token tracking
        total_tokens = state["total_tokens_used"] + tokens_used
        remaining_tokens = max(0, state["estimated_tokens_remaining"] - tokens_used)
        
        # Store generation context
        namespace = ("generations", user_id)
        await store.aput(
            namespace,
            f"screen_{generated_screen.screen_id}",
            {
                "data": f"Generated {current_screen_meta.screen_type} screen",
                "tokens_used": tokens_used,
                "generation_time_ms": generation_time,
                "timestamp": datetime.utcnow().isoformat()
            }
        )
        
        return {
            **state,
            "generated_screens": updated_screens,
            "current_screen_index": next_index,
            "phase": GenerationPhase.GENERATING if next_index < len(design_plan.screens) else GenerationPhase.COMPLETE,
            "overall_progress": int(overall_progress),
            "current_screen_progress": screen_progress,
            "total_tokens_used": total_tokens,
            "estimated_tokens_remaining": remaining_tokens,
            "updated_at": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        print(f"❌ Screen Generation Error: {str(e)}")
        return {
            **state,
            "phase": GenerationPhase.ERROR,
            "error_message": f"Screen generation failed: {str(e)}",
            "updated_at": datetime.utcnow().isoformat()
        }

async def _create_screen_prompt(
    screen_meta, 
    config: dict, 
    user_id: str, 
    store: BaseStore
) -> str:
    """Create detailed prompt for specific screen generation"""
    
    # Get user's design history for consistency
    namespace = ("generations", user_id)
    recent_generations = await store.asearch(namespace, limit=5)
    design_context = "\n".join([d.value["data"] for d in recent_generations])
    
    prompt = f"""
# Screen Generation Task

Generate a complete {screen_meta.screen_type.value} screen with the following specifications:

## Screen Details
- **Type**: {screen_meta.screen_type.value}
- **Title**: {screen_meta.title}
- **Description**: {screen_meta.description}

## Design Context
{design_context if design_context else "First screen in this project"}

## Configuration
- **Platform**: {config.get('platform', 'web')}
- **Theme**: {config.get('style', {}).get('theme', 'light')}
- **Accent Color**: {config.get('style', {}).get('accent_color', 'blue')}
- **Typography**: {config.get('typography', {}).get('heading_font', 'inter')}

## Output Requirements

Generate production-ready code with:

1. **Semantic HTML5** with proper landmarks
2. **Tailwind CSS utilities only** (no custom frameworks)
3. **Vanilla JavaScript** for interactions
4. **Mobile-first responsive design**
5. **Accessibility compliance** (WCAG 2.1 AA)

## Response Format

```html
[Complete HTML structure]
```

```css
[Custom CSS only if absolutely necessary]
```

```javascript
[JavaScript for interactions if needed]
```

Focus on creating a polished, professional {screen_meta.screen_type.value} that matches the design system and user expectations.
"""
    
    return prompt.strip()

