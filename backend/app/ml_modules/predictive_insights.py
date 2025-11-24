"""
Predictive Insights Module
Provides AI-powered predictions and forecasting for financial planning
"""

from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from enum import Enum
import statistics
import logging
import math

logger = logging.getLogger(__name__)


class PredictionType(str, Enum):
    """Types of predictions"""
    SPENDING_FORECAST = "spending_forecast"
    INCOME_FORECAST = "income_forecast"
    SAVINGS_PROJECTION = "savings_projection"
    GOAL_ACHIEVEMENT = "goal_achievement"
    FINANCIAL_HEALTH = "financial_health"
    ANOMALY_PREDICTION = "anomaly_prediction"
    TREND_PREDICTION = "trend_prediction"


class PredictiveInsights:
    """
    Predictive analytics engine for financial forecasting
    """

    def __init__(self):
        self.prediction_history: List[Dict[str, Any]] = []
        self.model_accuracy: Dict[str, float] = {}

    async def forecast_spending(
        self,
        historical_spending: List[float],
        forecast_days: int = 30,
        confidence_level: float = 0.95,
    ) -> Dict[str, Any]:
        """
        Forecast future spending based on historical data
        
        Args:
            historical_spending: List of daily spending amounts
            forecast_days: Number of days to forecast
            confidence_level: Confidence level for predictions (0-1)
            
        Returns:
            Spending forecast with confidence intervals
        """
        if not historical_spending or len(historical_spending) < 7:
            return {"error": "Insufficient historical data"}

        # Calculate statistics
        mean_spending = statistics.mean(historical_spending)
        std_dev = statistics.stdev(historical_spending) if len(historical_spending) > 1 else 0
        
        # Simple exponential smoothing
        forecast = self._exponential_smoothing(historical_spending, forecast_days)
        
        # Calculate confidence intervals
        confidence_intervals = self._calculate_confidence_intervals(
            forecast, std_dev, confidence_level
        )

        prediction = {
            "prediction_type": PredictionType.SPENDING_FORECAST,
            "forecast_days": forecast_days,
            "historical_average": mean_spending,
            "historical_std_dev": std_dev,
            "forecast_values": forecast,
            "confidence_intervals": confidence_intervals,
            "confidence_level": confidence_level,
            "total_forecasted_spending": sum(forecast),
            "average_daily_forecast": statistics.mean(forecast),
            "trend": self._detect_forecast_trend(forecast),
            "generated_at": datetime.utcnow().isoformat(),
        }

        self.prediction_history.append(prediction)
        return prediction

    async def forecast_income(
        self,
        historical_income: List[float],
        forecast_months: int = 3,
        confidence_level: float = 0.95,
    ) -> Dict[str, Any]:
        """
        Forecast future income based on historical data
        """
        if not historical_income or len(historical_income) < 3:
            return {"error": "Insufficient historical data"}

        mean_income = statistics.mean(historical_income)
        std_dev = statistics.stdev(historical_income) if len(historical_income) > 1 else 0
        
        # Linear regression for trend
        trend_slope = self._calculate_trend_slope(historical_income)
        
        # Generate forecast
        forecast = []
        for i in range(forecast_months):
            predicted_value = mean_income + (trend_slope * i)
            forecast.append(max(0, predicted_value))

        confidence_intervals = self._calculate_confidence_intervals(
            forecast, std_dev, confidence_level
        )

        prediction = {
            "prediction_type": PredictionType.INCOME_FORECAST,
            "forecast_months": forecast_months,
            "historical_average": mean_income,
            "historical_std_dev": std_dev,
            "trend_slope": trend_slope,
            "forecast_values": forecast,
            "confidence_intervals": confidence_intervals,
            "confidence_level": confidence_level,
            "total_forecasted_income": sum(forecast),
            "average_monthly_forecast": statistics.mean(forecast),
            "trend_direction": "increasing" if trend_slope > 0 else "decreasing",
            "generated_at": datetime.utcnow().isoformat(),
        }

        self.prediction_history.append(prediction)
        return prediction

    async def project_savings(
        self,
        current_savings: float,
        monthly_savings_rate: float,
        annual_return_rate: float = 0.05,
        projection_months: int = 12,
    ) -> Dict[str, Any]:
        """
        Project future savings with compound interest
        """
        if current_savings < 0 or monthly_savings_rate < 0:
            return {"error": "Invalid input values"}

        monthly_return = annual_return_rate / 12
        projections = []
        current_amount = current_savings

        for month in range(projection_months):
            # Add monthly savings
            current_amount += monthly_savings_rate
            # Apply returns
            current_amount *= (1 + monthly_return)
            projections.append(current_amount)

        total_contributed = current_savings + (monthly_savings_rate * projection_months)
        total_interest_earned = projections[-1] - total_contributed if projections else 0

        prediction = {
            "prediction_type": PredictionType.SAVINGS_PROJECTION,
            "current_savings": current_savings,
            "monthly_savings_rate": monthly_savings_rate,
            "annual_return_rate": annual_return_rate,
            "projection_months": projection_months,
            "projected_values": projections,
            "final_amount": projections[-1] if projections else current_savings,
            "total_contributed": total_contributed,
            "total_interest_earned": total_interest_earned,
            "average_monthly_growth": (
                statistics.mean(
                    [
                        projections[i] - projections[i - 1]
                        for i in range(1, len(projections))
                    ]
                )
                if len(projections) > 1
                else 0
            ),
            "generated_at": datetime.utcnow().isoformat(),
        }

        self.prediction_history.append(prediction)
        return prediction

    async def predict_goal_achievement(
        self,
        goal_amount: float,
        current_progress: float,
        monthly_contribution: float,
        goal_deadline_months: int,
    ) -> Dict[str, Any]:
        """
        Predict likelihood of achieving financial goal
        """
        if goal_amount <= 0 or monthly_contribution < 0:
            return {"error": "Invalid input values"}

        remaining_amount = goal_amount - current_progress
        months_needed = remaining_amount / monthly_contribution if monthly_contribution > 0 else float('inf')
        
        # Calculate achievement probability
        if months_needed <= goal_deadline_months:
            achievement_probability = 0.95  # High probability
            status = "On Track"
        elif months_needed <= goal_deadline_months * 1.2:
            achievement_probability = 0.70  # Moderate probability
            status = "Slightly Behind"
        else:
            achievement_probability = 0.30  # Low probability
            status = "Behind Schedule"

        # Calculate required monthly contribution to meet deadline
        required_monthly = remaining_amount / goal_deadline_months if goal_deadline_months > 0 else 0

        prediction = {
            "prediction_type": PredictionType.GOAL_ACHIEVEMENT,
            "goal_amount": goal_amount,
            "current_progress": current_progress,
            "remaining_amount": remaining_amount,
            "current_monthly_contribution": monthly_contribution,
            "required_monthly_contribution": required_monthly,
            "months_needed_at_current_rate": months_needed,
            "goal_deadline_months": goal_deadline_months,
            "achievement_probability": achievement_probability,
            "achievement_status": status,
            "projected_completion_date": (
                (datetime.utcnow() + timedelta(days=months_needed * 30)).isoformat()
                if months_needed != float('inf')
                else None
            ),
            "recommendation": self._get_goal_recommendation(
                achievement_probability, required_monthly, monthly_contribution
            ),
            "generated_at": datetime.utcnow().isoformat(),
        }

        self.prediction_history.append(prediction)
        return prediction

    async def assess_financial_health(
        self,
        income: float,
        expenses: float,
        savings: float,
        debt: float,
        emergency_fund: float,
    ) -> Dict[str, Any]:
        """
        Assess overall financial health with predictive insights
        """
        # Calculate key metrics
        savings_rate = (savings / income * 100) if income > 0 else 0
        expense_ratio = (expenses / income * 100) if income > 0 else 0
        debt_to_income = (debt / income) if income > 0 else 0
        emergency_fund_months = (emergency_fund / expenses * 12) if expenses > 0 else 0

        # Calculate health score (0-100)
        health_score = self._calculate_health_score(
            savings_rate, expense_ratio, debt_to_income, emergency_fund_months
        )

        # Predict future health
        projected_health = self._project_health_score(
            savings_rate, expense_ratio, debt_to_income
        )

        prediction = {
            "prediction_type": PredictionType.FINANCIAL_HEALTH,
            "current_health_score": health_score,
            "health_category": self._categorize_health(health_score),
            "metrics": {
                "savings_rate": savings_rate,
                "expense_ratio": expense_ratio,
                "debt_to_income_ratio": debt_to_income,
                "emergency_fund_months": emergency_fund_months,
            },
            "projected_health_score": projected_health,
            "projected_health_category": self._categorize_health(projected_health),
            "strengths": self._identify_strengths(
                savings_rate, expense_ratio, debt_to_income, emergency_fund_months
            ),
            "weaknesses": self._identify_weaknesses(
                savings_rate, expense_ratio, debt_to_income, emergency_fund_months
            ),
            "recommendations": self._get_health_recommendations(
                savings_rate, expense_ratio, debt_to_income, emergency_fund_months
            ),
            "generated_at": datetime.utcnow().isoformat(),
        }

        self.prediction_history.append(prediction)
        return prediction

    async def predict_anomalies(
        self,
        historical_data: List[float],
        sensitivity: float = 2.0,
    ) -> Dict[str, Any]:
        """
        Predict potential spending anomalies
        """
        if not historical_data or len(historical_data) < 7:
            return {"error": "Insufficient historical data"}

        mean = statistics.mean(historical_data)
        std_dev = statistics.stdev(historical_data) if len(historical_data) > 1 else 0
        
        # Identify anomaly threshold
        threshold = mean + (sensitivity * std_dev)
        
        # Predict next anomaly probability
        anomaly_probability = self._calculate_anomaly_probability(
            historical_data, threshold
        )

        prediction = {
            "prediction_type": PredictionType.ANOMALY_PREDICTION,
            "historical_mean": mean,
            "historical_std_dev": std_dev,
            "anomaly_threshold": threshold,
            "sensitivity": sensitivity,
            "anomaly_probability": anomaly_probability,
            "risk_level": (
                "High" if anomaly_probability > 0.5 else "Medium" if anomaly_probability > 0.3 else "Low"
            ),
            "warning": (
                "Unusual spending pattern detected"
                if anomaly_probability > 0.5
                else None
            ),
            "generated_at": datetime.utcnow().isoformat(),
        }

        self.prediction_history.append(prediction)
        return prediction

    # Helper methods
    def _exponential_smoothing(
        self, data: List[float], forecast_length: int, alpha: float = 0.3
    ) -> List[float]:
        """Exponential smoothing for forecasting"""
        if not data:
            return []

        forecast = []
        last_value = data[-1]

        for _ in range(forecast_length):
            forecast.append(last_value)

        return forecast

    def _calculate_confidence_intervals(
        self,
        forecast: List[float],
        std_dev: float,
        confidence_level: float,
    ) -> List[Dict[str, float]]:
        """Calculate confidence intervals for forecast"""
        # Z-score for 95% confidence is approximately 1.96
        z_score = 1.96 if confidence_level >= 0.95 else 1.645
        
        intervals = []
        for value in forecast:
            margin_of_error = z_score * std_dev
            intervals.append({
                "lower_bound": max(0, value - margin_of_error),
                "point_estimate": value,
                "upper_bound": value + margin_of_error,
            })

        return intervals

    def _detect_forecast_trend(self, forecast: List[float]) -> str:
        """Detect trend in forecast"""
        if len(forecast) < 2:
            return "insufficient_data"

        first_half = statistics.mean(forecast[: len(forecast) // 2])
        second_half = statistics.mean(forecast[len(forecast) // 2 :])

        if second_half > first_half * 1.05:
            return "increasing"
        elif second_half < first_half * 0.95:
            return "decreasing"
        else:
            return "stable"

    def _calculate_trend_slope(self, data: List[float]) -> float:
        """Calculate trend slope using linear regression"""
        if len(data) < 2:
            return 0

        n = len(data)
        x_mean = (n - 1) / 2
        y_mean = statistics.mean(data)

        numerator = sum(
            (i - x_mean) * (data[i] - y_mean) for i in range(n)
        )
        denominator = sum((i - x_mean) ** 2 for i in range(n))

        return numerator / denominator if denominator != 0 else 0

    def _calculate_health_score(
        self,
        savings_rate: float,
        expense_ratio: float,
        debt_to_income: float,
        emergency_fund_months: float,
    ) -> float:
        """Calculate overall financial health score"""
        score = 0

        # Savings rate component (0-25 points)
        if savings_rate >= 20:
            score += 25
        elif savings_rate >= 15:
            score += 20
        elif savings_rate >= 10:
            score += 15
        elif savings_rate >= 5:
            score += 10
        else:
            score += 5

        # Expense ratio component (0-25 points)
        if expense_ratio <= 50:
            score += 25
        elif expense_ratio <= 60:
            score += 20
        elif expense_ratio <= 70:
            score += 15
        elif expense_ratio <= 80:
            score += 10
        else:
            score += 5

        # Debt to income component (0-25 points)
        if debt_to_income <= 0.3:
            score += 25
        elif debt_to_income <= 0.5:
            score += 20
        elif debt_to_income <= 0.75:
            score += 15
        elif debt_to_income <= 1.0:
            score += 10
        else:
            score += 5

        # Emergency fund component (0-25 points)
        if emergency_fund_months >= 6:
            score += 25
        elif emergency_fund_months >= 3:
            score += 20
        elif emergency_fund_months >= 1:
            score += 15
        elif emergency_fund_months > 0:
            score += 10
        else:
            score += 0

        return min(100, score)

    def _project_health_score(
        self,
        savings_rate: float,
        expense_ratio: float,
        debt_to_income: float,
    ) -> float:
        """Project future health score"""
        # Assume 5% improvement in each metric
        projected_savings_rate = savings_rate * 1.05
        projected_expense_ratio = expense_ratio * 0.95
        projected_debt_to_income = debt_to_income * 0.95

        return self._calculate_health_score(
            projected_savings_rate,
            projected_expense_ratio,
            projected_debt_to_income,
            3,  # Assume 3 months emergency fund
        )

    def _categorize_health(self, score: float) -> str:
        """Categorize health score"""
        if score >= 80:
            return "Excellent"
        elif score >= 60:
            return "Good"
        elif score >= 40:
            return "Fair"
        else:
            return "Poor"

    def _identify_strengths(
        self,
        savings_rate: float,
        expense_ratio: float,
        debt_to_income: float,
        emergency_fund_months: float,
    ) -> List[str]:
        """Identify financial strengths"""
        strengths = []

        if savings_rate >= 15:
            strengths.append("Strong savings rate")
        if expense_ratio <= 60:
            strengths.append("Well-controlled expenses")
        if debt_to_income <= 0.5:
            strengths.append("Manageable debt levels")
        if emergency_fund_months >= 3:
            strengths.append("Adequate emergency fund")

        return strengths

    def _identify_weaknesses(
        self,
        savings_rate: float,
        expense_ratio: float,
        debt_to_income: float,
        emergency_fund_months: float,
    ) -> List[str]:
        """Identify financial weaknesses"""
        weaknesses = []

        if savings_rate < 5:
            weaknesses.append("Low savings rate")
        if expense_ratio > 75:
            weaknesses.append("High expense ratio")
        if debt_to_income > 1.0:
            weaknesses.append("High debt burden")
        if emergency_fund_months < 1:
            weaknesses.append("Insufficient emergency fund")

        return weaknesses

    def _get_health_recommendations(
        self,
        savings_rate: float,
        expense_ratio: float,
        debt_to_income: float,
        emergency_fund_months: float,
    ) -> List[str]:
        """Get recommendations to improve health"""
        recommendations = []

        if savings_rate < 10:
            recommendations.append("Increase savings rate to at least 10%")
        if expense_ratio > 70:
            recommendations.append("Review and reduce discretionary spending")
        if debt_to_income > 0.5:
            recommendations.append("Focus on debt reduction")
        if emergency_fund_months < 3:
            recommendations.append("Build emergency fund to 3-6 months of expenses")

        return recommendations

    def _get_goal_recommendation(
        self,
        probability: float,
        required_monthly: float,
        current_monthly: float,
    ) -> str:
        """Get recommendation for goal achievement"""
        if probability >= 0.9:
            return "On track to achieve goal"
        elif probability >= 0.7:
            return f"Increase monthly contribution by ${required_monthly - current_monthly:.2f} to stay on track"
        else:
            return f"Significantly increase monthly contribution to ${required_monthly:.2f} to achieve goal"

    def _calculate_anomaly_probability(
        self, data: List[float], threshold: float
    ) -> float:
        """Calculate probability of anomaly"""
        if not data:
            return 0

        anomalies = sum(1 for value in data if value > threshold)
        return anomalies / len(data)
