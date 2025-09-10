from typing import Any, Dict, Optional, AsyncGenerator, Set
from datetime import datetime
import time
import json
import asyncio
import logging
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

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    """Server-Sent Events formatter with debug info"""
    payload = json.dumps(event, ensure_ascii=False, default=str)
    logger.debug(f"Sending SSE event: {event.get('type', 'unknown')} - {len(payload)} bytes")
    return f"data: {payload}\n\n".encode("utf-8")

async def _send_heartbeat(thread_id: str) -> bytes:
    """Send periodic heartbeat to keep connection alive"""
    return _encode_sse({
        "thread_id": thread_id,
        "type": "heartbeat",
        "timestamp": datetime.utcnow().isoformat(),
        "message": "Connection alive"
    })

async def _send_progress_update(thread_id: str, phase: str, message: str, progress: int = 0) -> bytes:
    """Send detailed progress updates"""
    return _encode_sse({
        "thread_id": thread_id,
        "type": "progress_update",
        "phase": phase,
        "message": message,
        "progress": progress,
        "timestamp": datetime.utcnow().isoformat()
    })


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

def _safe_str(value) -> str:
    """Safely convert any value to string, handling enums and complex types"""
    if value is None:
        return ""
    elif hasattr(value, 'value'):  # Handle enums
        return str(value.value)
    else:
        return str(value)

@router.post("/chat", response_model=ChatResponse)
async def chat(
    chat_request: ChatRequest,
    request: Request,
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    thread_id = chat_request.thread_id or f"t_{int(datetime.utcnow().timestamp()*1000)}"
    user_id = str(current_user.get("id") or current_user.get("sub") or "anonymous")
    
    logger.info(f"Starting chat for thread_id: {thread_id}, user_id: {user_id}")
    
    saver_cm = store_cm = saver = store = None
    
    try:
        # Database setup (same as before)
        start_time = time.time()
        saver_cm, store_cm, saver, store = await asyncio.wait_for(
            _make_checkpointer_and_store(), 
            timeout=10.0
        )
        logger.info(f"Database connections established in {time.time() - start_time:.2f}s")
        
        # Store request audit
        await asyncio.wait_for(
            store.aput(
                ("requests", user_id),
                f"{thread_id}:{int(datetime.utcnow().timestamp())}",
                {
                    "message": chat_request.message,
                    "model": chat_request.model,
                    "timestamp": datetime.utcnow().isoformat(),
                    "ip": request.client.host if request.client else None,
                    "user_agent": request.headers.get("user-agent", ""),
                },
            ),
            timeout=5.0
        )

        config = {
            "configurable": {
                "user_id": user_id,
                "thread_id": thread_id,
                "model": chat_request.model,
            },
            "thread_id": thread_id,
        }
        
        graph = build_conversational_agent(checkpointer=saver, store=store)
        prior = await graph.aget_state(config)
        base_values = (prior.values if prior and prior.values else {})
        
        initial_state = {
            **base_values,
            "thread_id": thread_id,
            "current_message": chat_request.message,
            "updated_at": datetime.utcnow().isoformat(),
        }
        
        if chat_request.stream:
            # === FIXED STREAMING WITH INDEPENDENT HEARTBEAT ===
            async def event_stream() -> AsyncGenerator[bytes, None]:
                connection_start = time.time()
                heartbeat_interval = 15  # 15 seconds
                
                # Shared state between tasks
                stream_active = True
                heartbeat_queue = asyncio.Queue()
                event_queue = asyncio.Queue()
                
                async def heartbeat_task():
                    """Independent heartbeat sender"""
                    try:
                        while stream_active:
                            await asyncio.sleep(heartbeat_interval)
                            if stream_active:  # Check again after sleep
                                heartbeat_data = {
                                    "thread_id": thread_id,
                                    "type": "heartbeat",
                                    "timestamp": datetime.utcnow().isoformat(),
                                    "message": "Connection alive",
                                    "connection_age": time.time() - connection_start
                                }
                                await heartbeat_queue.put(heartbeat_data)
                    except asyncio.CancelledError:
                        logger.debug("Heartbeat task cancelled")
                
                async def graph_processing_task():
                    """Process graph events"""
                    try:
                        event_count = 0
                        sent_states: Set[str] = set()
                        last_response = ""
                        
                        async for event in graph.astream_events(initial_state, config=config, version="v2"):
                            if not stream_active:
                                break
                                
                            current_time = time.time()
                            event_count += 1
                            
                            # Check for client disconnect periodically
                            if event_count % 10 == 0 and await request.is_disconnected():
                                logger.warning(f"Client disconnected for thread {thread_id}")
                                await event_queue.put({"type": "client_disconnected"})
                                break
                            
                            event_type = event.get("event", "")
                            event_name = event.get("name", "")
                            event_data = event.get("data", {})
                            
                            logger.debug(f"Processing event: {event_type} - {event_name}")
                            
                            # Handle chain start events
                            if event_type == "on_chain_start" and event_name in ["router", "planner", "generator"]:
                                phase_messages = {
                                    "router": "Analyzing your request...",
                                    "planner": "Creating design plan...",
                                    "generator": "Generating your designs..."
                                }
                                progress_data = {
                                    "thread_id": thread_id,
                                    "type": "progress_update",
                                    "phase": event_name,
                                    "message": phase_messages.get(event_name, f"Starting {event_name}..."),
                                    "progress": 0,
                                    "timestamp": datetime.utcnow().isoformat()
                                }
                                await event_queue.put(progress_data)
                            
                            # Handle LLM streaming
                            elif event_type == "on_llm_stream" and event_data.get("chunk"):
                                chunk_content = event_data["chunk"].get("content", "")
                                if chunk_content:
                                    chunk_data = {
                                        "thread_id": thread_id,
                                        "type": "content_chunk",
                                        "content": chunk_content,
                                        "timestamp": datetime.utcnow().isoformat()
                                    }
                                    await event_queue.put(chunk_data)
                            
                            # Handle node completion
                            elif event_type == "on_chain_end" and event_name in ["router", "planner", "generator", "LangGraph"]:
                                output = event_data.get("output")
                                
                                if isinstance(output, dict):
                                    # Safe state hashing with enum handling
                                    state_components = [
                                        _safe_str(output.get('phase', '')),
                                        _safe_str(output.get('last_response', ''))[:100],
                                        _safe_str(output.get('progress', 0)),
                                        _safe_str(len(output.get('generated_screens') or []))
                                    ]
                                    state_hash = ":".join(state_components)
                                    
                                    if state_hash not in sent_states:
                                        sent_states.add(state_hash)
                                        
                                        current_response = _human_response_from_state(output)
                                        
                                        if current_response != last_response:
                                            last_response = current_response
                                            
                                            payload = _state_to_response(
                                                thread_id, 
                                                output, 
                                                chat_request.include_token_usage
                                            )
                                            
                                            payload.update({
                                                "event_source": event_name,
                                                "event_count": event_count,
                                                "processing_time": current_time - connection_start
                                            })
                                            
                                            await event_queue.put(payload)
                            
                            # Handle custom streaming events
                            elif event_type == "on_custom_event" and event_name == "llm_stream":
                                stream_data = event_data.get("data", {})
                                if stream_data.get("type") == "content_delta":
                                    chunk_data = {
                                        "thread_id": thread_id,
                                        "type": "generation_chunk",
                                        "content": stream_data.get("content", ""),
                                        "screen_id": stream_data.get("screen_id"),
                                        "timestamp": datetime.utcnow().isoformat()
                                    }
                                    await event_queue.put(chunk_data)
                            
                            # Timeout check
                            if current_time - connection_start > 300:  # 5 minutes
                                logger.warning(f"Stream timeout for thread {thread_id}")
                                await event_queue.put({
                                    "thread_id": thread_id,
                                    "type": "timeout",
                                    "message": "Processing timeout - please try again"
                                })
                                break
                        
                        # Signal completion
                        completion_data = {
                            "thread_id": thread_id,
                            "type": "stream_complete",
                            "message": "Processing completed successfully",
                            "total_events": event_count,
                            "total_time": time.time() - connection_start,
                            "timestamp": datetime.utcnow().isoformat()
                        }
                        
                        if chat_request.include_token_usage and hasattr(llm_service, 'token_tracker'):
                            completion_data["session_token_usage"] = llm_service.token_tracker.get_session_summary()
                        
                        await event_queue.put(completion_data)
                        
                    except Exception as e:
                        logger.error(f"Graph processing error: {e}", exc_info=True)
                        await event_queue.put({
                            "thread_id": thread_id,
                            "type": "error",
                            "message": f"Processing error: {str(e)}",
                            "timestamp": datetime.utcnow().isoformat()
                        })
                    finally:
                        await event_queue.put({"type": "processing_done"})
                
                try:
                    logger.info(f"Starting stream for thread {thread_id}")
                    
                    # Send initial connection confirmation
                    yield _encode_sse({
                        "thread_id": thread_id,
                        "type": "stream_started",
                        "message": "Connection established, processing request...",
                        "timestamp": datetime.utcnow().isoformat()
                    })
                    
                    # Start both tasks
                    heartbeat_task_handle = asyncio.create_task(heartbeat_task())
                    graph_task_handle = asyncio.create_task(graph_processing_task())
                    
                    processing_complete = False
                    
                    # Main event loop - handle events from both queues
                    while stream_active and not processing_complete:
                        try:
                            # Wait for events from either queue with timeout
                            done, pending = await asyncio.wait(
                                [
                                    asyncio.create_task(heartbeat_queue.get()),
                                    asyncio.create_task(event_queue.get())
                                ],
                                return_when=asyncio.FIRST_COMPLETED,
                                timeout=1.0  # Check for completion every second
                            )
                            
                            # Process completed events
                            for task in done:
                                try:
                                    event_data = await task
                                    
                                    if event_data.get("type") == "processing_done":
                                        processing_complete = True
                                        break
                                    elif event_data.get("type") == "client_disconnected":
                                        logger.warning("Client disconnected, stopping stream")
                                        stream_active = False
                                        break
                                    else:
                                        # Send the event
                                        yield _encode_sse(event_data)
                                        
                                except Exception as e:
                                    logger.error(f"Error processing event: {e}")
                            
                            # Cancel pending tasks
                            for task in pending:
                                task.cancel()
                                try:
                                    await task
                                except asyncio.CancelledError:
                                    pass
                            
                        except asyncio.TimeoutError:
                            # Timeout is normal - just continue the loop
                            continue
                    
                    logger.info(f"Stream completed for thread {thread_id}")
                    
                except Exception as e:
                    logger.error(f"Stream error for thread {thread_id}: {str(e)}", exc_info=True)
                    yield _encode_sse({
                        "thread_id": thread_id,
                        "type": "error",
                        "message": f"Processing error: {str(e)}",
                        "timestamp": datetime.utcnow().isoformat()
                    })
                
                finally:
                    # Clean up
                    stream_active = False
                    
                    # Cancel tasks
                    if 'heartbeat_task_handle' in locals():
                        heartbeat_task_handle.cancel()
                    if 'graph_task_handle' in locals():
                        graph_task_handle.cancel()
                    
                    # Wait for tasks to finish
                    for task in [t for t in [locals().get('heartbeat_task_handle'), locals().get('graph_task_handle')] if t]:
                        try:
                            await task
                        except asyncio.CancelledError:
                            pass
                    
                    # Clean up resources
                    try:
                        await _close_checkpointer_and_store(saver_cm, store_cm)
                        logger.info(f"Resources cleaned up for thread {thread_id}")
                    except Exception as cleanup_error:
                        logger.error(f"Cleanup error for thread {thread_id}: {cleanup_error}")
            
            return StreamingResponse(
                event_stream(),
                media_type="text/event-stream",
                headers={
                    "Cache-Control": "no-cache, no-transform",
                    "Connection": "keep-alive",
                    "X-Accel-Buffering": "no",
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Headers": "Cache-Control",
                },
            )
        
        else:
            # Non-streaming response (same as before)
            try:
                final_state = await asyncio.wait_for(
                    graph.ainvoke(initial_state, config=config),
                    timeout=180.0
                )
                
                await store.aput(
                    ("final_states", user_id),
                    thread_id,
                    {
                        "state": final_state,
                        "timestamp": datetime.utcnow().isoformat(),
                        "token_usage": llm_service.token_tracker.get_session_summary() if chat_request.include_token_usage else None,
                    }
                )
                
                return JSONResponse(_state_to_response(
                    thread_id, 
                    final_state, 
                    chat_request.include_token_usage
                ))
                
            finally:
                await _close_checkpointer_and_store(saver_cm, store_cm)
    
    except asyncio.TimeoutError:
        logger.error(f"Request timeout for thread {thread_id}")
        await _close_checkpointer_and_store(saver_cm, store_cm)
        raise HTTPException(
            status_code=408,
            detail={
                "error": "request_timeout", 
                "message": "Request processing timed out",
                "thread_id": thread_id,
            }
        )
    
    except Exception as e:
        logger.error(f"Chat endpoint error for thread {thread_id}: {str(e)}", exc_info=True)
        await _close_checkpointer_and_store(saver_cm, store_cm)
        
        raise HTTPException(
            status_code=500,
            detail={
                "error": "chat_processing_failed",
                "message": str(e),
                "thread_id": thread_id,
            }
        )
