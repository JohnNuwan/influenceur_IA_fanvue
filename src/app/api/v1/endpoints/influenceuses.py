"""
Influenceuse endpoints
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.core.database import get_db
from app.models.influenceuse import Influenceuse
from app.models.user import User

router = APIRouter()


# Pydantic models
class InfluenceuseBase(BaseModel):
    stage_name: str
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    cover_image_url: Optional[str] = None
    content_categories: List[str] = []
    content_style: Optional[str] = None
    subscription_price: float = 0.0
    tips_enabled: bool = True
    custom_content_enabled: bool = True


class InfluenceuseCreate(InfluenceuseBase):
    user_id: int


class InfluenceuseUpdate(BaseModel):
    stage_name: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    cover_image_url: Optional[str] = None
    content_categories: Optional[List[str]] = None
    content_style: Optional[str] = None
    subscription_price: Optional[float] = None
    tips_enabled: Optional[bool] = None
    custom_content_enabled: Optional[bool] = None
    is_active: Optional[bool] = None
    is_verified: Optional[bool] = None
    is_featured: Optional[bool] = None


class InfluenceuseResponse(InfluenceuseBase):
    id: int
    user_id: int
    followers_count: int
    following_count: int
    posts_count: int
    is_active: bool
    is_verified: bool
    is_featured: bool
    auto_posting_enabled: bool
    chatbot_enabled: bool
    analytics_enabled: bool
    created_at: str
    updated_at: Optional[str] = None
    last_activity: Optional[str] = None

    class Config:
        from_attributes = True


@router.get("/", response_model=List[InfluenceuseResponse])
async def get_influenceuses(
    skip: int = 0,
    limit: int = 100,
    is_active: Optional[bool] = None,
    is_verified: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """
    Get all influenceuses with filters and pagination
    """
    query = db.query(Influenceuse)
    
    if is_active is not None:
        query = query.filter(Influenceuse.is_active == is_active)
    
    if is_verified is not None:
        query = query.filter(Influenceuse.is_verified == is_verified)
    
    influenceuses = query.offset(skip).limit(limit).all()
    return influenceuses


@router.get("/{influenceuse_id}", response_model=InfluenceuseResponse)
async def get_influenceuse(influenceuse_id: int, db: Session = Depends(get_db)):
    """
    Get influenceuse by ID
    """
    influenceuse = db.query(Influenceuse).filter(Influenceuse.id == influenceuse_id).first()
    if not influenceuse:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Influenceuse not found"
        )
    return influenceuse


@router.post("/", response_model=InfluenceuseResponse)
async def create_influenceuse(
    influenceuse: InfluenceuseCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new influenceuse
    """
    # Check if user exists
    user = db.query(User).filter(User.id == influenceuse.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Check if influenceuse already exists for this user
    existing_influenceuse = db.query(Influenceuse).filter(
        Influenceuse.user_id == influenceuse.user_id
    ).first()
    
    if existing_influenceuse:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Influenceuse already exists for this user"
        )
    
    # Create new influenceuse
    db_influenceuse = Influenceuse(**influenceuse.dict())
    db.add(db_influenceuse)
    db.commit()
    db.refresh(db_influenceuse)
    
    return db_influenceuse


@router.put("/{influenceuse_id}", response_model=InfluenceuseResponse)
async def update_influenceuse(
    influenceuse_id: int,
    influenceuse_update: InfluenceuseUpdate,
    db: Session = Depends(get_db)
):
    """
    Update influenceuse
    """
    db_influenceuse = db.query(Influenceuse).filter(Influenceuse.id == influenceuse_id).first()
    if not db_influenceuse:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Influenceuse not found"
        )
    
    # Update fields
    update_data = influenceuse_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_influenceuse, field, value)
    
    db.commit()
    db.refresh(db_influenceuse)
    
    return db_influenceuse


@router.delete("/{influenceuse_id}")
async def delete_influenceuse(influenceuse_id: int, db: Session = Depends(get_db)):
    """
    Delete influenceuse
    """
    db_influenceuse = db.query(Influenceuse).filter(Influenceuse.id == influenceuse_id).first()
    if not db_influenceuse:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Influenceuse not found"
        )
    
    db.delete(db_influenceuse)
    db.commit()
    
    return {"message": "Influenceuse deleted successfully"}


@router.get("/{influenceuse_id}/stats")
async def get_influenceuse_stats(influenceuse_id: int, db: Session = Depends(get_db)):
    """
    Get influenceuse statistics
    """
    influenceuse = db.query(Influenceuse).filter(Influenceuse.id == influenceuse_id).first()
    if not influenceuse:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Influenceuse not found"
        )
    
    # Here you would typically calculate more detailed statistics
    # For now, we'll return basic stats
    return {
        "id": influenceuse.id,
        "stage_name": influenceuse.stage_name,
        "followers_count": influenceuse.followers_count,
        "following_count": influenceuse.following_count,
        "posts_count": influenceuse.posts_count,
        "subscription_price": influenceuse.subscription_price,
        "is_active": influenceuse.is_active,
        "is_verified": influenceuse.is_verified,
        "is_featured": influenceuse.is_featured,
    }
