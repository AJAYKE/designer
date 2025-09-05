from langchain_core.runnables import RunnableConfig
from langgraph.store.base import BaseStore
from typing import Dict, Any, List
from datetime import datetime
import json

from app.models.conversation_state import ConversationState, ConversationPhase
from app.services.multi_model_llm_service import MultiModelLLMService

async def conversation_management_agent(
    state: ConversationState,
    config: RunnableConfig,
    *,
    store: BaseStore,
) -> ConversationState:
    """
    Manage overall conversation flow, context, and determine next steps.
    This is the "brain" of the conversational system that handles:
    - General conversation responses
    - Context management and memory
    - Conversation completion detection
    - Follow-up request handling
    - Error recovery and edge cases
    """
    
    print(f"💬 Conversation Manager: Processing phase {state['phase']} for {state['thread_id']}")
    
    try:
        user_id = config["configurable"]["user_id"]
        current_message = state.get("current_message", "")
        phase = state.get("phase", ConversationPhase.INITIAL)
        
        # Update message history
        updated_history = state.get("message_history", [])
        updated_history.append({
            "role": "user",
            "content": current_message,
            "timestamp": datetime.utcnow().isoformat(),
            "phase": phase
        })
        
        # Determine conversation action based on phase and context
        conversation_action = await _determine_conversation_action(state, user_id, store)
        
        # Generate appropriate response
        response_data = await _generate_conversation_response(
            conversation_action,
            state,
            user_id,
            store
        )
        
        # Update conversation context
        updated_context = await _update_conversation_context(
            state,
            conversation_action,
            response_data,
            user_id,
            store
        )
        
        # Add assistant response to history
        updated_history.append({
            "role": "assistant", 
            "content": response_data.get("response", ""),
            "timestamp": datetime.utcnow().isoformat(),
            "action": conversation_action["type"],
            "data": response_data.get("data")
        })
        
        # Determine final conversation phase
        final_phase = _determine_final_phase(conversation_action, state)
        
        return {
            **state,
            "phase": final_phase,
            "message_history": updated_history,
            "conversation_context": updated_context,
            "last_response": response_data.get("response", ""),
            "last_action": conversation_action["type"],
            "updated_at": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        print(f"❌ Conversation Management Error: {str(e)}")
        
        # Error recovery - try to continue conversation gracefully
        error_response = "I encountered an issue processing your request. Could you try rephrasing that, or let me know if you'd like to start a new design?"
        
        updated_history = state.get("message_history", [])
        updated_history.append({
            "role": "assistant",
            "content": error_response,
            "timestamp": datetime.utcnow().isoformat(),
            "action": "error_recovery",
            "error": str(e)
        })
        
        return {
            **state,
            "phase": ConversationPhase.CONVERSING,
            "message_history": updated_history,
            "last_response": error_response,
            "last_action": "error_recovery",
            "error_message": f"Conversation management error: {str(e)}",
            "updated_at": datetime.utcnow().isoformat()
        }


async def _determine_conversation_action(
    state: ConversationState,
    user_id: str,
    store: BaseStore
) -> Dict[str, Any]:
    """Analyze current state and determine what conversational action to take"""
    
    phase = state.get("phase", ConversationPhase.INITIAL)
    current_message = state.get("current_message", "").lower()
    
    # Phase-specific action determination
    if phase == ConversationPhase.COMPLETE:
        # Design is complete - check for follow-up requests
        if any(word in current_message for word in ["modify", "change", "update", "edit", "different"]):
            return {
                "type": "modification_request",
                "priority": "high",
                "description": "User wants to modify completed design"
            }
        elif any(word in current_message for word in ["new", "another", "create", "build", "make"]):
            return {
                "type": "new_design_request", 
                "priority": "high",
                "description": "User wants to start a new design"
            }
        elif any(word in current_message for word in ["export", "download", "copy", "save"]):
            return {
                "type": "export_assistance",
                "priority": "medium",
                "description": "User needs help with exporting/using the design"
            }
        else:
            return {
                "type": "general_followup",
                "priority": "low", 
                "description": "General conversation about completed design"
            }
    
    elif phase == ConversationPhase.ERROR:
        # Recover from error state
        return {
            "type": "error_recovery",
            "priority": "high",
            "description": "Help user recover from error and continue"
        }
    
    elif phase == ConversationPhase.CANCELLED:
        # Design was cancelled - offer to restart
        return {
            "type": "restart_offer",
            "priority": "medium",
            "description": "Offer to start a new design after cancellation"
        }
    
    elif phase == ConversationPhase.GENERATING:
        # Currently generating - provide status or handle interruption
        if any(word in current_message for word in ["stop", "cancel", "abort"]):
            return {
                "type": "generation_cancellation",
                "priority": "high", 
                "description": "User wants to cancel ongoing generation"
            }
        else:
            return {
                "type": "generation_status",
                "priority": "low",
                "description": "Provide generation status update"
            }
    
    else:
        # Default conversational handling
        return {
            "type": "general_conversation",
            "priority": "medium",
            "description": "Handle general conversation"
        }


async def _generate_conversation_response(
    conversation_action: Dict[str, Any],
    state: ConversationState, 
    user_id: str,
    store: BaseStore
) -> Dict[str, Any]:
    """Generate appropriate response based on conversation action"""
    
    action_type = conversation_action["type"]
    current_message = state.get("current_message", "")
    
    if action_type == "modification_request":
        return await _handle_modification_request(state, current_message, user_id, store)
    
    elif action_type == "new_design_request":
        return await _handle_new_design_request(state, current_message, user_id, store)
    
    elif action_type == "export_assistance":
        return await _handle_export_assistance(state, current_message, user_id, store)
    
    elif action_type == "general_followup":
        return await _handle_general_followup(state, current_message, user_id, store)
    
    elif action_type == "error_recovery":
        return await _handle_error_recovery(state, current_message, user_id, store)
    
    elif action_type == "restart_offer":
        return await _handle_restart_offer(state, current_message, user_id, store)
    
    elif action_type == "generation_cancellation":
        return await _handle_generation_cancellation(state, current_message, user_id, store)
    
    elif action_type == "generation_status":
        return await _handle_generation_status(state, current_message, user_id, store)
    
    else:  # general_conversation
        return await _handle_general_conversation(state, current_message, user_id, store)


async def _handle_modification_request(
    state: ConversationState,
    message: str,
    user_id: str,
    store: BaseStore
) -> Dict[str, Any]:
    """Handle requests to modify completed designs"""
    
    generated_screens = state.get("generated_screens", [])
    
    if not generated_screens:
        return {
            "response": "I don't see any completed designs to modify. Would you like me to create a new design for you?",
            "data": {"action": "offer_new_design"}
        }
    
    # Analyze what kind of modification is requested
    modification_analysis = await _analyze_modification_request(message, generated_screens, user_id, store)
    
    if modification_analysis["scope"] == "minor":
        return {
            "response": f"I can help you {modification_analysis['description']}. Let me update that for you.",
            "data": {
                "action": "apply_modification",
                "modification_type": modification_analysis["type"],
                "affected_screens": modification_analysis["screens"]
            }
        }
    else:
        return {
            "response": f"That's a significant change - {modification_analysis['description']}. Would you like me to create a new design plan incorporating these changes?",
            "data": {
                "action": "request_new_plan",
                "modification_type": modification_analysis["type"], 
                "changes_requested": message
            }
        }


async def _handle_new_design_request(
    state: ConversationState,
    message: str,
    user_id: str,
    store: BaseStore
) -> Dict[str, Any]:
    """Handle requests for new designs"""
    
    return {
        "response": "Great! I'd be happy to help you create a new design. Let me analyze your requirements and create a plan.",
        "data": {
            "action": "start_new_design",
            "requirements": message,
            "transition_to_phase": ConversationPhase.PLANNING
        }
    }


async def _handle_export_assistance(
    state: ConversationState,
    message: str,
    user_id: str,
    store: BaseStore
) -> Dict[str, Any]:
    """Help users export or use their designs"""
    
    generated_screens = state.get("generated_screens", [])
    
    if not generated_screens:
        return {
            "response": "I don't see any completed designs to export. Once you have generated designs, I can help you copy the code, download files, or export to Figma.",
            "data": {"action": "no_designs_available"}
        }
    
    export_help = """Here are your options for using your designs:

📋 **Copy Code**: Click the copy button to get the HTML + CSS + JavaScript
📁 **Download ZIP**: Get all files packaged together
🎨 **Export to Figma**: Convert to Figma components (coming soon)
🔗 **Share Link**: Get a public URL to share your design

The generated code uses only HTML + Tailwind CSS + vanilla JavaScript, so you can use it anywhere - in React, Vue, or plain HTML projects."""

    return {
        "response": export_help,
        "data": {
            "action": "export_options",
            "available_screens": len(generated_screens),
            "export_formats": ["html", "zip", "figma"]
        }
    }


async def _handle_general_followup(
    state: ConversationState,
    message: str,
    user_id: str,
    store: BaseStore
) -> Dict[str, Any]:
    """Handle general conversation about completed designs"""
    
    # Use LLM to generate contextual response
    llm_service = MultiModelLLMService()
    
    context_prompt = f"""
You are an AI design assistant. The user just completed generating a design and said: "{message}"

Based on the conversation context, provide a helpful, friendly response. Be concise and offer next steps if appropriate.

Context:
- User has completed designs
- This is general follow-up conversation
- Keep response natural and helpful
"""
    
    try:
        response = await llm_service.generate_screen_code(
            context_prompt,
            screen_type=None,  # Not generating a screen
            model="openai:gpt-3.5-turbo"  # Use lighter model for conversation
        )
        
        return {
            "response": response.strip(),
            "data": {"action": "conversational_response"}
        }
    except:
        # Fallback response
        return {
            "response": "Your designs look great! Is there anything specific you'd like to know about them, or would you like to create something new?",
            "data": {"action": "fallback_response"}
        }


async def _handle_error_recovery(
    state: ConversationState,
    message: str,
    user_id: str,
    store: BaseStore
) -> Dict[str, Any]:
    """Help user recover from errors"""
    
    return {
        "response": "I'm ready to help! You can ask me to create a new design, modify an existing one, or if you're having issues, try being more specific about what you'd like me to build.",
        "data": {
            "action": "error_recovery",
            "suggestions": ["create new design", "modify existing", "ask for help"]
        }
    }


async def _handle_restart_offer(
    state: ConversationState,
    message: str,
    user_id: str,
    store: BaseStore
) -> Dict[str, Any]:
    """Offer to restart after cancellation"""
    
    return {
        "response": "No problem! I'm here whenever you're ready. Just describe what you'd like to create and I'll help you build it.",
        "data": {"action": "ready_for_new_design"}
    }


async def _handle_generation_cancellation(
    state: ConversationState,
    message: str,
    user_id: str,
    store: BaseStore
) -> Dict[str, Any]:
    """Handle requests to cancel ongoing generation"""
    
    return {
        "response": "I'll stop the current generation. Would you like to try a different approach or create something else?",
        "data": {
            "action": "cancel_generation", 
            "offer_alternatives": True
        }
    }


async def _handle_generation_status(
    state: ConversationState,
    message: str,
    user_id: str,
    store: BaseStore
) -> Dict[str, Any]:
    """Provide status update during generation"""
    
    progress = state.get("generation_progress", {})
    
    return {
        "response": f"I'm currently generating your designs. Progress: {progress.get('overall_progress', 0)}%. This should be ready soon!",
        "data": {
            "action": "status_update",
            "progress": progress
        }
    }


async def _handle_general_conversation(
    state: ConversationState,
    message: str,
    user_id: str,
    store: BaseStore
) -> Dict[str, Any]:
    """Handle general conversational messages"""
    
    # Simple conversational responses
    message_lower = message.lower()
    
    if any(greeting in message_lower for greeting in ["hello", "hi", "hey"]):
        return {
            "response": "Hello! I'm your AI design assistant. I can help you create websites, dashboards, mobile apps, and more. What would you like to build today?",
            "data": {"action": "greeting"}
        }
    
    elif any(word in message_lower for word in ["help", "what can you do"]):
        help_response = """I can help you create beautiful, responsive designs! Here's what I can do:

🎨 **Design Generation**: Create landing pages, dashboards, login screens, and more
📱 **Multi-Platform**: Web and mobile-optimized designs  
⚡ **Real-time Creation**: Watch your designs come to life as I build them
🎯 **Customization**: Choose styles, colors, fonts, and animations
💾 **Export Options**: Get clean HTML, CSS, and JavaScript code

Just tell me what you'd like to create, like "Build a modern dashboard" or "Create a landing page for my startup"!"""
        
        return {
            "response": help_response,
            "data": {"action": "help_provided"}
        }
    
    else:
        return {
            "response": "I'm here to help you create amazing designs! Tell me what you'd like to build, or ask me about my capabilities.",
            "data": {"action": "general_prompt"}
        }


async def _analyze_modification_request(
    message: str,
    generated_screens: List[Dict],
    user_id: str,
    store: BaseStore
) -> Dict[str, Any]:
    """Analyze the scope and type of modification requested"""
    
    message_lower = message.lower()
    
    # Detect modification scope
    minor_changes = ["color", "font", "text", "button", "spacing", "size"]
    major_changes = ["layout", "structure", "completely different", "redesign", "start over"]
    
    if any(change in message_lower for change in major_changes):
        scope = "major"
    elif any(change in message_lower for change in minor_changes):
        scope = "minor"
    else:
        scope = "unclear"
    
    # Detect what's being changed
    if "color" in message_lower:
        modification_type = "color_change"
        description = "change the color scheme"
    elif any(word in message_lower for word in ["font", "text", "typography"]):
        modification_type = "typography_change"
        description = "update the typography"
    elif "layout" in message_lower:
        modification_type = "layout_change"
        description = "modify the layout structure"
    else:
        modification_type = "general_change"
        description = "make the requested changes"
    
    return {
        "scope": scope,
        "type": modification_type,
        "description": description,
        "screens": ["all"],  # Could be more specific based on analysis
        "original_request": message
    }


async def _update_conversation_context(
    state: ConversationState,
    conversation_action: Dict[str, Any],
    response_data: Dict[str, Any],
    user_id: str,
    store: BaseStore
) -> Dict[str, Any]:
    """Update conversation context with new information"""
    
    current_context = state.get("conversation_context", {})
    
    # Update context based on action taken
    updated_context = {
        **current_context,
        "last_action": conversation_action["type"],
        "last_response_time": datetime.utcnow().isoformat(),
        "conversation_turns": current_context.get("conversation_turns", 0) + 1
    }
    
    # Track specific context based on action type
    if conversation_action["type"] == "modification_request":
        updated_context["pending_modifications"] = response_data.get("data", {})
    elif conversation_action["type"] == "new_design_request":
        updated_context["new_design_requested"] = True
        updated_context["requirements"] = state.get("current_message", "")
    
    # Store conversation analytics
    namespace = ("conversation_analytics", user_id)
    await store.aput(
        namespace,
        f"turn_{state['thread_id']}_{updated_context['conversation_turns']}",
        {
            "data": f"Conversation turn: {conversation_action['type']}",
            "action": conversation_action["type"],
            "phase": state.get("phase"),
            "timestamp": datetime.utcnow().isoformat()
        }
    )
    
    return updated_context


def _determine_final_phase(conversation_action: Dict[str, Any], state: ConversationState) -> ConversationPhase:
    """Determine what phase the conversation should be in after this action"""
    
    action_type = conversation_action["type"]
    current_phase = state.get("phase", ConversationPhase.CONVERSING)
    
    # Phase transitions based on conversation action
    phase_transitions = {
        "new_design_request": ConversationPhase.PLANNING,
        "modification_request": ConversationPhase.MODIFYING,
        "generation_cancellation": ConversationPhase.CANCELLED,
        "error_recovery": ConversationPhase.CONVERSING,
        "restart_offer": ConversationPhase.CONVERSING
    }
    
    return phase_transitions.get(action_type, current_phase)