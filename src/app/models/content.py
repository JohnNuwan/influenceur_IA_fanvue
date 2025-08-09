"""
Content model for Influenceur IA
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, JSON, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.core.database import Base


class ContentType(str, enum.Enum):
    """Content types"""
    IMAGE = "image"
    VIDEO = "video"
    TEXT = "text"
    AUDIO = "audio"


class ContentStatus(str, enum.Enum):
    """Content status"""
    DRAFT = "draft"
    GENERATED = "generated"
    PUBLISHED = "published"
    ARCHIVED = "archived"
    FAILED = "failed"


class Content(Base):
    """Content model"""
    __tablename__ = "content"

    id = Column(Integer, primary_key=True, index=True)
    influenceuse_id = Column(Integer, ForeignKey("influenceuses.id"), nullable=False)
    
    # Content info
    title = Column(String(255))
    description = Column(Text)
    content_type = Column(Enum(ContentType), nullable=False)
    status = Column(Enum(ContentStatus), default=ContentStatus.DRAFT)
    
    # File info
    file_url = Column(String(500))
    file_size = Column(Integer)
    file_format = Column(String(50))
    thumbnail_url = Column(String(500))
    
    # AI generation info
    prompt = Column(Text)
    ai_model = Column(String(100))  # "stable-diffusion", "midjourney", "ollama"
    generation_params = Column(JSON)  # Model parameters used
    generation_time = Column(Integer)  # Time in seconds
    
    # Categories and tags
    categories = Column(JSON, default=list)  # ["lingerie", "feet", "nude"]
    tags = Column(JSON, default=list)
    
    # Metadata
    width = Column(Integer)
    height = Column(Integer)
    duration = Column(Integer)  # For videos, in seconds
    
    # Publishing info
    is_public = Column(Boolean, default=False)
    is_featured = Column(Boolean, default=False)
    published_at = Column(DateTime(timezone=True))
    
    # Analytics
    views_count = Column(Integer, default=0)
    likes_count = Column(Integer, default=0)
    shares_count = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    influenceuse = relationship("Influenceuse", back_populates="content")
    
    def __repr__(self):
        return f"<Content(id={self.id}, title='{self.title}', type='{self.content_type}')>"
