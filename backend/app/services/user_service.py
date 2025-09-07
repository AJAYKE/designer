from sqlalchemy.orm import Session
from typing import Optional
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
import uuid

class UserService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_user_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        """Get user by ID"""
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_user_by_clerk_id(self, clerk_id: str) -> Optional[User]:
        """Get user by Clerk ID"""
        return self.db.query(User).filter(User.clerk_id == clerk_id).first()
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        return self.db.query(User).filter(User.email == email).first()
    
    def create_user(self, user_create: UserCreate) -> User:
        """Create a new user"""
        db_user = User(
            clerk_id=user_create.clerk_id,
            email=user_create.email,
            first_name=user_create.first_name,
            last_name=user_create.last_name,
            image_url=user_create.image_url
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def get_or_create_user(
        self, 
        clerk_id: str, 
        email: str, 
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        image_url: Optional[str] = None
    ) -> User:
        """Get existing user or create new one"""
        user = self.get_user_by_clerk_id(clerk_id)
        if user:
            # Update user info if changed
            updated = False
            if user.email != email:
                user.email = email
                updated = True
            if user.first_name != first_name:
                user.first_name = first_name
                updated = True
            if user.last_name != last_name:
                user.last_name = last_name
                updated = True
            if user.image_url != image_url:
                user.image_url = image_url
                updated = True
            
            if updated:
                self.db.commit()
                self.db.refresh(user)
            
            return user
        
        # Create new user
        user_create = UserCreate(
            clerk_id=clerk_id,
            email=email,
            first_name=first_name,
            last_name=last_name,
            image_url=image_url
        )
        return self.create_user(user_create)
    
    def update_user(self, user_id: uuid.UUID, user_update: UserUpdate) -> User:
        """Update user"""
        user = self.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        
        update_data = user_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)
        
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def delete_user(self, user_id: uuid.UUID) -> bool:
        """Delete user (soft delete)"""
        user = self.get_user_by_id(user_id)
        if not user:
            return False
        
        user.is_active = False
        self.db.commit()
        return True