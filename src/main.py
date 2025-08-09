"""
Main FastAPI application for Influenceur IA
"""

import os
import sys

# Ensure app package imports work regardless of working directory
sys.path.insert(0, os.path.dirname(__file__))

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
import structlog
import time

from app.core.config import settings
from app.core.database import engine
from app.api.v1.api import api_router
from app.core.logging import setup_logging
from app.core.database import redis_client

# Setup logging
setup_logging()
logger = structlog.get_logger()

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Backend API for Influenceur IA - Multi-influenceuse automation system",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=getattr(settings, "CORS_ALLOW_ORIGINS", settings.ALLOWED_HOSTS),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add trusted host middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.ALLOWED_HOSTS,
)


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response: Response = await call_next(request)
        if settings.SECURITY_HEADERS_ENABLED:
            response.headers.setdefault("X-Content-Type-Options", "nosniff")
            response.headers.setdefault("X-Frame-Options", "DENY")
            response.headers.setdefault("X-XSS-Protection", "1; mode=block")
            response.headers.setdefault("Referrer-Policy", "no-referrer")
            response.headers.setdefault("Permissions-Policy", "geolocation=(), microphone=()")
            response.headers.setdefault("Cache-Control", "no-store")
        return response


app.add_middleware(SecurityHeadersMiddleware)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.middleware("http")
async def rate_limit(request: Request, call_next):
    """Simple rate limit using Redis: per IP/method/path per minute."""
    path = request.url.path
    if path in {"/health", f"{settings.API_V1_STR}/health", f"{settings.API_V1_STR}/health/", f"{settings.API_V1_STR}/health/detailed"}:
        return await call_next(request)

    try:
        limit = getattr(settings, "RATE_LIMIT_PER_MINUTE", 0)
    except Exception:
        limit = 0

    if not limit or limit <= 0:
        return await call_next(request)

    client_ip = request.client.host if request.client else "unknown"
    key = f"ratelimit:{client_ip}:{request.method}:{path}"

    try:
        current = redis_client.incr(key)
        if current == 1:
            redis_client.expire(key, 60)
        if current > limit:
            return JSONResponse(status_code=429, content={"detail": "Rate limit exceeded"})
    except Exception:
        # Do not block on Redis failure
        pass

    return await call_next(request)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Add process time header to responses"""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests"""
    start_time = time.time()
    
    # Log request
    logger.info(
        "Request started",
        method=request.method,
        url=str(request.url),
        client_ip=request.client.host if request.client else None,
    )
    
    response = await call_next(request)
    
    # Log response
    process_time = time.time() - start_time
    logger.info(
        "Request completed",
        method=request.method,
        url=str(request.url),
        status_code=response.status_code,
        process_time=process_time,
    )
    
    return response


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    logger.error(
        "Unhandled exception",
        method=request.method,
        url=str(request.url),
        error=str(exc),
        exc_info=True,
    )
    
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )


@app.on_event("startup")
async def startup_event():
    """Application startup event"""
    logger.info("Starting Influenceur IA Backend")
    logger.info("Influenceur IA Backend started successfully")


@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown event"""
    logger.info("Shutting down Influenceur IA Backend")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Influenceur IA Backend API",
        "version": settings.VERSION,
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "version": settings.VERSION,
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )
