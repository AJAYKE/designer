from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import StreamingResponse
import json
import asyncio
from typing import AsyncGenerator, Dict, Any
from uuid import uuid4
from datetime import datetime

from app.models.api_models import (
    GenerateRequest,
    PlanApprovalRequest, 
    DesignPlanResponse,
    StreamingResponse as StreamingResponseModel,
    UserUsageResponse,
    EditScreenRequest
)
from app.models.design_state import DesignState, GenerationPhase
from app.middleware.auth_middleware import get_current_user
from app.middleware.rate_limit_middleware import request_rate_limit, token_rate_limit_check
from app.services.token_tracker import TokenTracker
from app.services.token_estimator import TokenEstimator
from app.services.s3_service import S3Service

router = APIRouter()

@router.post("/generate/plan", response_model=DesignPlanResponse)
@request_rate_limit(calls=5, period=60)  # 5 plans per minute
async def generate_design_plan(
    request: GenerateRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
    fastapi_request: Request = None
):
    """
    Phase 1: Generate design plan for user approval
    """
    
    try:
        user_id = current_user["user_id"]
        thread_id = request.thread_id or str(uuid4())
        message_id = request.message_id or str(uuid4())
        
        # Estimate tokens for planning
        token_estimator = TokenEstimator()
        estimated_planning_tokens = 500  # Planning is lightweight
        
        # Check token rate limits
        await token_rate_limit_check(user_id, estimated_planning_tokens)
        
        # Initialize enhanced design state
        initial_state: DesignState = {
            "thread_id": thread_id,
            "message_id": message_id,
            "user_id": user_id,
            "prompt_config": request.config.dict(),
            "design_plan": None,
            "plan_approved": False,
            "current_screen_index": 0,
            "generated_screens": [],
            "phase": GenerationPhase.PLANNING,
            "overall_progress": 0,
            "current_screen_progress": 0,
            "total_tokens_used": 0,
            "estimated_tokens_remaining": 0,
            "error_message": None,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }
        
        # Get the enhanced agent
        agent, checkpointer, store = await fastapi_request.app.state.design_agent
        
        # Run only the planning phase
        config = {
            "configurable": {
                "thread_id": thread_id,
                "user_id": user_id,
            }
        }
        
        # Execute planning agent only
        result_state = None
        async for chunk in agent.astream(
            initial_state,
            config,
            stream_mode="values"
        ):
            result_state = chunk
            # Stop after planning phase
            if result_state.get("phase") == GenerationPhase.PLAN_REVIEW:
                break
        
        if not result_state or not result_state.get("design_plan"):
            raise HTTPException(status_code=500, detail="Failed to generate design plan")
        
        design_plan = result_state["design_plan"]
        
        # Calculate estimated cost (rough estimate: $0.002 per 1K tokens)
        estimated_cost = (design_plan.total_estimated_tokens / 1000) * 0.002
        
        return DesignPlanResponse(
            thread_id=thread_id,
            message_id=message_id,
            plan=design_plan,
            estimated_tokens=design_plan.total_estimated_tokens,
            estimated_cost_usd=round(estimated_cost, 4)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Plan generation failed: {str(e)}")

@router.post("/generate/approve")
async def approve_design_plan(
    request: PlanApprovalRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
    fastapi_request: Request = None
):
    """
    Phase 2: Approve plan and trigger generation
    """
    
    try:
        user_id = current_user["user_id"]
        
        if not request.approved:
            return {"message": "Plan rejected. Please create a new plan."}
        
        # Get the enhanced agent
        agent, checkpointer, store = await fastapi_request.app.state.design_agent
        
        # Update the state to approve the plan
        config = {
            "configurable": {
                "thread_id": request.thread_id,
                "user_id": user_id,
            }
        }
        
        # Get current state
        current_state = await checkpointer.aget(config)
        if not current_state:
            raise HTTPException(status_code=404, detail="Design plan not found")
        
        # Update approval status
        updated_state = current_state.copy()
        updated_state["plan_approved"] = True
        updated_state["phase"] = GenerationPhase.GENERATING
        
        # Save updated state
        await checkpointer.aput(config, updated_state)
        
        return {"message": "Plan approved. Generation will begin.", "thread_id": request.thread_id}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Plan approval failed: {str(e)}")

@router.post("/generate/stream")
async def stream_design_generation(
    request: GenerateRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
    fastapi_request: Request = None
):
    """
    Stream the complete design generation process
    """
    
    async def generation_stream() -> AsyncGenerator[str, None]:
        try:
            user_id = current_user["user_id"]
            thread_id = request.thread_id or str(uuid4())
            message_id = request.message_id or str(uuid4())
            
            # Get the enhanced agent
            agent, checkpointer, store = await fastapi_request.app.state.design_agent
            
            config = {
                "configurable": {
                    "thread_id": thread_id,
                    "user_id": user_id,
                }
            }
            
            # Check if we have an existing state (approved plan)
            existing_state = await checkpointer.aget(config)
            
            if existing_state and existing_state.get("plan_approved"):
                # Continue from approved plan
                initial_state = existing_state
            else:
                # Start fresh (this shouldn't happen in production)
                raise HTTPException(status_code=400, detail="Plan must be approved first")
            
            # Stream the generation process
            async for chunk in agent.astream(
                initial_state,
                config,
                stream_mode="values"
            ):
                # Extract state from chunk
                current_state = chunk
                
                # Create streaming response
                stream_response = StreamingResponseModel(
                    thread_id=thread_id,
                    message_id=message_id,
                    phase=current_state.get("phase", GenerationPhase.GENERATING),
                    overall_progress=current_state.get("overall_progress", 0),
                    current_screen_progress=current_state.get("current_screen_progress", 0),
                    error=current_state.get("error_message")
                )
                
                # Add screen-specific data when available
                if current_state.get("generated_screens"):
                    latest_screen = current_state["generated_screens"][-1]
                    
                    # Stream metadata first
                    metadata_response = stream_response.copy()
                    metadata_response.data = {
                        "type": "screen_metadata",
                        "screen_id": latest_screen.screen_id,
                        "screen_type": latest_screen.metadata.screen_type,
                        "title": latest_screen.metadata.title,
                        "description": latest_screen.metadata.description
                    }
                    
                    yield f"data: {json.dumps(metadata_response.dict(), default=str)}\\n\\n"
                    
                    # Then stream the HTML content
                    html_response = stream_response.copy()
                    html_response.data = {
                        "type": "screen_content",
                        "screen_id": latest_screen.screen_id,
                        "html": latest_screen.html_code,
                        "css": latest_screen.css_classes,
                        "javascript": latest_screen.javascript,
                        "s3_url": latest_screen.s3_url
                    }
                    
                    yield f"data: {json.dumps(html_response.dict(), default=str)}\\n\\n"
                else:
                    # Regular progress update
                    yield f"data: {json.dumps(stream_response.dict(), default=str)}\\n\\n"
                
                # Small delay to prevent overwhelming
                await asyncio.sleep(0.1)
                
                # Break if complete or error
                if current_state.get("phase") in [GenerationPhase.COMPLETE, GenerationPhase.ERROR]:
                    break
            
            # Final completion message
            completion_response = StreamingResponseModel(
                thread_id=thread_id,
                message_id=message_id,
                phase=GenerationPhase.COMPLETE,
                overall_progress=100,
                current_screen_progress=100,
                data={"type": "generation_complete", "total_screens": len(current_state.get("generated_screens", []))}
            )
            
            yield f"data: {json.dumps(completion_response.dict(), default=str)}\\n\\n"
            
        except Exception as e:
            error_response = StreamingResponseModel(
                thread_id=thread_id if 'thread_id' in locals() else "unknown",
                message_id=message_id if 'message_id' in locals() else "unknown",
                phase=GenerationPhase.ERROR,
                overall_progress=0,
                current_screen_progress=0,
                error=str(e)
            )
            yield f"data: {json.dumps(error_response.dict(), default=str)}\\n\\n"
    
    return StreamingResponse(
        generation_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*"
        }
    )

@router.get("/design/{thread_id}")
async def get_design_result(
    thread_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user),
    fastapi_request: Request = None
):
    """Get the complete design result for a thread"""
    
    try:
        user_id = current_user["user_id"]
        
        # Get the enhanced agent
        agent, checkpointer, store = await fastapi_request.app.state.design_agent
        
        config = {
            "configurable": {
                "thread_id": thread_id,
                "user_id": user_id,
            }
        }
        
        # Get current state
        state = await checkpointer.aget(config)
        if not state:
            raise HTTPException(status_code=404, detail="Design not found")
        
        return {
            "thread_id": thread_id,
            "phase": state.get("phase"),
            "overall_progress": state.get("overall_progress"),
            "design_plan": state.get("design_plan"),
            "generated_screens": state.get("generated_screens", []),
            "total_tokens_used": state.get("total_tokens_used", 0),
            "created_at": state.get("created_at"),
            "updated_at": state.get("updated_at")
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve design: {str(e)}")

@router.post("/design/edit")
async def save_screen_edit(
    request: EditScreenRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Save user edits to a generated screen"""
    
    try:
        user_id = current_user["user_id"]
        
        # Store the edit in S3
        s3_service = S3Service()
        edit_url = await s3_service.store_user_edit(
            thread_id=request.thread_id,
            message_id=request.message_id,
            screen_id=request.screen_id,
            edited_html=request.edited_html,
            user_id=user_id
        )
        
        if not edit_url:
            raise HTTPException(status_code=500, detail="Failed to save edit")
        
        return {
            "message": "Edit saved successfully",
            "edit_url": edit_url,
            "saved_at": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save edit: {str(e)}")

@router.get("/user/usage", response_model=UserUsageResponse)
async def get_user_usage(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get current user's usage statistics"""
    
    try:
        user_id = current_user["user_id"]
        
        # Get token usage
        token_tracker = TokenTracker()
        usage = await token_tracker.get_user_token_usage(user_id)
        
        # Get request count (simplified)
        import redis.asyncio as redis
        redis_client = redis.from_url(settings.REDIS_URL)
        
        minute_key = f"requests:{user_id}:*"
        requests_this_minute = 0
        try:
            keys = await redis_client.keys(minute_key)
            if keys:
                values = await redis_client.mget(keys)
                requests_this_minute = sum(int(v) for v in values if v)
        except:
            pass
        
        return UserUsageResponse(
            user_id=user_id,
            hourly_tokens_used=usage["hourly_tokens"],
            daily_tokens_used=usage["daily_tokens"],
            hourly_tokens_remaining=max(0, usage["hourly_limit"] - usage["hourly_tokens"]),
            daily_tokens_remaining=max(0, usage["daily_limit"] - usage["daily_tokens"]),
            requests_this_minute=requests_this_minute,
            total_designs_generated=0  # TODO: Add to tracking
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get usage: {str(e)}")

@router.delete("/design/{thread_id}")
async def delete_design(
    thread_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user),
    fastapi_request: Request = None
):
    """Delete a design and its associated data"""
    
    try:
        user_id = current_user["user_id"]
        
        # Get the enhanced agent
        agent, checkpointer, store = await fastapi_request.app.state.design_agent
        
        config = {
            "configurable": {
                "thread_id": thread_id,
                "user_id": user_id,
            }
        }
        
        # Delete from checkpointer
        await checkpointer.adelete(config)
        
        # TODO: Delete from S3 as well
        
        return {"message": f"Design {thread_id} deleted successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Deletion failed: {str(e)}")

@router.get("/designs")
async def list_user_designs(
    limit: int = 20,
    offset: int = 0,
    current_user: Dict[str, Any] = Depends(get_current_user),
    fastapi_request: Request = None
):
    """List user's designs with pagination"""
    
    try:
        user_id = current_user["user_id"]
        
        # TODO: Implement proper pagination with checkpointer
        # For now, return empty list
        
        return {
            "designs": [],
            "total": 0,
            "limit": limit,
            "offset": offset,
            "user_id": user_id
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list designs: {str(e)}")

