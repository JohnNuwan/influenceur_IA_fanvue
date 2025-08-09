"""
Conversation model for Influenceur IA
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, JSON, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.core.database import Base


class ConversationStatus(str, enum.Enum):
    """Conversation status"""
    ACTIVE = "active"
    PAUSED = "paused"
    CLOSED = "closed"
    ARCHIVED = "archived"


class Conversation(Base):
    """Conversation model"""
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    influenceuse_id = Column(Integer, ForeignKey("influenceuses.id"), nullable=False)
    
    # Conversation info
    platform = Column(String(100))  # "fanvue", "onlyfans", "telegram", "discord"
    platform_conversation_id = Column(String(255))  # External conversation ID
    status = Column(Enum(ConversationStatus), default=ConversationStatus.ACTIVE)
    
    # Chatbot settings
    chatbot_enabled = Column(Boolean, default=True)
    auto_reply_enabled = Column(Boolean, default=True)
    ollama_model = Column(String(100), default="llama2:7b")
    
    # Conversation data
    conversation_history = Column(JSON, default=list)  # Store conversation context
    last_message_at = Column(DateTime(timezone=True))
    message_count = Column(Integer, default=0)
    
    # Analytics
    response_time_avg = Column(Integer)  # Average response time in seconds
    satisfaction_score = Column(Integer)  # User satisfaction score (1-5)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="conversations")
    influenceuse = relationship("Influenceuse", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Conversation(id={self.id}, platform='{self.platform}', status='{self.status}')>"


class Message(Base):
    """Message model"""
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    
    # Message info
    content = Column(Text, nullable=False)
    message_type = Column(String(50))  # "text", "image", "video", "audio"
    sender_type = Column(String(50))  # "user", "influenceuse", "bot"
    
    # Platform info
    platform_message_id = Column(String(255))  # External message ID
    platform_timestamp = Column(DateTime(timezone=True))
    
    # AI processing
    is_ai_generated = Column(Boolean, default=False)
    ai_model = Column(String(100))  # Model used for generation
    ai_confidence = Column(Integer)  # Confidence score (0-100)
    
    # Additional metadata (avoid reserved name 'metadata')
    metadata_json = Column(JSON)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    conversation = relationship("Conversation", back_populates="messages")
    
    def __repr__(self):
        return f"<Message(id={self.id}, type='{self.message_type}', sender='{self.sender_type}')>"
