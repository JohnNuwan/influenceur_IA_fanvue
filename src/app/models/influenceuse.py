"""
Influenceuse model for Influenceur IA
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Float, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Influenceuse(Base):
    """Influenceuse model"""
    __tablename__ = "influenceuses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Profile info
    stage_name = Column(String(255), nullable=False)
    bio = Column(Text)
    avatar_url = Column(String(500))
    cover_image_url = Column(String(500))
    
    # Social media stats
    followers_count = Column(Integer, default=0)
    following_count = Column(Integer, default=0)
    posts_count = Column(Integer, default=0)
    
    # Content preferences
    content_categories = Column(JSON, default=list)  # ["lingerie", "feet", "nude"]
    content_style = Column(String(100))  # "glamour", "artistic", "casual"
    
    # Monetization
    subscription_price = Column(Float, default=0.0)
    tips_enabled = Column(Boolean, default=True)
    custom_content_enabled = Column(Boolean, default=True)
    
    # Status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    is_featured = Column(Boolean, default=False)
    
    # Settings
    auto_posting_enabled = Column(Boolean, default=True)
    chatbot_enabled = Column(Boolean, default=True)
    analytics_enabled = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_activity = Column(DateTime(timezone=True))
    
    # Relationships
    user = relationship("User", back_populates="influenceuse")
    content = relationship("Content", back_populates="influenceuse")
    conversations = relationship("Conversation", back_populates="influenceuse")
    # Optional relations for future models
    # platform_accounts = relationship("PlatformAccount", back_populates="influenceuse")
    # sales = relationship("Sale", back_populates="influenceuse")
    # analytics = relationship("Analytics", back_populates="influenceuse")
    
    def __repr__(self):
        return f"<Influenceuse(id={self.id}, stage_name='{self.stage_name}')>"
