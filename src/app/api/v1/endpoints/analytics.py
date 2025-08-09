"""
Analytics endpoints for Influenceur IA
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.core.database import get_db
from app.models.influenceuse import Influenceuse
from app.models.content import Content

router = APIRouter()


# Pydantic models
class AnalyticsResponse(BaseModel):
    influenceuse_id: int
    period: str
    metrics: dict
    growth: dict
    top_content: List[dict]
    platform_performance: dict

    class Config:
        from_attributes = True


@router.get("/{influenceuse_id}/overview")
async def get_analytics_overview(
    influenceuse_id: int,
    period: str = "30d",
    db: Session = Depends(get_db)
):
    """
    Get analytics overview for an influenceuse
    """
    # Check if influenceuse exists
    influenceuse = db.query(Influenceuse).filter(
        Influenceuse.id == influenceuse_id
    ).first()
    
    if not influenceuse:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Influenceuse not found"
        )
    
    # Here you would calculate actual analytics
    # For now, we'll return mock data
    mock_analytics = {
        "influenceuse_id": influenceuse_id,
        "period": period,
        "metrics": {
            "total_revenue": 8500.0,
            "total_followers": 15000,
            "total_engagement": 2500,
            "total_content": 45,
            "avg_engagement_rate": 16.7,
            "conversion_rate": 3.2
        },
        "growth": {
            "revenue_growth": 25.5,
            "followers_growth": 12.3,
            "engagement_growth": 8.7,
            "content_growth": 15.2
        },
        "top_content": [
            {
                "id": 1,
                "title": "Summer Vibes",
                "views": 2500,
                "likes": 450,
                "shares": 120
            },
            {
                "id": 2,
                "title": "Behind the Scenes",
                "views": 1800,
                "likes": 320,
                "shares": 85
            }
        ],
        "platform_performance": {
            "fanvue": {
                "revenue": 5000.0,
                "subscribers": 250,
                "engagement": 1200
            },
            "onlyfans": {
                "revenue": 3500.0,
                "subscribers": 180,
                "engagement": 1300
            },
            "tiktok": {
                "followers": 8000,
                "views": 50000,
                "engagement": 2500
            }
        }
    }
    
    return mock_analytics


@router.get("/{influenceuse_id}/revenue")
async def get_revenue_analytics(
    influenceuse_id: int,
    period: str = "30d",
    db: Session = Depends(get_db)
):
    """
    Get revenue analytics for an influenceuse
    """
    # Check if influenceuse exists
    influenceuse = db.query(Influenceuse).filter(
        Influenceuse.id == influenceuse_id
    ).first()
    
    if not influenceuse:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Influenceuse not found"
        )
    
    # Mock revenue data
    mock_revenue = {
        "influenceuse_id": influenceuse_id,
        "period": period,
        "total_revenue": 8500.0,
        "revenue_breakdown": {
            "subscriptions": 4500.0,
            "tips": 1500.0,
            "custom_content": 2000.0,
            "partnerships": 500.0
        },
        "revenue_trend": [
            {"date": "2024-01-01", "revenue": 250.0},
            {"date": "2024-01-02", "revenue": 300.0},
            {"date": "2024-01-03", "revenue": 280.0}
        ],
        "platform_revenue": {
            "fanvue": 5000.0,
            "onlyfans": 3500.0
        }
    }
    
    return mock_revenue


@router.get("/{influenceuse_id}/engagement")
async def get_engagement_analytics(
    influenceuse_id: int,
    period: str = "30d",
    db: Session = Depends(get_db)
):
    """
    Get engagement analytics for an influenceuse
    """
    # Check if influenceuse exists
    influenceuse = db.query(Influenceuse).filter(
        Influenceuse.id == influenceuse_id
    ).first()
    
    if not influenceuse:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Influenceuse not found"
        )
    
    # Mock engagement data
    mock_engagement = {
        "influenceuse_id": influenceuse_id,
        "period": period,
        "total_engagement": 2500,
        "engagement_rate": 16.7,
        "engagement_breakdown": {
            "likes": 1500,
            "comments": 600,
            "shares": 400
        },
        "engagement_trend": [
            {"date": "2024-01-01", "engagement": 80},
            {"date": "2024-01-02", "engagement": 95},
            {"date": "2024-01-03", "engagement": 75}
        ],
        "top_engaging_content": [
            {
                "id": 1,
                "title": "Summer Vibes",
                "engagement_rate": 25.5,
                "likes": 450,
                "comments": 120,
                "shares": 85
            }
        ]
    }
    
    return mock_engagement


@router.get("/{influenceuse_id}/content")
async def get_content_analytics(
    influenceuse_id: int,
    period: str = "30d",
    db: Session = Depends(get_db)
):
    """
    Get content analytics for an influenceuse
    """
    # Check if influenceuse exists
    influenceuse = db.query(Influenceuse).filter(
        Influenceuse.id == influenceuse_id
    ).first()
    
    if not influenceuse:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Influenceuse not found"
        )
    
    # Mock content analytics
    mock_content = {
        "influenceuse_id": influenceuse_id,
        "period": period,
        "total_content": 45,
        "content_breakdown": {
            "images": 30,
            "videos": 10,
            "text": 5
        },
        "content_performance": {
            "avg_views": 1200,
            "avg_likes": 180,
            "avg_comments": 45,
            "avg_shares": 25
        },
        "top_performing_content": [
            {
                "id": 1,
                "title": "Summer Vibes",
                "type": "image",
                "views": 2500,
                "likes": 450,
                "engagement_rate": 25.5
            }
        ]
    }
    
    return mock_content


@router.get("/{influenceuse_id}/audience")
async def get_audience_analytics(
    influenceuse_id: int,
    period: str = "30d",
    db: Session = Depends(get_db)
):
    """
    Get audience analytics for an influenceuse
    """
    # Check if influenceuse exists
    influenceuse = db.query(Influenceuse).filter(
        Influenceuse.id == influenceuse_id
    ).first()
    
    if not influenceuse:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Influenceuse not found"
        )
    
    # Mock audience data
    mock_audience = {
        "influenceuse_id": influenceuse_id,
        "period": period,
        "total_followers": 15000,
        "follower_growth": 12.3,
        "audience_demographics": {
            "age_groups": {
                "18-24": 35,
                "25-34": 45,
                "35-44": 15,
                "45+": 5
            },
            "gender": {
                "male": 60,
                "female": 40
            },
            "locations": {
                "United States": 40,
                "United Kingdom": 25,
                "Canada": 15,
                "Other": 20
            }
        },
        "audience_engagement": {
            "active_followers": 8500,
            "engagement_rate": 16.7,
            "avg_time_spent": 3.5
        }
    }
    
    return mock_audience
