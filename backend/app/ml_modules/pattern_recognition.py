"""Pattern Recognition - Advanced ML module for detecting financial patterns and anomalies"""
from typing import Dict, List, Tuple
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.transaction import Transaction
import statistics
from collections import defaultdict

class PatternRecognition:
    """Advanced Machine Learning module for pattern recognition and anomaly detection"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def detect_all_patterns(self, user_id: int) -> Dict:
        """Detect all financial patterns for a user"""
        patterns = {
            "spending_patterns": self._detect_spending_patterns(user_id),
            "temporal_patterns": self._detect_temporal_patterns(user_id),
            "behavioral_patterns": self._detect_behavioral_patterns(user_id),
            "anomalies": self._detect_advanced_anomalies(user_id),
            "correlations": self._detect_spending_correlations(user_id)
        }
        
        return {
            "status": "success",
            "user_id": user_id,
            "patterns": patterns,
            "analysis_timestamp": datetime.utcnow().isoformat()
        }
    
    def _detect_spending_patterns(self, user_id: int) -> Dict:
        """Detect spending patterns across categories and time"""
        ninety_days_ago = datetime.utcnow() - timedelta(days=90)
        
        transactions = self.db.query(Transaction).filter(
            Transaction.user_id == user_id,
            Transaction.type == "expense",
            Transaction.transaction_date >= ninety_days_ago
        ).all()
        
        if not transactions:
            return {"status": "insufficient_data"}
        
        patterns = []
        
        # Category-based patterns
        category_data = defaultdict(list)
        for t in transactions:
            category_data[t.category].append(t.amount)
        
        for category, amounts in category_data.items():
            if len(amounts) >= 5:
                avg = statistics.mean(amounts)
                std_dev = statistics.stdev(amounts) if len(amounts) > 1 else 0
                
                # Identify pattern type
                pattern_type = self._classify_spending_pattern(amounts, avg, std_dev)
                
                patterns.append({
                    "category": category,
                    "pattern_type": pattern_type,
                    "average_transaction": round(avg, 2),
                    "std_deviation": round(std_dev, 2),
                    "transaction_count": len(amounts),
                    "total_spending": round(sum(amounts), 2),
                    "consistency_score": self._calculate_consistency_score(amounts, avg)
                })
        
        return {
            "status": "success",
            "patterns": patterns,
            "total_categories": len(patterns)
        }
    
    def _detect_temporal_patterns(self, user_id: int) -> Dict:
        """Detect temporal patterns (day of week, time of day, etc.)"""
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        
        transactions = self.db.query(Transaction).filter(
            Transaction.user_id == user_id,
            Transaction.type == "expense",
            Transaction.transaction_date >= thirty_days_ago
        ).all()
        
        if not transactions:
            return {"status": "insufficient_data"}
        
        # Day of week analysis
        day_of_week_spending = defaultdict(list)
        day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        
        for t in transactions:
            day_idx = t.transaction_date.weekday()
            day_of_week_spending[day_names[day_idx]].append(t.amount)
        
        # Hour of day analysis
        hour_spending = defaultdict(list)
        for t in transactions:
            hour = t.transaction_date.hour
            hour_spending[hour].append(t.amount)
        
        # Find peak spending times
        peak_day = max(day_of_week_spending.items(), key=lambda x: sum(x[1]))[0] if day_of_week_spending else None
        peak_hour = max(hour_spending.items(), key=lambda x: sum(x[1]))[0] if hour_spending else None
        
        # Day of week patterns
        day_patterns = []
        for day, amounts in day_of_week_spending.items():
            day_patterns.append({
                "day": day,
                "total_spending": round(sum(amounts), 2),
                "average_transaction": round(statistics.mean(amounts), 2),
                "transaction_count": len(amounts)
            })
        
        return {
            "status": "success",
            "day_of_week_patterns": day_patterns,
            "peak_spending_day": peak_day,
            "peak_spending_hour": peak_hour,
            "hourly_distribution": {
                str(hour): {
                    "total": round(sum(amounts), 2),
                    "count": len(amounts)
                }
                for hour, amounts in hour_spending.items()
            }
        }
    
    def _detect_behavioral_patterns(self, user_id: int) -> Dict:
        """Detect behavioral patterns in spending"""
        ninety_days_ago = datetime.utcnow() - timedelta(days=90)
        
        transactions = self.db.query(Transaction).filter(
            Transaction.user_id == user_id,
            Transaction.type == "expense",
            Transaction.transaction_date >= ninety_days_ago
        ).all()
        
        if not transactions:
            return {"status": "insufficient_data"}
        
        behaviors = []
        
        # Impulse buying pattern
        small_transactions = [t for t in transactions if t.amount < 50]
        if len(small_transactions) > len(transactions) * 0.5:
            behaviors.append({
                "behavior": "frequent_small_purchases",
                "severity": "medium",
                "description": f"{len(small_transactions)} small purchases detected",
                "percentage": round((len(small_transactions) / len(transactions)) * 100, 1),
                "recommendation": "Consider consolidating purchases to reduce transaction frequency"
            })
        
        # Large purchase pattern
        large_transactions = [t for t in transactions if t.amount > 500]
        if large_transactions:
            behaviors.append({
                "behavior": "large_purchases",
                "severity": "low",
                "description": f"{len(large_transactions)} large purchases detected",
                "average_large_purchase": round(statistics.mean([t.amount for t in large_transactions]), 2),
                "recommendation": "Monitor large purchases for budget impact"
            })
        
        # Recurring transaction pattern
        recurring_patterns = self._detect_recurring_transactions(transactions)
        if recurring_patterns:
            behaviors.append({
                "behavior": "recurring_transactions",
                "severity": "low",
                "description": f"{len(recurring_patterns)} recurring transaction patterns detected",
                "patterns": recurring_patterns,
                "recommendation": "Consider setting up automatic payments for recurring expenses"
            })
        
        # Spending velocity
        transactions_per_day = len(transactions) / 90
        if transactions_per_day > 2:
            behaviors.append({
                "behavior": "high_transaction_velocity",
                "severity": "medium",
                "description": f"Average {transactions_per_day:.1f} transactions per day",
                "recommendation": "High transaction frequency may indicate impulse spending"
            })
        
        return {
            "status": "success",
            "behaviors": behaviors,
            "total_behaviors_detected": len(behaviors)
        }
    
    def _detect_advanced_anomalies(self, user_id: int) -> Dict:
        """Detect advanced anomalies using statistical methods"""
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        
        transactions = self.db.query(Transaction).filter(
            Transaction.user_id == user_id,
            Transaction.type == "expense",
            Transaction.transaction_date >= thirty_days_ago
        ).all()
        
        if not transactions:
            return {"status": "insufficient_data"}
        
        anomalies = []
        
        # Outlier detection using IQR method
        amounts = [t.amount for t in transactions]
        if len(amounts) >= 4:
            sorted_amounts = sorted(amounts)
            q1 = sorted_amounts[len(sorted_amounts) // 4]
            q3 = sorted_amounts[3 * len(sorted_amounts) // 4]
            iqr = q3 - q1
            
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr
            
            for t in transactions:
                if t.amount > upper_bound:
                    anomalies.append({
                        "transaction_id": t.id,
                        "amount": round(t.amount, 2),
                        "category": t.category,
                        "date": t.transaction_date.isoformat(),
                        "anomaly_type": "outlier_high",
                        "severity": "high" if t.amount > upper_bound * 1.5 else "medium",
                        "description": f"Transaction amount ${t.amount:.2f} is significantly higher than typical"
                    })
        
        # Duplicate detection
        transaction_signatures = defaultdict(list)
        for t in transactions:
            sig = (t.category, round(t.amount, 2))
            transaction_signatures[sig].append(t)
        
        for sig, trans_list in transaction_signatures.items():
            if len(trans_list) > 2:
                # Check if they're close in time
                dates = sorted([t.transaction_date for t in trans_list])
                for i in range(len(dates) - 1):
                    if (dates[i+1] - dates[i]).days <= 1:
                        anomalies.append({
                            "anomaly_type": "potential_duplicate",
                            "severity": "medium",
                            "category": sig[0],
                            "amount": sig[1],
                            "count": len(trans_list),
                            "description": f"Multiple similar transactions detected"
                        })
                        break
        
        return {
            "status": "success",
            "anomalies": anomalies,
            "total_anomalies": len(anomalies)
        }
    
    def _detect_spending_correlations(self, user_id: int) -> Dict:
        """Detect correlations between spending categories"""
        ninety_days_ago = datetime.utcnow() - timedelta(days=90)
        
        transactions = self.db.query(Transaction).filter(
            Transaction.user_id == user_id,
            Transaction.type == "expense",
            Transaction.transaction_date >= ninety_days_ago
        ).all()
        
        if not transactions:
            return {"status": "insufficient_data"}
        
        # Group by week
        weekly_spending = defaultdict(lambda: defaultdict(float))
        for t in transactions:
            week_key = t.transaction_date.isocalendar()[1]
            weekly_spending[week_key][t.category] += t.amount
        
        correlations = []
        categories = set(t.category for t in transactions)
        
        # Simple correlation detection
        for cat1 in categories:
            for cat2 in categories:
                if cat1 < cat2:  # Avoid duplicates
                    cat1_values = [weekly_spending[week].get(cat1, 0) for week in weekly_spending]
                    cat2_values = [weekly_spending[week].get(cat2, 0) for week in weekly_spending]
                    
                    if len(cat1_values) > 2 and sum(cat1_values) > 0 and sum(cat2_values) > 0:
                        correlation = self._calculate_correlation(cat1_values, cat2_values)
                        if abs(correlation) > 0.6:
                            correlations.append({
                                "category_1": cat1,
                                "category_2": cat2,
                                "correlation_coefficient": round(correlation, 2),
                                "relationship": "positive" if correlation > 0 else "negative",
                                "strength": "strong" if abs(correlation) > 0.8 else "moderate"
                            })
        
        return {
            "status": "success",
            "correlations": correlations,
            "total_correlations": len(correlations)
        }
    
    @staticmethod
    def _classify_spending_pattern(amounts: List[float], avg: float, std_dev: float) -> str:
        """Classify spending pattern type"""
        if std_dev < avg * 0.2:
            return "consistent"
        elif std_dev > avg * 0.8:
            return "highly_variable"
        else:
            return "moderate_variable"
    
    @staticmethod
    def _calculate_consistency_score(amounts: List[float], avg: float) -> float:
        """Calculate consistency score (0-100)"""
        if not amounts or avg == 0:
            return 0
        std_dev = statistics.stdev(amounts) if len(amounts) > 1 else 0
        coefficient_of_variation = (std_dev / avg) * 100
        consistency = max(0, 100 - coefficient_of_variation)
        return round(min(100, consistency), 1)
    
    @staticmethod
    def _detect_recurring_transactions(transactions: List) -> List[Dict]:
        """Detect recurring transaction patterns"""
        recurring = defaultdict(list)
        
        for t in transactions:
            sig = (t.category, round(t.amount, 2))
            recurring[sig].append(t.transaction_date)
        
        patterns = []
        for sig, dates in recurring.items():
            if len(dates) >= 3:
                sorted_dates = sorted(dates)
                intervals = [(sorted_dates[i+1] - sorted_dates[i]).days for i in range(len(sorted_dates)-1)]
                
                if intervals:
                    avg_interval = statistics.mean(intervals)
                    if 25 <= avg_interval <= 35:  # Monthly pattern
                        patterns.append({
                            "category": sig[0],
                            "amount": sig[1],
                            "frequency": "monthly",
                            "occurrences": len(dates)
                        })
                    elif 5 <= avg_interval <= 8:  # Weekly pattern
                        patterns.append({
                            "category": sig[0],
                            "amount": sig[1],
                            "frequency": "weekly",
                            "occurrences": len(dates)
                        })
        
        return patterns
    
    @staticmethod
    def _calculate_correlation(x: List[float], y: List[float]) -> float:
        """Calculate Pearson correlation coefficient"""
        if len(x) != len(y) or len(x) < 2:
            return 0
        
        mean_x = statistics.mean(x)
        mean_y = statistics.mean(y)
        
        numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(len(x)))
        denominator = (
            (sum((xi - mean_x) ** 2 for xi in x) ** 0.5) *
            (sum((yi - mean_y) ** 2 for yi in y) ** 0.5)
        )
        
        if denominator == 0:
            return 0
        
        return numerator / denominator
