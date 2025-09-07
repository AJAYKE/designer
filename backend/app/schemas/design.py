from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
import uuid

class DesignBase(BaseModel):
    title: str
    description: Optional[str] = None
    prompt_config: Dict[str, Any]
    is_public: Optional[bool] = False
    tags: Optional[List[str]] = []

class DesignCreate(DesignBase):
    pass

class DesignUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    html_code: Optional[str] = None
    css_classes: Optional[str] = None
    javascript: Optional[str] = None
    images: Optional[List[Dict[str, Any]]] = None
    status: Optional[str] = None
    is_public: Optional[bool] = None
    tags: Optional[List[str]] = None

class Design(DesignBase):
    id: uuid.UUID
    user_id: uuid.UUID
    html_code: Optional[str] = None
    css_classes: Optional[str] = None
    javascript: Optional[str] = None
    images: List[Dict[str, Any]]
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True