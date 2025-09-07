from app.models.conversation_state import ConversationState
from datetime import datetime
from langchain_core.runnables import RunnableConfig
from langgraph.store.base import BaseStore
from app.models.conversation_state import ConversationPhase
from app.services.llm_service import LLMService
import logging

logger = logging.getLogger(__name__)

async def converser(state: ConversationState, config: RunnableConfig, *, store: BaseStore) -> ConversationState:
    llm_service = LLMService()
    current_message = state.get("current_message", "").strip()
    try:
        conversational_response = await llm_service.generate_conversational_response(
            current_message,
            context={
                "design_plan": state.get("design_plan"),
                "generated_screens": state.get("generated_screens"),
            }
        )
        return { **state, "phase": ConversationPhase.INITIAL,
                 "last_response": conversational_response,
                 "routing_confidence": 0.7,
                 "updated_at": datetime.utcnow().isoformat() }
    except Exception as e:
        logger.error(f"LLM conversational response error: {e}")
        return { **state, "phase": ConversationPhase.INITIAL,
                 "updated_at": datetime.utcnow().isoformat() }
