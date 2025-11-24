"""API endpoints for pattern recognition and advanced anomaly detection"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.ml_modules.pattern_recognition import PatternRecognition
from app.models.user import User

router = APIRouter(prefix="/api/v1/patterns", tags=["Pattern Recognition"])

@router.get("/all")
async def detect_all_patterns(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Detect all financial patterns for the user"""
    try:
        pattern_detector = PatternRecognition(db)
        patterns = pattern_detector.detect_all_patterns(current_user.id)
        return patterns
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/spending")
async def detect_spending_patterns(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Detect spending patterns across categories"""
    try:
        pattern_detector = PatternRecognition(db)
        patterns = pattern_detector._detect_spending_patterns(current_user.id)
        return {
            "status": "success",
            "patterns": patterns
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/temporal")
async def detect_temporal_patterns(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Detect temporal patterns (day of week, time of day)"""
    try:
        pattern_detector = PatternRecognition(db)
        patterns = pattern_detector._detect_temporal_patterns(current_user.id)
        return patterns
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/behavioral")
async def detect_behavioral_patterns(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Detect behavioral patterns in spending"""
    try:
        pattern_detector = PatternRecognition(db)
        patterns = pattern_detector._detect_behavioral_patterns(current_user.id)
        return patterns
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/anomalies")
async def detect_advanced_anomalies(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Detect advanced anomalies using statistical methods"""
    try:
        pattern_detector = PatternRecognition(db)
        anomalies = pattern_detector._detect_advanced_anomalies(current_user.id)
        return anomalies
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/correlations")
async def detect_spending_correlations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Detect correlations between spending categories"""
    try:
        pattern_detector = PatternRecognition(db)
        correlations = pattern_detector._detect_spending_correlations(current_user.id)
        return correlations
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
