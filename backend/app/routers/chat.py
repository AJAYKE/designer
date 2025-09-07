from typing import Any, Dict, Optional, AsyncGenerator, Set
from datetime import datetime
import json
import asyncio

from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel

from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from langgraph.store.postgres.aio import AsyncPostgresStore

from app.core.config import settings
from app.core.auth import get_current_user
from app.agents.agent import build_conversational_agent
from app.models.conversation_state import ConversationPhase
from app.services.llm_service import LLMService

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    thread_id: Optional[str] = None
    model: str = "gpt-4o-mini"
    stream: bool = True
    include_token_usage: bool = False

class ChatResponse(BaseModel):
    thread_id: str
    phase: ConversationPhase
    response: str
    data: Optional[Dict[str, Any]] = None
    requires_approval: bool = False
    token_usage: Optional[Dict[str, Any]] = None
    generation_progress: Optional[Dict[str, Any]] = None

# Global LLM service instance for token tracking
llm_service = LLMService()

def _encode_sse(event: Dict[str, Any]) -> bytes:
    """Server-Sent Events formatter"""
    payload = json.dumps(event, ensure_ascii=False, default=str)
    return f"data: {payload}\n\n".encode("utf-8")

def _human_response_from_state(state: dict) -> str:
    if last := state.get("last_response"):
        return last

    phase = state.get("phase", ConversationPhase.INITIAL)
    plan = state.get("design_plan", {}) or {}
    progress = state.get("generation_progress", {}) or {}
    screens = plan.get("screens", []) or state.get("generated_screens", [])

    if phase == ConversationPhase.INITIAL:
        return "Hello! Tell me what you want to build, and I’ll plan and generate it."
    elif phase == ConversationPhase.PLANNING:
        return "Analyzing your requirements and creating a plan…"
    elif phase == ConversationPhase.GENERATING:
        if progress:
            name = progress.get("current_screen_name") or "your screens"
            pct = progress.get("overall_progress", 0)
            return f"Generating {name}… {pct}% complete"
        return "Creating your screens…"
    elif phase == ConversationPhase.COMPLETE:
        n = len(state.get("generated_screens", []) or screens)
        return f"🎉 Successfully generated {n} screen{'s' if n!=1 else ''}! Your design is ready."
    elif phase == ConversationPhase.CANCELLED:
        return "Process cancelled. Start a new request anytime!"
    elif phase == ConversationPhase.ERROR:
        return f"Sorry, there was an error: {state.get('error_message','Something went wrong')}. Please try again."
    return "I’m ready to build. What would you like to create?"

def _state_to_response(thread_id: str, state: Dict[str, Any], include_token_usage: bool = False) -> Dict[str, Any]:
    phase = state.get("phase", ConversationPhase.INITIAL)
    response_text = _human_response_from_state(state)

    data = {}
    if plan := state.get("design_plan"):
        data["design_plan"] = plan
    if progress := state.get("generation_progress"):
        data["generation_progress"] = progress
    if screens := state.get("generated_screens"):
        data["generated_screens"] = screens
    if summary := state.get("generation_summary"):
        data["generation_summary"] = summary
    if changes := state.get("plan_changes"):
        data["plan_changes"] = changes
    if confidence := state.get("routing_confidence"):
        data["routing_confidence"] = confidence
    if fallback := state.get("fallback_used"):
        data["fallback_used"] = fallback

    resp = {
        "thread_id": thread_id,
        "phase": phase.value,
        "response": response_text,
        "data": data or None,
        "requires_approval": False,                 # ← always false now
        "generation_progress": state.get("generation_progress"),
        "progress": state.get("progress", 0),
    }
    if include_token_usage and hasattr(llm_service, 'token_tracker'):
        resp["token_usage"] = llm_service.token_tracker.get_session_summary()
    return resp

async def _make_checkpointer_and_store():
    """Create database connections for checkpointing and storage"""
    saver_cm = AsyncPostgresSaver.from_conn_string(settings.DATABASE_URL)
    store_cm = AsyncPostgresStore.from_conn_string(settings.DATABASE_URL)
    
    saver = await saver_cm.__aenter__()
    store = await store_cm.__aenter__()
    
    await saver.setup()
    await store.setup()
    
    return saver_cm, store_cm, saver, store

async def _close_checkpointer_and_store(saver_cm, store_cm):
    """Clean up database connections"""
    try:
        if saver_cm:
            await saver_cm.__aexit__(None, None, None)
    finally:
        if store_cm:
            await store_cm.__aexit__(None, None, None)

@router.post("/chat", response_model=ChatResponse)
async def chat(
    chat_request: ChatRequest,
    request: Request,
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    """
    Fixed chat endpoint with proper streaming and conversational flow
    """
    thread_id = chat_request.thread_id or f"t_{int(datetime.utcnow().timestamp()*1000)}"
    user_id = str(current_user.get("id") or current_user.get("sub") or "anonymous")
    
    saver_cm = store_cm = saver = store = None
    
    try:
        # Create database connections
        saver_cm, store_cm, saver, store = await _make_checkpointer_and_store()
        
        # Store incoming request for audit
        await store.aput(
            ("requests", user_id),
            f"{thread_id}:{int(datetime.utcnow().timestamp())}",
            {
                "message": chat_request.message,
                "model": chat_request.model,
                "timestamp": datetime.utcnow().isoformat(),
                "ip": request.client.host if request.client else None,
                "user_agent": request.headers.get("user-agent", ""),
            },
        )

        # Configure execution
        config: RunnableConfig = {
            "configurable": {
                "user_id": user_id,
                "thread_id": thread_id,
                "model": chat_request.model,
            },
            "thread_id": thread_id,
        }
        
        # Build agent graph
        graph = build_conversational_agent(checkpointer=saver, store=store)

        prior = await graph.aget_state(config)
        base_values = (prior.values if prior and prior.values else {})

        
        # Prepare initial state
        initial_state = {
            **base_values,
            "thread_id": thread_id,
            "current_message": chat_request.message,
            "updated_at": datetime.utcnow().isoformat(),
        }
        
    
        
        if chat_request.stream:
            # === STREAMING RESPONSE ===
            async def event_stream() -> AsyncGenerator[bytes, None]:
                try:
                    # Track what we've already sent to avoid duplicates
                    sent_states: Set[str] = set()
                    last_response = ""
                    
                    # For LLM streaming events, we need to handle them specially
                    streaming_content = ""
                    current_screen_id = None
                    
                    async for event in graph.astream_events(initial_state, config=config, version="v2"):
                        event_type = event.get("event", "")
                        event_name = event.get("name", "")
                        event_data = event.get("data", {})
                        
                        # Handle LLM streaming events (chunk by chunk)
                        if event_type == "on_llm_stream" and event_data.get("chunk"):
                            chunk_content = event_data["chunk"].get("content", "")
                            if chunk_content:
                                streaming_content += chunk_content
                                
                                # Stream the chunk immediately
                                chunk_payload = {
                                    "thread_id": thread_id,
                                    "type": "content_chunk",
                                    "content": chunk_content,
                                    "accumulated_content": streaming_content,
                                    "screen_id": current_screen_id
                                }
                                yield _encode_sse(chunk_payload)
                        
                        # Handle our custom streaming events from generator
                        elif event_type == "on_custom_event" and event_name == "llm_stream":
                            stream_data = event_data.get("data", {})
                            if stream_data.get("type") == "content_delta":
                                chunk_payload = {
                                    "thread_id": thread_id,
                                    "type": "generation_chunk", 
                                    "content": stream_data.get("content", ""),
                                    "accumulated_content": stream_data.get("accumulated_content", ""),
                                    "screen_id": stream_data.get("screen_id")
                                }
                                yield _encode_sse(chunk_payload)
                        
                        # Handle node completion events (but avoid duplicates)
                        elif event_type == "on_chain_end" and event_name in ["router", "planner", "generator", "LangGraph"]:
                            output = event_data.get("output")
                            
                            if isinstance(output, dict) and output.get("phase"):
                                # Create a hash of the relevant state to detect duplicates
                                state_hash = f"{output.get('phase', '')}:{output.get('last_response', '')}:{output.get('progress', 0)}"
                                
                                if state_hash not in sent_states:
                                    sent_states.add(state_hash)
                                    
                                    current_response = _human_response_from_state(output)
                                    
                                    # Only send if response actually changed
                                    if current_response != last_response:
                                        last_response = current_response
                                        
                                        payload = _state_to_response(
                                            thread_id, 
                                            output, 
                                            chat_request.include_token_usage
                                        )
                                        
                                        # Add minimal metadata
                                        payload["event_source"] = event_name
                                        
                                        yield _encode_sse(payload)
                        
                        # Check for client disconnect
                        if await request.is_disconnected():
                            break
                    
                    # Send completion event
                    completion_payload = {
                        "thread_id": thread_id,
                        "type": "stream_complete",
                        "message": "Stream completed successfully"
                    }
                    
                    if chat_request.include_token_usage:
                        completion_payload["session_token_usage"] = llm_service.token_tracker.get_session_summary()
                    
                    yield _encode_sse(completion_payload)
                    
                except asyncio.CancelledError:
                    yield _encode_sse({
                        "thread_id": thread_id,
                        "type": "cancelled",
                        "message": "Stream cancelled by client"
                    })
                except Exception as e:
                    import logging
                    logger = logging.getLogger(__name__)
                    logger.error(f"Streaming error: {e}", exc_info=True)
                    yield _encode_sse({
                        "thread_id": thread_id,
                        "type": "error",
                        "message": str(e)
                    })
                finally:
                    # Clean up resources
                    await _close_checkpointer_and_store(saver_cm, store_cm)
            
            return StreamingResponse(
                event_stream(),
                media_type="text/event-stream",
                headers={
                    "Cache-Control": "no-cache, no-transform",
                    "Connection": "keep-alive",
                    "X-Accel-Buffering": "no",
                },
            )
        
        else:
            # === NON-STREAMING RESPONSE ===
            final_state = await graph.ainvoke(initial_state, config=config)
            
            # Store final state for analytics
            await store.aput(
                ("final_states", user_id),
                thread_id,
                {
                    "state": final_state,
                    "timestamp": datetime.utcnow().isoformat(),
                    "token_usage": llm_service.token_tracker.get_session_summary() if chat_request.include_token_usage else None,
                }
            )
            
            await _close_checkpointer_and_store(saver_cm, store_cm)
            
            return JSONResponse(_state_to_response(
                thread_id, 
                final_state, 
                chat_request.include_token_usage
            ))
    
    except Exception as e:
        # Ensure cleanup on any error
        await _close_checkpointer_and_store(saver_cm, store_cm)
        
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Chat endpoint error: {e}", exc_info=True)
        
        raise HTTPException(
            status_code=500,
            detail={
                "error": "chat_processing_failed",
                "message": str(e),
                "thread_id": thread_id,
            }
        )

@router.get("/chat/{thread_id}/usage")
async def get_usage_stats(
    thread_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    """Get token usage statistics for a conversation thread"""
    
    if hasattr(llm_service, 'token_tracker'):
        return {
            "thread_id": thread_id,
            "session_summary": llm_service.token_tracker.get_session_summary(),
            "recent_operations": llm_service.token_tracker.get_recent_operations(minutes=30),
        }
    
    return {
        "thread_id": thread_id,
        "message": "Token tracking not available",
    }