"""
Main API router for v1
"""

from fastapi import APIRouter

from app.api.v1.endpoints import (
    auth,
    users,
    influenceuses,
    content,
    chatbot,
    social_media,
    analytics,
    sales,
    health,
)

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(influenceuses.router, prefix="/influenceuses", tags=["influenceuses"])
api_router.include_router(content.router, prefix="/content", tags=["content"])
api_router.include_router(chatbot.router, prefix="/chatbot", tags=["chatbot"])
api_router.include_router(social_media.router, prefix="/social-media", tags=["social-media"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
api_router.include_router(sales.router, prefix="/sales", tags=["sales"])
api_router.include_router(health.router, prefix="/health", tags=["health"])
