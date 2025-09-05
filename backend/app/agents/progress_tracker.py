from langchain_core.runnables import RunnableConfig
from langgraph.store.base import BaseStore
from app.models.design_state import DesignState, GenerationPhase
from datetime import datetime

async def progress_tracking_agent(
    state: DesignState,
    config: RunnableConfig,
    *,
    store: BaseStore,
) -> DesignState:
    """
    Track progress and handle completion/error states
    """
    print(f"📊 Progress Tracker: Phase {state['phase']}, Progress {state['overall_progress']}%")
    
    try:
        user_id = config["configurable"]["user_id"]
        
        # Update final state based on current phase
        if state["phase"] == GenerationPhase.PLAN_REVIEW:
            # Plan is ready for user review
            return {
                **state,
                "overall_progress": 25,
                "current_screen_progress": 0,
                "updated_at": datetime.utcnow().isoformat()
            }
        
        elif state["phase"] == GenerationPhase.COMPLETE:
            # All screens generated successfully
            namespace = ("completions", user_id)
            await store.aput(
                namespace,
                f"project_{state['thread_id']}",
                {
                    "data": f"Completed project with {len(state['generated_screens'])} screens",
                    "total_tokens": state["total_tokens_used"],
                    "screens": [s.screen_id for s in state["generated_screens"]],
                    "timestamp": datetime.utcnow().isoformat()
                }
            )
            
            return {
                **state,
                "overall_progress": 100,
                "current_screen_progress": 100,
                "updated_at": datetime.utcnow().isoformat()
            }
        
        elif state["phase"] == GenerationPhase.ERROR:
            # Handle error state
            namespace = ("errors", user_id)
            await store.aput(
                namespace,
                f"error_{state['thread_id']}_{datetime.utcnow().isoformat()}",
                {
                    "data": f"Generation failed: {state['error_message']}",
                    "phase": state["phase"],
                    "progress": state["overall_progress"],
                    "timestamp": datetime.utcnow().isoformat()
                }
            )
            
            return {
                **state,
                "updated_at": datetime.utcnow().isoformat()
            }
        
        else:
            # Default progress update
            return {
                **state,
                "updated_at": datetime.utcnow().isoformat()
            }
            
    except Exception as e:
        print(f"❌ Progress Tracking Error: {str(e)}")
        return {
            **state,
            "phase": GenerationPhase.ERROR,
            "error_message": f"Progress tracking failed: {str(e)}",
            "updated_at": datetime.utcnow().isoformat()
        }