from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Dict, Any, List, Optional
from app.core.database import get_db
from app.core.auth import get_current_user, require_premium
from app.models.user import User
from app.schemas.design import Design as DesignSchema, DesignCreate, DesignUpdate
from app.services.design_service import DesignService
from app.services.user_service import UserService
import uuid

router = APIRouter()

@router.post("/", response_model=DesignSchema)
async def create_design(
    design_create: DesignCreate,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new design"""
    user_service = UserService(db)
    design_service = DesignService(db)
    
    # Get or create user
    user = user_service.get_or_create_user(
        clerk_id=current_user['id'],
        email=current_user['email']
    )
    
    # Create design
    design = design_service.create_design(user.id, design_create)
    return design

@router.get("/", response_model=List[DesignSchema])
async def get_user_designs(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    status: Optional[str] = Query(None),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user's designs"""
    user_service = UserService(db)
    design_service = DesignService(db)
    
    user = user_service.get_user_by_clerk_id(current_user['id'])
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    designs = design_service.get_user_designs(
        user_id=user.id,
        skip=skip,
        limit=limit,
        status=status
    )
    return designs

@router.get("/{design_id}", response_model=DesignSchema)
async def get_design(
    design_id: uuid.UUID,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific design"""
    design_service = DesignService(db)
    user_service = UserService(db)
    
    user = user_service.get_user_by_clerk_id(current_user['id'])
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    design = design_service.get_design(design_id)
    if not design:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Design not found"
        )
    
    # Check if user owns the design or if it's public
    if design.user_id != user.id and not design.is_public:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    return design

@router.put("/{design_id}", response_model=DesignSchema)
async def update_design(
    design_id: uuid.UUID,
    design_update: DesignUpdate,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a design"""
    design_service = DesignService(db)
    user_service = UserService(db)
    
    user = user_service.get_user_by_clerk_id(current_user['id'])
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    design = design_service.get_design(design_id)
    if not design:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Design not found"
        )
    
    # Check ownership
    if design.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    updated_design = design_service.update_design(design_id, design_update)
    return updated_design

@router.delete("/{design_id}")
async def delete_design(
    design_id: uuid.UUID,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a design"""
    design_service = DesignService(db)
    user_service = UserService(db)
    
    user = user_service.get_user_by_clerk_id(current_user['id'])
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    design = design_service.get_design(design_id)
    if not design:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Design not found"
        )
    
    # Check ownership
    if design.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    design_service.delete_design(design_id)
    return {"message": "Design deleted successfully"}

# Premium features
@router.post("/{design_id}/export/figma")
async def export_to_figma(
    design_id: uuid.UUID,
    current_user: Dict[str, Any] = Depends(require_premium),
    db: Session = Depends(get_db)
):
    """Export design to Figma (Premium feature)"""
    # Implementation for Figma export
    return {"message": "Figma export initiated", "design_id": design_id}