from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from app.models.prompt_config import PromptConfig
from app.models.design_state import GeneratedScreen, DesignPlan, GenerationPhase

class GenerateRequest(BaseModel):
    config: PromptConfig
    thread_id: Optional[str] = None
    message_id: Optional[str] = None

class PlanApprovalRequest(BaseModel):
    thread_id: str
    message_id: str
    approved: bool
    modifications: Optional[List[str]] = []

class StreamingResponse(BaseModel):
    thread_id: str
    message_id: str
    phase: GenerationPhase
    overall_progress: int
    current_screen_progress: int
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

class DesignPlanResponse(BaseModel):
    thread_id: str
    message_id: str
    plan: DesignPlan
    estimated_tokens: int
    estimated_cost_usd: float

class GeneratedScreenResponse(BaseModel):
    screen: GeneratedScreen
    s3_url: str
    metadata: Dict[str, Any]

class UserUsageResponse(BaseModel):
    user_id: str
    hourly_tokens_used: int
    daily_tokens_used: int
    hourly_tokens_remaining: int
    daily_tokens_remaining: int
    requests_this_minute: int
    total_designs_generated: int

class EditScreenRequest(BaseModel):
    thread_id: str
    message_id: str
    screen_id: str
    edited_html: str