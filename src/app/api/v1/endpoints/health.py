"""
Health check endpoints
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import time

from app.core.database import get_db, check_database_connection, check_redis_connection
from app.core.config import settings

router = APIRouter()


@router.get("/")
async def health_check():
    """
    Basic health check
    """
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "version": settings.VERSION,
        "service": "influenceur-ia-backend",
    }


@router.get("/detailed")
async def detailed_health_check(db: Session = Depends(get_db)):
    """
    Detailed health check with database and Redis status
    """
    # Check database connection
    db_status = check_database_connection()
    
    # Check Redis connection
    redis_status = check_redis_connection()
    
    # Overall status
    overall_status = "healthy" if db_status and redis_status else "unhealthy"
    
    return {
        "status": overall_status,
        "timestamp": time.time(),
        "version": settings.VERSION,
        "service": "influenceur-ia-backend",
        "database": {
            "status": "connected" if db_status else "disconnected",
            "url": settings.DATABASE_URL.split("@")[-1] if "@" in settings.DATABASE_URL else "localhost",
        },
        "redis": {
            "status": "connected" if redis_status else "disconnected",
            "url": settings.REDIS_URL,
        },
        "features": {
            "multi_tenant": settings.MULTI_TENANT_ENABLED,
            "ollama_enabled": bool(settings.OLLAMA_URL),
            "minio_enabled": bool(settings.MINIO_ENDPOINT),
        },
    }
