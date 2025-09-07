from datetime import datetime
from langchain_core.runnables import RunnableConfig
from langgraph.store.base import BaseStore
from app.models.conversation_state import ConversationState, ConversationPhase
import logging

logger = logging.getLogger(__name__)

def _summarize_plan(plan: dict) -> str:
    screens = plan.get("screens", []) or []
    n = len(screens)
    if n == 0:
        return "I'm ready to create your design. Please approve or let me know what changes you'd like."
    titles = [s.get("title", s.get("screen_type", "Untitled")) for s in screens[:3]]
    title_list = ", ".join(titles)
    if n > 3:
        title_list += f", and {n - 3} more"
    return f"I've planned {n} screen{'s' if n != 1 else ''}: {title_list}. Would you like me to proceed, or would you like any changes?"

async def feedback_gate(state: ConversationState, config: RunnableConfig, *, store: BaseStore) -> ConversationState:
    """
    Single source of truth for moving from AWAITING_APPROVAL to GENERATING/PLANNING/END.
    Also clears `human_feedback` after consuming it to avoid reprocessing.
    """
    human_feedback = state.get("human_feedback", {}) or {}
    action = human_feedback.get("action", "pending")
    logger.info(f"[feedback_gate] processing action={action}")

    # Consume actionable feedback
    if action in ("approved", "edit_plan", "cancel"):
        if action == "approved":
            new_state = {
                **state,
                "phase": ConversationPhase.GENERATING,
                "progress": max(40, state.get("progress", 0)),
                "last_response": "Great! I'll start generating your screens now.",
                "updated_at": datetime.utcnow().isoformat(),
            }
        elif action == "edit_plan":
            mods = human_feedback.get("modifications") or []
            new_state = {
                **state,
                "phase": ConversationPhase.PLANNING,
                "progress": 15,
                "last_response": "I'll revise the plan based on your feedback.",
        "updated_at": datetime.utcnow().isoformat(),
        "is_edit_cycle": True,                  # ← mark single-pass edit
        "edit_modifications": mods,             # ← pass the edits explicitly
    }
            # Important: CLEAR feedback so we don’t loop on the same edit
            new_state.pop("human_feedback", None)
            return new_state

        else:  # cancel
            new_state = {
                **state,
                "phase": ConversationPhase.CANCELLED,
                "progress": 0,
                "last_response": "Design process cancelled. Feel free to start a new request anytime!",
                "updated_at": datetime.utcnow().isoformat(),
            }

        # Important: clear human_feedback after consuming it
        new_state.pop("human_feedback", None)
        return new_state

    # No actionable feedback → remain in AWAITING_APPROVAL and summarize the plan
    plan = state.get("design_plan", {}) or {}
    response = _summarize_plan(plan)

    return {
        **state,
        "phase": ConversationPhase.AWAITING_APPROVAL,
        "last_response": response,
        "updated_at": datetime.utcnow().isoformat(),
    }
