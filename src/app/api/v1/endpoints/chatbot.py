"""
Chatbot endpoints with Ollama integration
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from pydantic import BaseModel
import httpx
import json
from datetime import datetime

from app.core.database import get_db
from app.models.conversation import Conversation, Message, ConversationStatus
from app.models.influenceuse import Influenceuse
from app.core.config import settings

router = APIRouter()


# Pydantic models
class MessageCreate(BaseModel):
    content: str
    message_type: str = "text"
    sender_type: str = "user"


class MessageResponse(BaseModel):
    id: int
    content: str
    message_type: str
    sender_type: str
    is_ai_generated: bool
    created_at: str

    class Config:
        from_attributes = True


class ConversationCreate(BaseModel):
    influenceuse_id: int
    platform: str
    platform_conversation_id: Optional[str] = None


class ConversationResponse(BaseModel):
    id: int
    influenceuse_id: int
    platform: str
    status: str
    chatbot_enabled: bool
    auto_reply_enabled: bool
    ollama_model: str
    message_count: int
    created_at: str
    last_message_at: Optional[str] = None

    class Config:
        from_attributes = True


class OllamaRequest(BaseModel):
    model: str
    prompt: str
    stream: bool = False


class OllamaResponse(BaseModel):
    response: str
    model: str
    created_at: str


async def call_ollama(prompt: str, model: str = "llama2:7b") -> str:
    """
    Call Ollama API to generate response
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{settings.OLLAMA_URL}/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=30.0
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get("response", "")
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to generate response from Ollama"
                )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error calling Ollama: {str(e)}"
        )


@router.post("/conversations", response_model=ConversationResponse)
async def create_conversation(
    conversation: ConversationCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new conversation
    """
    # Check if influenceuse exists
    influenceuse = db.query(Influenceuse).filter(
        Influenceuse.id == conversation.influenceuse_id
    ).first()
    
    if not influenceuse:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Influenceuse not found"
        )
    
    # Create new conversation
    db_conversation = Conversation(
        influenceuse_id=conversation.influenceuse_id,
        platform=conversation.platform,
        platform_conversation_id=conversation.platform_conversation_id,
        ollama_model=settings.OLLAMA_MODEL
    )
    
    db.add(db_conversation)
    db.commit()
    db.refresh(db_conversation)
    
    return db_conversation


@router.get("/conversations", response_model=List[ConversationResponse])
async def get_conversations(
    influenceuse_id: Optional[int] = None,
    platform: Optional[str] = None,
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get conversations with filters
    """
    query = db.query(Conversation)
    
    if influenceuse_id:
        query = query.filter(Conversation.influenceuse_id == influenceuse_id)
    
    if platform:
        query = query.filter(Conversation.platform == platform)
    
    if status:
        query = query.filter(Conversation.status == status)
    
    conversations = query.offset(skip).limit(limit).all()
    return conversations


@router.get("/conversations/{conversation_id}", response_model=ConversationResponse)
async def get_conversation(conversation_id: int, db: Session = Depends(get_db)):
    """
    Get conversation by ID
    """
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    return conversation


@router.post("/conversations/{conversation_id}/messages", response_model=MessageResponse)
async def send_message(
    conversation_id: int,
    message: MessageCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Send a message in a conversation
    """
    # Check if conversation exists
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    # Create user message
    db_message = Message(
        conversation_id=conversation_id,
        content=message.content,
        message_type=message.message_type,
        sender_type=message.sender_type
    )
    
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    
    # Update conversation
    conversation.message_count += 1
    conversation.last_message_at = db_message.created_at
    db.commit()
    
    # Generate AI response if auto-reply is enabled
    if conversation.auto_reply_enabled and message.sender_type == "user":
        background_tasks.add_task(
            generate_ai_response,
            conversation_id,
            message.content,
            db
        )
    
    return db_message


@router.get("/conversations/{conversation_id}/messages", response_model=List[MessageResponse])
async def get_messages(
    conversation_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get messages in a conversation
    """
    # Check if conversation exists
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    messages = db.query(Message).filter(
        Message.conversation_id == conversation_id
    ).offset(skip).limit(limit).all()
    
    return messages


async def generate_ai_response(conversation_id: int, user_message: str, db: Session):
    """
    Generate AI response using Ollama
    """
    try:
        # Get conversation
        conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
        if not conversation:
            return
        
        # Generate response using Ollama
        prompt = f"User: {user_message}\nAssistant:"
        ai_response = await call_ollama(prompt, conversation.ollama_model)
        
        # Create AI message
        db_message = Message(
            conversation_id=conversation_id,
            content=ai_response,
            message_type="text",
            sender_type="bot",
            is_ai_generated=True,
            ai_model=conversation.ollama_model
        )
        
        db.add(db_message)
        db.commit()
        
        # Update conversation
        conversation.message_count += 1
        conversation.last_message_at = db_message.created_at
        db.commit()
        
    except Exception as e:
        print(f"Error generating AI response: {e}")


@router.post("/ollama/generate", response_model=OllamaResponse)
async def generate_with_ollama(request: OllamaRequest):
    """
    Generate response using Ollama directly
    """
    try:
        response = await call_ollama(request.prompt, request.model)
        return OllamaResponse(
            response=response,
            model=request.model,
            created_at=str(datetime.utcnow())
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating response: {str(e)}"
        )
