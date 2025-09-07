from datetime import datetime
from langchain_core.runnables import RunnableConfig
from langgraph.store.base import BaseStore
from app.models.conversation_state import ConversationState, ConversationPhase
from app.services.llm_service import LLMService
import logging, hashlib

logger = logging.getLogger(__name__)

DESIGN_KEYWORDS = [
    "create", "build", "make", "design", "generate", "develop",
    "website", "app", "application", "page", "landing", "dashboard",
    "login", "signup", "form", "portal", "platform", "site"
]
async def router(state: ConversationState, config: RunnableConfig, *, store: BaseStore) -> ConversationState:
    llm_service = LLMService()
    current_message = (state.get("current_message") or "").strip()
    current_phase = state.get("phase", ConversationPhase.INITIAL)

    if not current_message:
        return {
            **state,
            "phase": ConversationPhase.INITIAL,
            "last_response": "I didn't receive your message. Could you please try again?",
            "updated_at": datetime.utcnow().isoformat(),
        }

    # Optional: keep dedupe to avoid double-processing identical chunks
    sig = hashlib.sha1(current_message.encode("utf-8")).hexdigest()
    last_sig = state.get("_last_routed_sig")
    is_new_message = sig != last_sig

    try:
        if is_new_message:
            routing_result = await llm_service.route_request(
                message=current_message,
                current_phase=current_phase,
                context={
                    "design_plan": state.get("design_plan"),
                    "generated_screens": state.get("generated_screens"),
                    "last_requirements": state.get("design_requirements"),
                }
            )
            action      = routing_result.get("action", "noop")
            confidence  = float(routing_result.get("confidence", 0.5) or 0.5)
            mods        = routing_result.get("modifications") or []
            extracted   = routing_result.get("extracted_requirements") or current_message

            # --- Phase decisions (LLM-driven) ---
            if action == "cancel":
                return { **state, "phase": ConversationPhase.CANCELLED, "_last_routed_sig": sig,
                         "updated_at": datetime.utcnow().isoformat() }

            # Start a brand-new plan
            if action == "design_request" and current_phase in (ConversationPhase.INITIAL, ConversationPhase.COMPLETE):
                return {
                    **state,
                    "phase": ConversationPhase.PLANNING,
                    "design_requirements": extracted,
                    "routing_confidence": confidence,
                    "last_response": "Got it. I’ll create a plan now.",
                    "_last_routed_sig": sig,
                    "updated_at": datetime.utcnow().isoformat(),
                }

            # EDIT the existing plan → replan with prior context
            if action == "modification_request" and state.get("design_plan"):
                # Build a requirements brief that includes prior plan + concrete edits
                from json import dumps
                prior_plan = state.get("design_plan")
                edit_brief = (
                    "Please update the existing design based on these changes:\n"
                    + "\n".join(f"- {m}" for m in mods) + "\n\n"
                    "Maintain overall style unless edits conflict.\n"
                    "Here is the current plan JSON:\n"
                    + dumps(prior_plan) + "\n"
                )
                return {
                    **state,
                    "phase": ConversationPhase.PLANNING,
                    "design_requirements": edit_brief,
                    "routing_confidence": confidence,
                    "last_response": "Understood. Updating the plan and regenerating…",
                    "_last_routed_sig": sig,
                    "updated_at": datetime.utcnow().isoformat(),
                }

            # Small talk / general conversation
            if action == "small_talk":
                return {
                    **state,
                    "phase": ConversationPhase.INITIAL,  # flows to converser
                    "routing_confidence": confidence,
                    "_last_routed_sig": sig,
                    "updated_at": datetime.utcnow().isoformat(),
                }

            # If uncertain, keep current phase but mark message consumed
            return { **state, "_last_routed_sig": sig, "updated_at": datetime.utcnow().isoformat() }

    except Exception as e:
        logger.error(f"[router] LLM routing error: {e}")

    # Fallback: do not force PLANNING by keywords; default to converser path
    return {
        **state,
        "phase": ConversationPhase.INITIAL if current_phase in (ConversationPhase.COMPLETE, ConversationPhase.INITIAL) else current_phase,
        "_last_routed_sig": sig,
        "updated_at": datetime.utcnow().isoformat(),
    }
