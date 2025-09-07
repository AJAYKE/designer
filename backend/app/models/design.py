from sqlalchemy import Column, String, DateTime, Text, JSON, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from app.core.database import Base

class Design(Base):
    __tablename__ = "designs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    prompt_config = Column(JSON, nullable=False)
    html_code = Column(Text, nullable=True)
    css_classes = Column(Text, nullable=True)
    javascript = Column(Text, nullable=True)
    images = Column(JSON, default=[])
    status = Column(String, default="draft")  # draft, completed, published
    is_public = Column(Boolean, default=False)
    tags = Column(JSON, default=[])
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationship
    user = relationship("User", backref="designs")


