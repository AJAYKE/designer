from typing import Dict, Any
from app.models.design_state import DesignState, DesignPlan, DesignMetadata, ScreenType, GenerationPhase
from app.services.token_estimator import TokenEstimator
from app.services.llm_service import LLMService
from datetime import datetime
from uuid import uuid4
import json

async def planning_agent(state: DesignState) -> DesignState:
    """
    Planning agent - that creates detailed plans for multiple screens
    """
    print(f"Planning Agent: Processing for user {state['configurable'].get('user_id')}")
    
    try:
        user_id = state["configurable"]["user_id"]
        thread_id = state["thread_id"]
        
        # Get user context from store (previous designs, preferences)
        namespace = ("user_context", user_id)
        user_memories = await store.asearch(namespace, query="design preferences")
        user_context = "\n".join([d.value["data"] for d in user_memories])
        
        # Extract configuration
        config_data = state["prompt_config"]
        
        # Create comprehensive planning prompt
        planning_prompt = await _create_planning_prompt(config_data, user_context)
        
        # Generate plan using LLM
        llm_service = LLMService()
        plan_response = await llm_service.generate_plan(planning_prompt)
        
        # Parse plan response into structured format
        design_plan = await _parse_plan_response(plan_response, config_data)
        
        # Estimate tokens for each screen
        token_estimator = TokenEstimator()
        for screen_metadata in design_plan.screens:
            screen_metadata.estimated_tokens = token_estimator.estimate_screen_tokens(
                screen_metadata.screen_type,
                config_data
            )
        
        design_plan.total_estimated_tokens = sum(s.estimated_tokens for s in design_plan.screens)
        
        # Store plan context for future reference
        await store.aput(
            namespace,
            f"plan_{design_plan.plan_id}",
            {
                "data": f"Created design plan with {len(design_plan.screens)} screens",
                "plan_summary": design_plan.generation_strategy,
                "timestamp": datetime.utcnow().isoformat()
            }
        )
        
        return {
            **state,
            "design_plan": design_plan,
            "phase": GenerationPhase.PLAN_REVIEW,
            "overall_progress": 20,
            "estimated_tokens_remaining": design_plan.total_estimated_tokens,
            "updated_at": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        print(f"❌ Enhanced Planning Agent Error: {str(e)}")
        return {
            **state,
            "phase": GenerationPhase.ERROR,
            "error_message": f"Planning failed: {str(e)}",
            "overall_progress": 0,
            "updated_at": datetime.utcnow().isoformat()
        }

async def _create_planning_prompt(config: Dict[str, Any], user_context: str) -> str:
    """Create a comprehensive planning prompt"""
    
    platform = config.get("platform", "web")
    layout = config.get("layout", {})
    sections = config.get("sections", [])
    
    prompt = f"""
# Design Planning Task

Create a comprehensive plan for a {platform} application with multiple screens/pages.

## User Context
{user_context if user_context else "New user - no previous design history"}

## Configuration
Platform: {platform}
Layout Type: {layout.get('type', 'hero')}
Sections Required: {sections}
Theme: {config.get('style', {}).get('theme', 'light')}

## Planning Requirements

You must create a detailed plan that includes:

1. **Screen Architecture**: Determine what screens/pages are needed
2. **User Flow**: How users navigate between screens
3. **Content Strategy**: What content goes on each screen
4. **Technical Approach**: Responsive design strategy
5. **Generation Order**: Optimal order for screen generation

## Response Format

Provide your response as a JSON object with this exact structure:

```json
{{
  "screens": [
    {{
      "screen_type": "landing|dashboard|login|profile|settings|mobile_app",
      "title": "Screen Title",
      "description": "Detailed description of this screen's purpose",
      "generation_order": 1
    }}
  ],
  "generation_strategy": "Brief explanation of the approach",
  "user_context": "Summary of user needs and requirements"
}}
```

Create a plan for 2-5 screens maximum. Focus on the most essential screens for the user's requirements.
"""
    
    return prompt.strip()

async def _parse_plan_response(response: str, config: Dict[str, Any]) -> DesignPlan:
    """Parse LLM response into structured DesignPlan"""
    
    try:
        # Extract JSON from response
        json_start = response.find('{')
        json_end = response.rfind('}') + 1
        json_str = response[json_start:json_end]
        
        plan_data = json.loads(json_str)
        
        # Create screen metadata objects
        screens = []
        for screen_data in plan_data["screens"]:
            screen_metadata = DesignMetadata(
                screen_id=str(uuid4()),
                screen_type=ScreenType(screen_data["screen_type"]),
                title=screen_data["title"],
                description=screen_data["description"],
                estimated_tokens=0,  # Will be calculated later
                generation_order=screen_data.get("generation_order", len(screens) + 1)
            )
            screens.append(screen_metadata)
        
        # Sort screens by generation order
        screens.sort(key=lambda x: x.generation_order)
        
        # Create design plan
        design_plan = DesignPlan(
            plan_id=str(uuid4()),
            screens=screens,
            total_estimated_tokens=0,  # Will be calculated later
            generation_strategy=plan_data.get("generation_strategy", "Sequential generation"),
            user_context=plan_data.get("user_context", "Standard requirements"),
            created_at=datetime.utcnow()
        )
        
        return design_plan
        
    except Exception as e:
        print(f"⚠️ Plan parsing error: {e}")
        # Fallback to single landing screen
        return DesignPlan(
            plan_id=str(uuid4()),
            screens=[
                DesignMetadata(
                    screen_id=str(uuid4()),
                    screen_type=ScreenType.LANDING,
                    title="Landing Page",
                    description="Main landing page for the application",
                    estimated_tokens=2000,
                    generation_order=1
                )
            ],
            total_estimated_tokens=2000,
            generation_strategy="Single screen fallback",
            user_context="Fallback plan due to parsing error",
            created_at=datetime.utcnow()
        )