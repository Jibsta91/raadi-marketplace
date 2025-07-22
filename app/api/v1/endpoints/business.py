from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from app.core.database import get_db
from app.api.v1.endpoints.auth import get_current_user
from app.models.user import User

router = APIRouter()


@router.get("/dashboard")
async def get_business_dashboard(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get business dashboard data"""
    if current_user.role not in ["business", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Business account required"
        )
    
    dashboard_data = {
        "business_info": {
            "company_name": current_user.company_name or "My Business",
            "registration": current_user.company_registration,
            "address": current_user.company_address,
            "verified": True
        },
        "listings": {
            "total_listings": 45,
            "active_listings": 42,
            "pending_listings": 2,
            "expired_listings": 1,
            "featured_listings": 5
        },
        "analytics": {
            "total_views": 12450,
            "total_inquiries": 234,
            "conversion_rate": 1.9,
            "revenue_this_month": 45600,
            "currency": "NOK"
        },
        "recent_activity": [
            {
                "type": "new_inquiry",
                "message": "New inquiry for Tesla Model 3",
                "timestamp": "2025-01-22T09:30:00Z"
            },
            {
                "type": "listing_viewed",
                "message": "Your BMW listing was viewed 15 times",
                "timestamp": "2025-01-22T08:45:00Z"
            }
        ]
    }
    
    return dashboard_data


@router.get("/analytics")
async def get_business_analytics(
    period: str = "30d",
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get detailed business analytics"""
    if current_user.role not in ["business", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Business account required"
        )
    
    analytics = {
        "period": period,
        "overview": {
            "total_revenue": 125600,
            "total_listings": 45,
            "total_views": 45600,
            "total_inquiries": 678,
            "conversion_rate": 2.1
        },
        "performance_trends": {
            "views_trend": "+15.2%",
            "inquiries_trend": "+8.7%",
            "revenue_trend": "+22.3%"
        },
        "category_performance": [
            {
                "category": "bil_og_campingvogn",
                "listings": 15,
                "views": 28900,
                "inquiries": 234,
                "revenue": 89400
            },
            {
                "category": "torget",
                "listings": 20,
                "views": 12300,
                "inquiries": 156,
                "revenue": 24600
            }
        ]
    }
    
    return analytics
