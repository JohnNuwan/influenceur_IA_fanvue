"""
Sales endpoints for Influenceur IA
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.core.database import get_db
from app.models.influenceuse import Influenceuse

router = APIRouter()


# Pydantic models
class SaleCreate(BaseModel):
    influenceuse_id: int
    amount: float
    currency: str = "EUR"
    sale_type: str  # "subscription", "tip", "custom_content", "partnership"
    platform: str  # "fanvue", "onlyfans", "tiktok", "instagram"
    description: Optional[str] = None


class SaleResponse(BaseModel):
    id: int
    influenceuse_id: int
    amount: float
    currency: str
    sale_type: str
    platform: str
    description: Optional[str] = None
    created_at: str

    class Config:
        from_attributes = True


@router.post("/", response_model=SaleResponse)
async def create_sale(
    sale: SaleCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new sale record
    """
    # Check if influenceuse exists
    influenceuse = db.query(Influenceuse).filter(
        Influenceuse.id == sale.influenceuse_id
    ).first()
    
    if not influenceuse:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Influenceuse not found"
        )
    
    # Here you would create the actual sale record
    # For now, we'll return mock data
    mock_sale = {
        "id": 1,
        "influenceuse_id": sale.influenceuse_id,
        "amount": sale.amount,
        "currency": sale.currency,
        "sale_type": sale.sale_type,
        "platform": sale.platform,
        "description": sale.description,
        "created_at": "2024-01-15T10:00:00Z"
    }
    
    return mock_sale


@router.get("/{influenceuse_id}", response_model=List[SaleResponse])
async def get_sales(
    influenceuse_id: int,
    sale_type: Optional[str] = None,
    platform: Optional[str] = None,
    period: str = "30d",
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get sales for an influenceuse
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
    
    # Mock sales data
    mock_sales = [
        {
            "id": 1,
            "influenceuse_id": influenceuse_id,
            "amount": 50.0,
            "currency": "EUR",
            "sale_type": "subscription",
            "platform": "fanvue",
            "description": "Monthly subscription",
            "created_at": "2024-01-15T10:00:00Z"
        },
        {
            "id": 2,
            "influenceuse_id": influenceuse_id,
            "amount": 25.0,
            "currency": "EUR",
            "sale_type": "tip",
            "platform": "onlyfans",
            "description": "Tip from user",
            "created_at": "2024-01-14T15:30:00Z"
        }
    ]
    
    return mock_sales


@router.get("/{influenceuse_id}/summary")
async def get_sales_summary(
    influenceuse_id: int,
    period: str = "30d",
    db: Session = Depends(get_db)
):
    """
    Get sales summary for an influenceuse
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
    
    # Mock sales summary
    mock_summary = {
        "influenceuse_id": influenceuse_id,
        "period": period,
        "total_revenue": 8500.0,
        "total_sales": 150,
        "avg_sale_amount": 56.7,
        "revenue_breakdown": {
            "subscriptions": 4500.0,
            "tips": 1500.0,
            "custom_content": 2000.0,
            "partnerships": 500.0
        },
        "platform_breakdown": {
            "fanvue": 5000.0,
            "onlyfans": 3500.0
        },
        "top_selling_items": [
            {
                "name": "Monthly Subscription",
                "revenue": 3000.0,
                "sales_count": 60
            },
            {
                "name": "Custom Photos",
                "revenue": 1500.0,
                "sales_count": 30
            }
        ]
    }
    
    return mock_summary
