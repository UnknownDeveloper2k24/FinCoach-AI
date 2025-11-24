"""Machine Learning Modules for FINCoach AI"""
from app.ml_modules.anomaly_detector import AnomalyDetector
from app.ml_modules.categorizer import Categorizer
from app.ml_modules.prediction_engine import PredictionEngine
from app.ml_modules.advanced_analytics import AdvancedAnalytics, AnalyticsMetric
from app.ml_modules.predictive_insights import PredictiveInsights, PredictionType

__all__ = [
    "AnomalyDetector",
    "Categorizer",
    "PredictionEngine",
    "AdvancedAnalytics",
    "AnalyticsMetric",
    "PredictiveInsights",
    "PredictionType",
]
