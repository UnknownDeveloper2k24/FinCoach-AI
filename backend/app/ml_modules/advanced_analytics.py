"""
Advanced Analytics Module
Provides comprehensive financial analytics and insights
"""

from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from enum import Enum
import statistics
import logging

logger = logging.getLogger(__name__)


class AnalyticsMetric(str, Enum):
    """Types of analytics metrics"""
    SPENDING_PATTERN = "spending_pattern"
    INCOME_TREND = "income_trend"
    SAVINGS_RATE = "savings_rate"
    EXPENSE_RATIO = "expense_ratio"
    CASH_FLOW = "cash_flow"
    BUDGET_VARIANCE = "budget_variance"
    CATEGORY_ANALYSIS = "category_analysis"
    TEMPORAL_ANALYSIS = "temporal_analysis"


class AdvancedAnalytics:
    """
    Advanced analytics engine for comprehensive financial analysis
    """

    def __init__(self):
        self.metrics_cache: Dict[str, Any] = {}
        self.analysis_history: List[Dict[str, Any]] = []

    async def analyze_spending_patterns(
        self, transactions: List[Dict[str, Any]], period_days: int = 90
    ) -> Dict[str, Any]:
        """
        Analyze spending patterns over a period
        
        Args:
            transactions: List of transaction data
            period_days: Number of days to analyze
            
        Returns:
            Spending pattern analysis
        """
        if not transactions:
            return {"error": "No transactions provided"}

        # Filter transactions by period
        cutoff_date = datetime.utcnow() - timedelta(days=period_days)
        filtered_txns = [
            t
            for t in transactions
            if datetime.fromisoformat(t.get("date", "")) > cutoff_date
        ]

        # Categorize spending
        spending_by_category = self._categorize_spending(filtered_txns)
        
        # Calculate statistics
        daily_spending = self._calculate_daily_spending(filtered_txns)
        weekly_spending = self._calculate_weekly_spending(filtered_txns)
        
        # Identify patterns
        patterns = self._identify_spending_patterns(daily_spending, weekly_spending)

        analysis = {
            "period_days": period_days,
            "total_transactions": len(filtered_txns),
            "spending_by_category": spending_by_category,
            "daily_average": statistics.mean(daily_spending) if daily_spending else 0,
            "daily_median": statistics.median(daily_spending) if daily_spending else 0,
            "daily_std_dev": (
                statistics.stdev(daily_spending) if len(daily_spending) > 1 else 0
            ),
            "weekly_average": statistics.mean(weekly_spending) if weekly_spending else 0,
            "patterns_identified": patterns,
            "anomalies": self._detect_spending_anomalies(daily_spending),
        }

        return analysis

    async def analyze_income_trends(
        self, transactions: List[Dict[str, Any]], period_days: int = 90
    ) -> Dict[str, Any]:
        """
        Analyze income trends and stability
        """
        if not transactions:
            return {"error": "No transactions provided"}

        # Filter income transactions
        cutoff_date = datetime.utcnow() - timedelta(days=period_days)
        income_txns = [
            t
            for t in transactions
            if t.get("type") == "income"
            and datetime.fromisoformat(t.get("date", "")) > cutoff_date
        ]

        if not income_txns:
            return {"error": "No income transactions found"}

        # Calculate income statistics
        income_amounts = [t.get("amount", 0) for t in income_txns]
        income_by_source = self._categorize_income(income_txns)
        
        # Trend analysis
        monthly_income = self._calculate_monthly_income(income_txns)
        trend = self._calculate_trend(monthly_income)

        analysis = {
            "period_days": period_days,
            "total_income_transactions": len(income_txns),
            "total_income": sum(income_amounts),
            "average_income": statistics.mean(income_amounts) if income_amounts else 0,
            "income_stability": self._calculate_stability(income_amounts),
            "income_by_source": income_by_source,
            "monthly_trend": monthly_income,
            "trend_direction": trend,
            "projected_annual_income": self._project_annual_income(monthly_income),
        }

        return analysis

    async def calculate_savings_rate(
        self,
        income: float,
        expenses: float,
        savings: float,
        period_days: int = 30,
    ) -> Dict[str, Any]:
        """
        Calculate and analyze savings rate
        """
        if income <= 0:
            return {"error": "Invalid income value"}

        savings_rate = (savings / income) * 100 if income > 0 else 0
        expense_ratio = (expenses / income) * 100 if income > 0 else 0

        analysis = {
            "period_days": period_days,
            "income": income,
            "expenses": expenses,
            "savings": savings,
            "savings_rate_percent": savings_rate,
            "expense_ratio_percent": expense_ratio,
            "savings_rate_category": self._categorize_savings_rate(savings_rate),
            "recommendation": self._get_savings_recommendation(savings_rate),
            "target_savings_rate": 20,  # Industry standard
            "gap_to_target": max(0, 20 - savings_rate),
        }

        return analysis

    async def analyze_budget_variance(
        self,
        budget: Dict[str, float],
        actual_spending: Dict[str, float],
    ) -> Dict[str, Any]:
        """
        Analyze variance between budget and actual spending
        """
        variance_analysis = {}
        total_budget = 0
        total_actual = 0
        total_variance = 0

        for category, budgeted_amount in budget.items():
            actual_amount = actual_spending.get(category, 0)
            variance = actual_amount - budgeted_amount
            variance_percent = (variance / budgeted_amount * 100) if budgeted_amount > 0 else 0

            variance_analysis[category] = {
                "budgeted": budgeted_amount,
                "actual": actual_amount,
                "variance": variance,
                "variance_percent": variance_percent,
                "status": "Over" if variance > 0 else "Under",
            }

            total_budget += budgeted_amount
            total_actual += actual_amount
            total_variance += variance

        overall_variance_percent = (
            (total_variance / total_budget * 100) if total_budget > 0 else 0
        )

        analysis = {
            "category_analysis": variance_analysis,
            "total_budget": total_budget,
            "total_actual": total_actual,
            "total_variance": total_variance,
            "overall_variance_percent": overall_variance_percent,
            "categories_over_budget": [
                cat for cat, data in variance_analysis.items() if data["variance"] > 0
            ],
            "categories_under_budget": [
                cat for cat, data in variance_analysis.items() if data["variance"] < 0
            ],
        }

        return analysis

    async def analyze_cash_flow(
        self, transactions: List[Dict[str, Any]], period_days: int = 90
    ) -> Dict[str, Any]:
        """
        Analyze cash flow patterns
        """
        if not transactions:
            return {"error": "No transactions provided"}

        cutoff_date = datetime.utcnow() - timedelta(days=period_days)
        filtered_txns = [
            t
            for t in transactions
            if datetime.fromisoformat(t.get("date", "")) > cutoff_date
        ]

        # Calculate daily cash flow
        daily_cash_flow = self._calculate_daily_cash_flow(filtered_txns)
        
        # Calculate cumulative cash flow
        cumulative_flow = self._calculate_cumulative_flow(daily_cash_flow)

        analysis = {
            "period_days": period_days,
            "total_inflow": sum(
                t.get("amount", 0)
                for t in filtered_txns
                if t.get("type") == "income"
            ),
            "total_outflow": sum(
                t.get("amount", 0)
                for t in filtered_txns
                if t.get("type") == "expense"
            ),
            "net_cash_flow": cumulative_flow[-1] if cumulative_flow else 0,
            "average_daily_flow": (
                statistics.mean(daily_cash_flow) if daily_cash_flow else 0
            ),
            "cash_flow_volatility": (
                statistics.stdev(daily_cash_flow) if len(daily_cash_flow) > 1 else 0
            ),
            "positive_flow_days": sum(1 for cf in daily_cash_flow if cf > 0),
            "negative_flow_days": sum(1 for cf in daily_cash_flow if cf < 0),
        }

        return analysis

    def _categorize_spending(
        self, transactions: List[Dict[str, Any]]
    ) -> Dict[str, float]:
        """Categorize spending by category"""
        spending = {}
        for txn in transactions:
            if txn.get("type") == "expense":
                category = txn.get("category", "Other")
                amount = txn.get("amount", 0)
                spending[category] = spending.get(category, 0) + amount
        return spending

    def _categorize_income(
        self, transactions: List[Dict[str, Any]]
    ) -> Dict[str, float]:
        """Categorize income by source"""
        income = {}
        for txn in transactions:
            source = txn.get("source", "Other")
            amount = txn.get("amount", 0)
            income[source] = income.get(source, 0) + amount
        return income

    def _calculate_daily_spending(
        self, transactions: List[Dict[str, Any]]
    ) -> List[float]:
        """Calculate daily spending amounts"""
        daily_spending = {}
        for txn in transactions:
            if txn.get("type") == "expense":
                date = txn.get("date", "").split("T")[0]
                amount = txn.get("amount", 0)
                daily_spending[date] = daily_spending.get(date, 0) + amount
        return list(daily_spending.values())

    def _calculate_weekly_spending(
        self, transactions: List[Dict[str, Any]]
    ) -> List[float]:
        """Calculate weekly spending amounts"""
        weekly_spending = {}
        for txn in transactions:
            if txn.get("type") == "expense":
                date = datetime.fromisoformat(txn.get("date", ""))
                week = date.isocalendar()[1]
                amount = txn.get("amount", 0)
                weekly_spending[week] = weekly_spending.get(week, 0) + amount
        return list(weekly_spending.values())

    def _calculate_monthly_income(
        self, transactions: List[Dict[str, Any]]
    ) -> Dict[str, float]:
        """Calculate monthly income"""
        monthly_income = {}
        for txn in transactions:
            date = datetime.fromisoformat(txn.get("date", ""))
            month = date.strftime("%Y-%m")
            amount = txn.get("amount", 0)
            monthly_income[month] = monthly_income.get(month, 0) + amount
        return monthly_income

    def _identify_spending_patterns(
        self, daily_spending: List[float], weekly_spending: List[float]
    ) -> List[str]:
        """Identify spending patterns"""
        patterns = []
        
        if daily_spending:
            avg_daily = statistics.mean(daily_spending)
            if statistics.stdev(daily_spending) if len(daily_spending) > 1 else 0 > avg_daily * 0.5:
                patterns.append("High spending volatility")
        
        if weekly_spending:
            if len(weekly_spending) > 1:
                trend = self._calculate_trend(
                    {str(i): v for i, v in enumerate(weekly_spending)}
                )
                if trend == "increasing":
                    patterns.append("Spending trend is increasing")
                elif trend == "decreasing":
                    patterns.append("Spending trend is decreasing")
        
        return patterns

    def _detect_spending_anomalies(self, daily_spending: List[float]) -> List[str]:
        """Detect spending anomalies"""
        anomalies = []
        
        if not daily_spending or len(daily_spending) < 3:
            return anomalies
        
        mean = statistics.mean(daily_spending)
        std_dev = statistics.stdev(daily_spending)
        
        for spending in daily_spending:
            if abs(spending - mean) > 2 * std_dev:
                anomalies.append(f"Unusual spending detected: ${spending:.2f}")
        
        return anomalies[:5]

    def _calculate_stability(self, amounts: List[float]) -> float:
        """Calculate income stability (0-1, higher is more stable)"""
        if not amounts or len(amounts) < 2:
            return 1.0
        
        mean = statistics.mean(amounts)
        std_dev = statistics.stdev(amounts)
        
        # Coefficient of variation
        cv = (std_dev / mean) if mean > 0 else 1.0
        stability = max(0, 1 - cv)
        
        return min(1.0, stability)

    def _calculate_trend(self, data: Dict[str, float]) -> str:
        """Calculate trend direction"""
        if len(data) < 2:
            return "insufficient_data"
        
        values = list(data.values())
        first_half = statistics.mean(values[: len(values) // 2])
        second_half = statistics.mean(values[len(values) // 2 :])
        
        if second_half > first_half * 1.05:
            return "increasing"
        elif second_half < first_half * 0.95:
            return "decreasing"
        else:
            return "stable"

    def _project_annual_income(self, monthly_income: Dict[str, float]) -> float:
        """Project annual income based on monthly data"""
        if not monthly_income:
            return 0
        
        avg_monthly = statistics.mean(monthly_income.values())
        return avg_monthly * 12

    def _categorize_savings_rate(self, rate: float) -> str:
        """Categorize savings rate"""
        if rate < 5:
            return "Very Low"
        elif rate < 10:
            return "Low"
        elif rate < 20:
            return "Moderate"
        elif rate < 30:
            return "Good"
        else:
            return "Excellent"

    def _get_savings_recommendation(self, rate: float) -> str:
        """Get recommendation based on savings rate"""
        if rate < 10:
            return "Increase savings by reducing discretionary spending"
        elif rate < 20:
            return "Good progress, aim for 20% savings rate"
        elif rate < 30:
            return "Excellent savings rate, consider investment opportunities"
        else:
            return "Outstanding savings rate, focus on wealth building"

    def _calculate_daily_cash_flow(
        self, transactions: List[Dict[str, Any]]
    ) -> List[float]:
        """Calculate daily cash flow"""
        daily_flow = {}
        for txn in transactions:
            date = txn.get("date", "").split("T")[0]
            amount = txn.get("amount", 0)
            txn_type = txn.get("type", "")
            
            flow = amount if txn_type == "income" else -amount
            daily_flow[date] = daily_flow.get(date, 0) + flow
        
        return list(daily_flow.values())

    def _calculate_cumulative_flow(self, daily_flow: List[float]) -> List[float]:
        """Calculate cumulative cash flow"""
        cumulative = []
        total = 0
        for flow in daily_flow:
            total += flow
            cumulative.append(total)
        return cumulative
