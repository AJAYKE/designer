from datetime import datetime
from langchain_core.runnables import RunnableConfig
from langgraph.store.base import BaseStore
from app.models.conversation_state import ConversationState, ConversationPhase
from app.services.llm_service import LLMService
import logging

logger = logging.getLogger(__name__)

def _create_fallback_plan(requirements: str) -> dict:
    return {
        "estimated_complexity": "simple",
        "design_system": {"color_scheme": "modern", "primary_color": "blue-500"},
        "screens": [{
            "id": "screen_1",
            "screen_type": "landing",
            "title": "Landing Page",
            "description": "Auto-generated baseline plan from requirements.",
            "order": 1,
            "components": ["Header", "Hero with CTA", "Features", "Footer"]
        }]
    }

async def planner(state: ConversationState, config: RunnableConfig, *, store: BaseStore) -> ConversationState:
    llm_service = LLMService()
    try:
        requirements = state.get("design_requirements", "Create a simple website")
        prior_plan = state.get("design_plan")  # may be None for new designs
        logger.info(f"Generating design plan. Prior plan exists? {bool(prior_plan)}")

        # NEW: pass prior plan to help with incremental edits
        plan = await llm_service.generate_design_plan(requirements, context={"prior_plan": prior_plan})
        if not isinstance(plan, dict) or not plan.get("screens"):
            logger.warning("Invalid plan structure, using fallback")
            plan = _create_fallback_plan(requirements)

        for i, screen in enumerate(plan.get("screens", [])):
            screen.setdefault("id", f"screen_{i+1}")
            screen.setdefault("order", i + 1)
        plan["screens"].sort(key=lambda s: s.get("order", 999))

        response_text = (
            f"Planned a {plan.get('estimated_complexity','medium')} design with "
            f"{len(plan['screens'])} screens. Generating now…"
        )

        return {
            **state,
            "design_plan": plan,                # ← updated plan replaces old one
            "phase": ConversationPhase.GENERATING,
            "progress": max(25, state.get("progress", 0)),
            "last_response": response_text,
            # Optional: drop stale generated_screens so UI shows fresh output only
            "generated_screens": None,
            "updated_at": datetime.utcnow().isoformat(),
        }
    except Exception as e:
        logger.error(f"Planning error: {e}")
        fallback_plan = _create_fallback_plan(state.get("design_requirements", "simple website"))
        return {
            **state,
            "design_plan": fallback_plan,
            "phase": ConversationPhase.GENERATING,
            "progress": 20,
            "last_response": "Planned a basic design (fallback). Generating now…",
            "error_message": f"Planning fallback used: {str(e)}",
            "updated_at": datetime.utcnow().isoformat(),
        }
