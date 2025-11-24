"""API endpoints for intelligent recommendations"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.ml_modules.intelligent_recommender import IntelligentRecommender
from app.models.user import User

router = APIRouter(prefix="/api/v1/recommendations", tags=["Intelligent Recommendations"])

@router.get("/personalized")
async def get_personalized_recommendations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get personalized financial recommendations based on spending patterns"""
    try:
        recommender = IntelligentRecommender(db)
        recommendations = recommender.get_personalized_recommendations(current_user.id)
        return recommendations
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/category/{category}")
async def get_category_recommendations(
    category: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific recommendations for a spending category"""
    try:
        recommender = IntelligentRecommender(db)
        recommendations = recommender.get_category_recommendations(current_user.id, category)
        return recommendations
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
