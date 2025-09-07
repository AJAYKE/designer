from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.design import Design
from app.schemas.design import DesignCreate, DesignUpdate
import uuid

class DesignService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_design(self, design_id: uuid.UUID) -> Optional[Design]:
        """Get design by ID"""
        return self.db.query(Design).filter(Design.id == design_id).first()
    
    def get_user_designs(
        self, 
        user_id: uuid.UUID, 
        skip: int = 0, 
        limit: int = 100,
        status: Optional[str] = None
    ) -> List[Design]:
        """Get designs for a user"""
        query = self.db.query(Design).filter(Design.user_id == user_id)
        
        if status:
            query = query.filter(Design.status == status)
        
        return query.offset(skip).limit(limit).all()
    
    def get_public_designs(self, skip: int = 0, limit: int = 100) -> List[Design]:
        """Get public designs"""
        return (
            self.db.query(Design)
            .filter(Design.is_public == True)
            .filter(Design.status == "published")
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def create_design(self, user_id: uuid.UUID, design_create: DesignCreate) -> Design:
        """Create a new design"""
        db_design = Design(
            user_id=user_id,
            title=design_create.title,
            description=design_create.description,
            prompt_config=design_create.prompt_config,
            is_public=design_create.is_public,
            tags=design_create.tags
        )
        self.db.add(db_design)
        self.db.commit()
        self.db.refresh(db_design)
        return db_design
    
    def update_design(self, design_id: uuid.UUID, design_update: DesignUpdate) -> Design:
        """Update design"""
        design = self.get_design(design_id)
        if not design:
            raise ValueError("Design not found")
        
        update_data = design_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(design, field, value)
        
        self.db.commit()
        self.db.refresh(design)
        return design
    
    def delete_design(self, design_id: uuid.UUID) -> bool:
        """Delete design"""
        design = self.get_design(design_id)
        if not design:
            return False
        
        self.db.delete(design)
        self.db.commit()
        return True
    
    def count_user_designs(self, user_id: uuid.UUID) -> int:
        """Count user's designs"""
        return self.db.query(Design).filter(Design.user_id == user_id).count()
    
    def search_designs(
        self, 
        query: str, 
        user_id: Optional[uuid.UUID] = None,
        is_public: bool = True,
        skip: int = 0, 
        limit: int = 100
    ) -> List[Design]:
        """Search designs by title or description"""
        db_query = self.db.query(Design)
        
        if user_id:
            db_query = db_query.filter(Design.user_id == user_id)
        elif is_public:
            db_query = db_query.filter(Design.is_public == True)
        
        db_query = db_query.filter(
            (Design.title.ilike(f"%{query}%")) | 
            (Design.description.ilike(f"%{query}%"))
        )
        
        return db_query.offset(skip).limit(limit).all()