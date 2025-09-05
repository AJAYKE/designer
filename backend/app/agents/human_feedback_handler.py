from langgraph.graph.graph import RunnableConfig
from langgraph.store.base import BaseStore
from app.models.conversation_state import ConversationState


async def human_feedback_handler(
    state: ConversationState,
    config: RunnableConfig,
    *,
    store: BaseStore,
) -> ConversationState:
    """
    Handle human feedback and approval - this is where interruption occurs
    """
    
    print(f"👤 Human Feedback Handler: Waiting for user response on {state['thread_id']}")
    
    feedback = state.get("human_feedback", {})
    action = feedback.get("action", "pending")
    
    if action == "approved":
        print("✅ Plan approved by user - proceeding to generation")
        return {
            **state,
            "phase": ConversationPhase.GENERATING,
            "plan_approved": True,
            "updated_at": datetime.utcnow().isoformat()
        }
    
    elif action == "edit_plan":
        print("📝 User requested plan modifications")
        return {
            **state,
            "phase": ConversationPhase.PLANNING,
            "plan_modifications": feedback.get("modifications", []),
            "updated_at": datetime.utcnow().isoformat()
        }
    
    elif action == "cancel":
        print("❌ User canceled the design")
        return {
            **state,
            "phase": ConversationPhase.CANCELLED,
            "updated_at": datetime.utcnow().isoformat()
        }
    
    else:
        # Still waiting for feedback - this triggers the interruption
        return {
            **state,
            "phase": ConversationPhase.AWAITING_APPROVAL,
            "updated_at": datetime.utcnow().isoformat()
        }

