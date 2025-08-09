"""
Content endpoints for Influenceur IA
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from pydantic import BaseModel
from sqlalchemy import func

from app.core.database import get_db
from app.models.content import Content, ContentType, ContentStatus
from app.models.influenceuse import Influenceuse

router = APIRouter()


# Pydantic models
class ContentBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    content_type: ContentType
    categories: List[str] = []
    tags: List[str] = []
    is_public: bool = False
    is_featured: bool = False


class ContentCreate(ContentBase):
    influenceuse_id: int
    prompt: Optional[str] = None
    ai_model: Optional[str] = None


class ContentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    categories: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    is_public: Optional[bool] = None
    is_featured: Optional[bool] = None
    status: Optional[ContentStatus] = None


class ContentResponse(ContentBase):
    id: int
    influenceuse_id: int
    status: str
    file_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    file_size: Optional[int] = None
    file_format: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    duration: Optional[int] = None
    views_count: int
    likes_count: int
    shares_count: int
    created_at: str
    updated_at: Optional[str] = None
    published_at: Optional[str] = None

    class Config:
        from_attributes = True


@router.get("/", response_model=List[ContentResponse])
async def get_content(
    influenceuse_id: Optional[int] = None,
    content_type: Optional[ContentType] = None,
    status: Optional[ContentStatus] = None,
    is_public: Optional[bool] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get content with filters and pagination
    """
    query = db.query(Content)
    
    if influenceuse_id:
        query = query.filter(Content.influenceuse_id == influenceuse_id)
    
    if content_type:
        query = query.filter(Content.content_type == content_type)
    
    if status:
        query = query.filter(Content.status == status)
    
    if is_public is not None:
        query = query.filter(Content.is_public == is_public)
    
    content_list = query.offset(skip).limit(limit).all()
    return content_list


@router.get("/{content_id}", response_model=ContentResponse)
async def get_content_by_id(content_id: int, db: Session = Depends(get_db)):
    """
    Get content by ID
    """
    content = db.query(Content).filter(Content.id == content_id).first()
    if not content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content not found"
        )
    return content


@router.post("/", response_model=ContentResponse)
async def create_content(
    content: ContentCreate,
    db: Session = Depends(get_db)
):
    """
    Create new content
    """
    # Check if influenceuse exists
    influenceuse = db.query(Influenceuse).filter(
        Influenceuse.id == content.influenceuse_id
    ).first()
    
    if not influenceuse:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Influenceuse not found"
        )
    
    # Create new content
    db_content = Content(**content.dict())
    db.add(db_content)
    db.commit()
    db.refresh(db_content)
    
    return db_content


@router.put("/{content_id}", response_model=ContentResponse)
async def update_content(
    content_id: int,
    content_update: ContentUpdate,
    db: Session = Depends(get_db)
):
    """
    Update content
    """
    db_content = db.query(Content).filter(Content.id == content_id).first()
    if not db_content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content not found"
        )
    
    # Update fields
    update_data = content_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_content, field, value)
    
    db.commit()
    db.refresh(db_content)
    
    return db_content


@router.delete("/{content_id}")
async def delete_content(content_id: int, db: Session = Depends(get_db)):
    """
    Delete content
    """
    db_content = db.query(Content).filter(Content.id == content_id).first()
    if not db_content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content not found"
        )
    
    db.delete(db_content)
    db.commit()
    
    return {"message": "Content deleted successfully"}


@router.post("/{content_id}/publish")
async def publish_content(content_id: int, db: Session = Depends(get_db)):
    """
    Publish content
    """
    db_content = db.query(Content).filter(Content.id == content_id).first()
    if not db_content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content not found"
        )
    
    db_content.status = ContentStatus.PUBLISHED
    db_content.is_public = True
    db_content.published_at = func.now()
    
    db.commit()
    db.refresh(db_content)
    
    return {"message": "Content published successfully"}


@router.post("/{content_id}/archive")
async def archive_content(content_id: int, db: Session = Depends(get_db)):
    """
    Archive content
    """
    db_content = db.query(Content).filter(Content.id == content_id).first()
    if not db_content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content not found"
        )
    
    db_content.status = ContentStatus.ARCHIVED
    db_content.is_public = False
    
    db.commit()
    db.refresh(db_content)
    
    return {"message": "Content archived successfully"}


@router.get("/{content_id}/stats")
async def get_content_stats(content_id: int, db: Session = Depends(get_db)):
    """
    Get content statistics
    """
    content = db.query(Content).filter(Content.id == content_id).first()
    if not content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content not found"
        )
    
    return {
        "id": content.id,
        "title": content.title,
        "views_count": content.views_count,
        "likes_count": content.likes_count,
        "shares_count": content.shares_count,
        "status": content.status,
        "is_public": content.is_public,
        "is_featured": content.is_featured,
        "created_at": content.created_at,
        "published_at": content.published_at,
    }
