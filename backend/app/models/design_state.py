from typing import TypedDict, Optional, List, Dict, Any
from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class UnsplashImage(BaseModel):
    id: str
    url: str
    alt_description: str
    width: int
    height: int
    author: str


class GenerationPhase(str, Enum):
    PLANNING = "planning"
    PLAN_REVIEW = "plan_review" 
    GENERATING = "generating"
    COMPLETE = "complete"
    ERROR = "error"

class ScreenType(str, Enum):
    LANDING = "landing"
    DASHBOARD = "dashboard"
    LOGIN = "login"
    PROFILE = "profile"
    SETTINGS = "settings"
    MOBILE_APP = "mobile_app"

class DesignMetadata(BaseModel):
    screen_id: str
    screen_type: ScreenType
    title: str
    description: str
    estimated_tokens: int
    generation_order: int

class GeneratedScreen(BaseModel):
    screen_id: str
    metadata: DesignMetadata
    html_code: str
    css_classes: str
    javascript: str
    images: List[Dict[str, Any]]
    s3_url: Optional[str] = None
    generation_time_ms: int
    token_usage: int

class DesignPlan(BaseModel):
    plan_id: str
    screens: List[DesignMetadata]
    total_estimated_tokens: int
    generation_strategy: str
    user_context: str
    created_at: datetime

class DesignState(TypedDict):
    # User and conversation tracking
    thread_id: str
    message_id: str
    user_id: Optional[str]
    
    # Input configuration
    prompt_config: Dict[str, Any]
    
    # Planning phase
    design_plan: Optional[DesignPlan]
    plan_approved: bool
    
    # Generation phase
    current_screen_index: int
    generated_screens: List[GeneratedScreen]
    
    # Progress tracking
    phase: GenerationPhase
    overall_progress: int  # 0-100
    current_screen_progress: int  # 0-100
    
    # Token and usage tracking
    total_tokens_used: int
    estimated_tokens_remaining: int
    
    # Error handling
    error_message: Optional[str]
    
    # Timestamps
    created_at: str
    updated_at: str

