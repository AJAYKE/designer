from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, Any
from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.user import User
from app.schemas.user import User as UserSchema, UserCreate, UserUpdate
from app.services.user_service import UserService

router = APIRouter()

@router.get("/me")
async def get_me(current_user = Depends(get_current_user)):
    """Get current user info - requires authentication"""
    return {
        "message": "Authentication successful!",
        "user": current_user
    }

@router.put("/me", response_model=UserSchema)
async def update_user_profile(
    user_update: UserUpdate,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update current user profile"""
    user_service = UserService(db)
    
    user = user_service.get_user_by_clerk_id(current_user['id'])
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    updated_user = user_service.update_user(user.id, user_update)
    return updated_user

@router.delete("/me")
async def delete_user_account(
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete current user account"""
    user_service = UserService(db)
    
    user = user_service.get_user_by_clerk_id(current_user['id'])
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Soft delete or hard delete based on requirements
    user_service.delete_user(user.id)
    
    return {"message": "Account deleted successfully"}

