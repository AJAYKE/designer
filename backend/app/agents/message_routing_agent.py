from datetime import datetime
from typing import Any, Dict
from langchain_core.runnables import RunnableConfig
from langgraph.store.base import BaseStore
from app.models.conversation_state import ConversationState, ConversationPhase

async def message_routing_agent(
    state: ConversationState,
    config: RunnableConfig,
    *,
    store: BaseStore,
) -> ConversationState:
    """
    Route messages based on conversation context and determine appropriate phase
    """
    
    user_message = state.get("current_message", "")
    thread_id = state["thread_id"]
    user_id = config["configurable"]["user_id"]
    
    print(f"🧭 Message Router: Processing '{user_message[:50]}...' for {user_id}")
    
    # Analyze message intent and current context
    message_intent = await _analyze_message_intent(user_message, state, store, user_id)
    
    # Determine conversation phase
    if state.get("phase") == ConversationPhase.AWAITING_APPROVAL:
        # User is responding to a plan
        if any(word in user_message.lower() for word in ["yes", "approve", "looks good", "perfect"]):
            human_feedback = {"action": "approved", "message": user_message}
        elif any(word in user_message.lower() for word in ["change", "modify", "different", "instead"]):
            human_feedback = {"action": "edit_plan", "message": user_message, "modifications": [user_message]}
        elif any(word in user_message.lower() for word in ["cancel", "stop", "nevermind"]):
            human_feedback = {"action": "cancel", "message": user_message}
        else:
            human_feedback = {"action": "clarify", "message": user_message}
        
        return {
            **state,
            "human_feedback": human_feedback,
            "phase": ConversationPhase.PROCESSING_FEEDBACK,
            "updated_at": datetime.utcnow().isoformat()
        }
    
    elif message_intent["type"] == "new_design_request":
        # New design request - go to planning
        return {
            **state,
            "phase": ConversationPhase.PLANNING,
            "design_requirements": message_intent["requirements"],
            "updated_at": datetime.utcnow().isoformat()
        }
    
    elif message_intent["type"] == "modification_request":
        # User wants to modify existing design
        return {
            **state,
            "phase": ConversationPhase.MODIFYING,
            "modification_request": message_intent["modifications"],
            "updated_at": datetime.utcnow().isoformat()
        }
    
    else:
        # General conversation
        return {
            **state,
            "phase": ConversationPhase.CONVERSING,
            "updated_at": datetime.utcnow().isoformat()
        }


async def _analyze_message_intent(
    message: str, 
    state: ConversationState, 
    store: BaseStore, 
    user_id: str
) -> Dict[str, Any]:
    """Analyze user message to determine intent and extract requirements"""
    
    # Get conversation history for context
    namespace = ("conversations", user_id)
    recent_messages = await store.asearch(namespace, limit=5)
    
    # Simple intent detection (could be enhanced with LLM)
    message_lower = message.lower()
    
    # Design request patterns
    design_patterns = [
        "create", "build", "make", "design", "generate", 
        "dashboard", "landing", "website", "app", "page"
    ]
    
    modification_patterns = [
        "change", "modify", "update", "edit", "different",
        "instead", "rather", "switch", "make it"
    ]
    
    if any(pattern in message_lower for pattern in design_patterns):
        return {
            "type": "new_design_request",
            "requirements": message,
            "confidence": 0.8
        }
    elif any(pattern in message_lower for pattern in modification_patterns):
        return {
            "type": "modification_request", 
            "modifications": [message],
            "confidence": 0.7
        }
    else:
        return {
            "type": "general_conversation",
            "message": message,
            "confidence": 0.5
        }

