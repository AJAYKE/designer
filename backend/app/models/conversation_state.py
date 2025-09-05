from typing import TypedDict, Optional, List, Dict, Any
from enum import Enum
from datetime import datetime

class ConversationPhase(str, Enum):
    INITIAL = "initial"
    PLANNING = "planning"
    AWAITING_APPROVAL = "awaiting_approval" 
    PROCESSING_FEEDBACK = "processing_feedback"
    GENERATING = "generating"
    MODIFYING = "modifying"
    CONVERSING = "conversing"
    COMPLETE = "complete"
    CANCELLED = "cancelled"
    ERROR = "error"

class ConversationState(TypedDict):
    # Core conversation tracking
    thread_id: str
    user_id: str
    phase: ConversationPhase
    
    # Message handling
    current_message: str
    message_history: List[Dict[str, Any]]
    
    # Design planning
    design_requirements: Optional[str]
    design_plan: Optional[Dict[str, Any]]
    plan_approved: bool
    plan_modifications: List[str]
    
    # Human feedback
    human_feedback: Optional[Dict[str, Any]]
    
    # Generation
    generated_screens: List[Dict[str, Any]]
    generation_progress: Dict[str, Any]
    
    # Model selection
    selected_model: str
    
    # Context and memory
    conversation_context: Dict[str, Any]
    
    # Timestamps
    created_at: str
    updated_at: str