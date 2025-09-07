from typing import TypedDict, Optional, List, Dict, Any
from enum import Enum
from datetime import datetime

class ConversationPhase(Enum):
    INITIAL = "initial"
    PLANNING = "planning"
    AWAITING_APPROVAL = "awaiting_approval"
    GENERATING = "generating"
    COMPLETE = "complete"
    CANCELLED = "cancelled"
    ERROR = "error"

class ConversationState(TypedDict, total=False):
    # Core state
    thread_id: str
    phase: ConversationPhase
    current_message: str
    updated_at: str
    progress: int  # 0-100
    
    # Design process
    design_requirements: str
    design_plan: Dict[str, Any]
    plan_changes: List[str]
    human_feedback: Dict[str, Any]
    
    # Generation process
    generated_screens: List[Dict[str, Any]]
    generation_progress: Dict[str, Any]
    generation_summary: Dict[str, Any]
    
    # AI/LLM tracking
    routing_confidence: float
    token_usage: Dict[str, Any]
    llm_operations: List[Dict[str, Any]]
    
    # Response and communication
    last_response: str
    requires_approval: bool
    
    # Error handling
    error_message: str
    fallback_used: bool
    
    # Metadata
    user_preferences: Dict[str, Any]
    session_metadata: Dict[str, Any]
