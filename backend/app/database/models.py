from sqlalchemy import Column, Integer, String, DateTime, Text, JSON, Boolean, Float
from sqlalchemy.sql import func
from app.core.database import Base

class Design(Base):
    """Enhanced design model with more tracking"""
    __tablename__ = "designs"
    
    id = Column(Integer, primary_key=True, index=True)
    thread_id = Column(String, unique=True, index=True, nullable=False)
    message_id = Column(String, index=True, nullable=True)
    
    # User tracking
    user_id = Column(String, index=True, nullable=False)
    user_email = Column(String, nullable=True)
    
    # Design content
    design_plan = Column(JSON, nullable=True)
    generated_screens = Column(JSON, nullable=True)  # List of GeneratedScreen objects
    
    # Configuration and metadata
    prompt_config = Column(JSON, nullable=False)
    
    # Status tracking
    phase = Column(String, nullable=False, default="planning")
    overall_progress = Column(Integer, nullable=False, default=0)
    plan_approved = Column(Boolean, default=False)
    
    # Usage tracking
    total_tokens_used = Column(Integer, default=0)
    estimated_cost_usd = Column(Float, default=0.0)
    generation_time_ms = Column(Integer, nullable=True)
    
    # S3 storage
    s3_base_url = Column(String, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Error handling
    error_message = Column(Text, nullable=True)
    
    def to_dict(self):
        return {
            "id": self.id,
            "thread_id": self.thread_id,
            "message_id": self.message_id,
            "user_id": self.user_id,
            "user_email": self.user_email,
            "design_plan": self.design_plan,
            "generated_screens": self.generated_screens,
            "prompt_config": self.prompt_config,
            "phase": self.phase,
            "overall_progress": self.overall_progress,
            "plan_approved": self.plan_approved,
            "total_tokens_used": self.total_tokens_used,
            "estimated_cost_usd": self.estimated_cost_usd,
            "generation_time_ms": self.generation_time_ms,
            "s3_base_url": self.s3_base_url,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "error_message": self.error_message
        }

class TokenUsage(Base):
    """Track token usage for billing and analytics"""
    __tablename__ = "token_usage"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True, nullable=False)
    thread_id = Column(String, index=True, nullable=True)
    
    # Token details
    prompt_tokens = Column(Integer, nullable=False)
    completion_tokens = Column(Integer, nullable=False) 
    total_tokens = Column(Integer, nullable=False)
    
    # Operation details
    model = Column(String, nullable=False)
    operation_type = Column(String, nullable=False)  # planning, generation_landing, etc.
    duration_ms = Column(Integer, nullable=True)
    
    # Cost tracking
    cost_usd = Column(Float, default=0.0)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())