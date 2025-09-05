from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any, AsyncGenerator, List
import json
import asyncio
from datetime import datetime
from uuid import uuid4

from app.models.conversation_state import ConversationState, ConversationPhase
from app.middleware.auth_middleware import get_current_user
from app.middleware.rate_limit_middleware import request_rate_limit
# from app.agents.conversational_agent import build_conversational_agent

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    thread_id: Optional[str] = None
    model: str = "openai:gpt-4"
    stream: bool = True

class ChatResponse(BaseModel):
    thread_id: str
    phase: ConversationPhase
    response: str
    data: Optional[Dict[str, Any]] = None
    requires_approval: bool = False

@router.post("/chat")
@request_rate_limit(calls=20, period=60)  # 20 messages per minute
async def unified_chat_endpoint(
    chat_request: ChatRequest,
    request: Request,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Unified conversational endpoint that handles:
    1. Initial design requests
    2. Plan approval/editing  
    3. Generation progress streaming
    4. Follow-up modifications
    5. General conversation
    """
    
    if request.stream:
        return StreamingResponse(
            _stream_conversation(chat_request, current_user, request),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*"
            }
        )
    else:
        return await _handle_single_chat_request(chat_request, current_user, request)


async def _stream_conversation(
    request: ChatRequest,
    current_user: Dict[str, Any],
    fastapi_request: Request
) -> AsyncGenerator[str, None]:
    """Stream conversation responses with real-time updates"""
    
    try:
        user_id = current_user["user_id"]
        thread_id = request.thread_id or str(uuid4())
        
        # Get conversational agent
        agent, checkpointer, store = fastapi_request.app.state.conversational_agent

        
        config = {
            "configurable": {
                "thread_id": thread_id,
                "user_id": user_id,
            }
        }
        
        # Get existing conversation state or create new
        existing_state = await checkpointer.aget(config)

        
        if existing_state:
            # Continue existing conversation
            initial_state = {
                **existing_state,
                "current_message": request.message,
                "selected_model": request.model,
                "updated_at": datetime.utcnow().isoformat()
            }
        else:
            # New conversation
            initial_state = ConversationState(
                thread_id=thread_id,
                user_id=user_id,
                phase=ConversationPhase.INITIAL,
                current_message=request.message,
                message_history=[],
                design_requirements=None,
                design_plan=None,
                plan_approved=False,
                plan_modifications=[],
                human_feedback=None,
                generated_screens=[],
                generation_progress={},
                selected_model=request.model,
                conversation_context={},
                created_at=datetime.utcnow().isoformat(),
                updated_at=datetime.utcnow().isoformat()
            )
        
        # Stream conversation processing
        async for chunk in agent.astream(
            initial_state,
            config,
            stream_mode="values"
        ):
            current_state = chunk
            
            # Create streaming response based on phase
            stream_data = await _create_stream_response(current_state, request.message)
            
            yield f"data: {json.dumps(stream_data, default=str)}\n\n"
            
            # Handle interruption points
            if current_state.get("phase") == ConversationPhase.AWAITING_APPROVAL:
                # Send approval request and wait
                approval_data = {
                    "type": "approval_required",
                    "thread_id": thread_id,
                    "phase": current_state["phase"],
                    "design_plan": current_state.get("design_plan"),
                    "requires_human_input": True,
                    "message": "Please review the plan above. Say 'looks good' to proceed, or suggest changes."
                }
                
                yield f"data: {json.dumps(approval_data, default=str)}\n\n"
                break  # Wait for next user message
            
            # Break if conversation complete
            if current_state.get("phase") in [ConversationPhase.COMPLETE, ConversationPhase.ERROR]:
                break
            
            # Small delay to prevent overwhelming
            await asyncio.sleep(0.1)
        
    except Exception as e:
        error_response = {
            "type": "error",
            "error": str(e),
            "thread_id": thread_id if 'thread_id' in locals() else "unknown"
        }
        yield f"data: {json.dumps(error_response)}\n\n"


async def _handle_single_chat_request(
    request: ChatRequest,
    current_user: Dict[str, Any],
    fastapi_request: Request
) -> ChatResponse:
    """Handle non-streaming chat request"""
    
    user_id = current_user["user_id"]
    thread_id = request.thread_id or str(uuid4())
    
    # Get conversational agent
    agent, checkpointer, store = fastapi_request.app.state.conversational_agent
    
    config = {
        "configurable": {
            "thread_id": thread_id,
            "user_id": user_id,
        }
    }
    
    # Process conversation
    result_state = None
    async for chunk in agent.astream(
        {"current_message": request.message, "thread_id": thread_id, "user_id": user_id},
        config,
        stream_mode="values"
    ):
        result_state = chunk
        
        # Stop at interruption points
        if result_state.get("phase") == ConversationPhase.AWAITING_APPROVAL:
            break
    
    # Create response
    return ChatResponse(
        thread_id=thread_id,
        phase=result_state.get("phase", ConversationPhase.ERROR),
        response=_generate_response_message(result_state),
        data=_extract_response_data(result_state),
        requires_approval=result_state.get("phase") == ConversationPhase.AWAITING_APPROVAL
    )


async def _create_stream_response(state: ConversationState, original_message: str) -> Dict[str, Any]:
    """Create appropriate streaming response based on conversation state"""
    
    phase = state.get("phase", ConversationPhase.INITIAL)
    
    base_response = {
        "thread_id": state["thread_id"],
        "phase": phase,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    if phase == ConversationPhase.PLANNING:
        return {
            **base_response,
            "type": "planning",
            "message": "Analyzing your requirements and creating a design plan...",
            "status": "thinking"
        }
    
    elif phase == ConversationPhase.AWAITING_APPROVAL:
        return {
            **base_response,
            "type": "plan_ready",
            "message": "Here's your design plan:",
            "design_plan": state.get("design_plan"),
            "status": "awaiting_approval"
        }
    
    elif phase == ConversationPhase.GENERATING:
        progress = state.get("generation_progress", {})
        return {
            **base_response,
            "type": "generating",
            "message": "Generating your designs...",
            "progress": progress,
            "status": "generating"
        }
    
    elif phase == ConversationPhase.COMPLETE:
        return {
            **base_response,
            "type": "complete",
            "message": "Your designs are ready!",
            "generated_screens": state.get("generated_screens", []),
            "status": "complete"
        }
    
    else:
        return {
            **base_response,
            "type": "message",
            "message": _generate_response_message(state),
            "status": "ready"
        }


def _generate_response_message(state: ConversationState) -> str:
    """Generate appropriate response message based on state"""
    
    phase = state.get("phase", ConversationPhase.INITIAL)
    
    messages = {
        ConversationPhase.PLANNING: "Let me analyze your requirements and create a design plan...",
        ConversationPhase.AWAITING_APPROVAL: "Please review the design plan above and let me know if you'd like to proceed or make changes.",
        ConversationPhase.GENERATING: "Generating your designs now...",
        ConversationPhase.COMPLETE: "Your designs are ready! You can preview, copy, or export them.",
        ConversationPhase.ERROR: f"I encountered an error: {state.get('error_message', 'Unknown error')}",
        ConversationPhase.CANCELLED: "Design process cancelled. Feel free to start a new design anytime!"
    }
    
    return messages.get(phase, "How can I help you with your design?")


def _extract_response_data(state: ConversationState) -> Optional[Dict[str, Any]]:
    """Extract relevant data for response"""
    
    phase = state.get("phase")
    
    if phase == ConversationPhase.AWAITING_APPROVAL:
        return {"design_plan": state.get("design_plan")}
    elif phase == ConversationPhase.GENERATING:
        return {"progress": state.get("generation_progress")}
    elif phase == ConversationPhase.COMPLETE:
        return {"generated_screens": state.get("generated_screens")}
    else:
        return None


@router.get("/chat/{thread_id}/status")
async def get_chat_status(
    thread_id: str,
    request: Request,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get current status of a chat conversation"""
    
    try:
        user_id = current_user["user_id"]
        
        # Get conversational agent
        agent, checkpointer, store = fastapi_request.app.state.conversational_agent
        
        config = {
            "configurable": {
                "thread_id": thread_id,
                "user_id": user_id,
            }
        }
        
        # Get current state
        state = await checkpointer.aget(config)
        if not state:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        return {
            "thread_id": thread_id,
            "phase": state.get("phase"),
            "requires_approval": state.get("phase") == ConversationPhase.AWAITING_APPROVAL,
            "design_plan": state.get("design_plan"),
            "generated_screens": state.get("generated_screens", []),
            "updated_at": state.get("updated_at")
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get chat status: {str(e)}")


@router.post("/chat/{thread_id}/resume")
async def resume_interrupted_chat(
    thread_id: str,
    request: Request,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Resume an interrupted conversation (after approval)"""
    
    try:
        user_id = current_user["user_id"]
        
        # Get conversational agent
        agent, checkpointer, store = fastapi_request.app.state.conversational_agent
        
        config = {
            "configurable": {
                "thread_id": thread_id,
                "user_id": user_id,
            }
        }
        
        # Resume from interruption
        result_state = None
        async for chunk in agent.astream(None, config, stream_mode="values"):
            result_state = chunk
            break
        
        return {
            "thread_id": thread_id,
            "resumed": True,
            "phase": result_state.get("phase") if result_state else "unknown"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to resume chat: {str(e)}")


@router.delete("/chat/{thread_id}")
async def delete_conversation(
    thread_id: str,
    request: Request,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Delete a conversation and its history"""
    
    try:
        user_id = current_user["user_id"]
        
        # Get conversational agent
        agent, checkpointer, store = fastapi_request.app.state.conversational_agent
        
        config = {
            "configurable": {
                "thread_id": thread_id,
                "user_id": user_id,
            }
        }
        
        # Delete from checkpointer
        await checkpointer.adelete(config)
        
        return {"message": f"Conversation {thread_id} deleted successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete conversation: {str(e)}")