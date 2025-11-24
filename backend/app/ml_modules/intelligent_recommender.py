"""Intelligent Recommender - ML module for personalized financial recommendations based on patterns"""
from typing import Dict, List, Tuple
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.transaction import Transaction
from app.models.goal import Goal
import statistics

class IntelligentRecommender:
    """Machine Learning module for generating intelligent financial recommendations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_personalized_recommendations(self, user_id: int) -> Dict:
        """Generate personalized recommendations based on user's financial patterns"""
        recommendations = []
        
        # Analyze spending patterns
        spending_analysis = self._analyze_spending_patterns(user_id)
        if spending_analysis:
            recommendations.extend(spending_analysis)
        
        # Analyze savings potential
        savings_analysis = self._analyze_savings_potential(user_id)
        if savings_analysis:
            recommendations.extend(savings_analysis)
        
        # Analyze category trends
        category_analysis = self._analyze_category_trends(user_id)
        if category_analysis:
            recommendations.extend(category_analysis)
        
        # Analyze goal progress
        goal_analysis = self._analyze_goal_progress(user_id)
        if goal_analysis:
            recommendations.extend(goal_analysis)
        
        # Analyze budget efficiency
        budget_analysis = self._analyze_budget_efficiency(user_id)
        if budget_analysis:
            recommendations.extend(budget_analysis)
        
        # Sort by priority score
        recommendations.sort(key=lambda x: x.get('priority_score', 0), reverse=True)
        
        return {
            "status": "success",
            "total_recommendations": len(recommendations),
            "recommendations": recommendations[:10],  # Top 10 recommendations
            "generated_at": datetime.utcnow().isoformat()
        }
    
    def _analyze_spending_patterns(self, user_id: int) -> List[Dict]:
        """Analyze spending patterns and generate recommendations"""
        recommendations = []
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        
        recent_transactions = self.db.query(Transaction).filter(
            Transaction.user_id == user_id,
            Transaction.type == "expense",
            Transaction.transaction_date >= thirty_days_ago
        ).all()
        
        if not recent_transactions:
            return recommendations
        
        # Group by category
        category_spending = {}
        for transaction in recent_transactions:
            if transaction.category not in category_spending:
                category_spending[transaction.category] = []
            category_spending[transaction.category].append(transaction.amount)
        
        # Analyze each category
        for category, amounts in category_spending.items():
            total = sum(amounts)
            avg = total / len(amounts)
            
            # Check for high-frequency small purchases
            small_purchases = [a for a in amounts if a < 50]
            if len(small_purchases) > len(amounts) * 0.6:
                recommendations.append({
                    "type": "consolidation",
                    "category": category,
                    "title": f"Consolidate {category} purchases",
                    "description": f"You have {len(small_purchases)} small purchases in {category}. Consider consolidating to save time and potentially reduce costs.",
                    "potential_savings": round(avg * 0.1, 2),
                    "priority_score": 7,
                    "action": f"Review and consolidate {category} purchases"
                })
            
            # Check for high spending categories
            if total > 500:
                recommendations.append({
                    "type": "budget_review",
                    "category": category,
                    "title": f"Review {category} spending",
                    "description": f"Your {category} spending is ${total:.2f} in the last 30 days. Consider setting a budget limit.",
                    "current_spending": round(total, 2),
                    "priority_score": 6,
                    "action": f"Set a budget limit for {category}"
                })
        
        return recommendations
    
    def _analyze_savings_potential(self, user_id: int) -> List[Dict]:
        """Analyze potential savings opportunities"""
        recommendations = []
        ninety_days_ago = datetime.utcnow() - timedelta(days=90)
        
        transactions = self.db.query(Transaction).filter(
            Transaction.user_id == user_id,
            Transaction.type == "expense",
            Transaction.transaction_date >= ninety_days_ago
        ).all()
        
        if not transactions:
            return recommendations
        
        # Calculate total spending
        total_spending = sum(t.amount for t in transactions)
        
        # Identify discretionary spending
        discretionary_categories = ['entertainment', 'dining', 'shopping', 'subscriptions']
        discretionary_spending = sum(
            t.amount for t in transactions 
            if t.category.lower() in discretionary_categories
        )
        
        if discretionary_spending > 0:
            savings_potential = discretionary_spending * 0.2  # 20% reduction potential
            recommendations.append({
                "type": "savings_opportunity",
                "title": "Reduce discretionary spending",
                "description": f"You spend ${discretionary_spending:.2f} on discretionary items. Reducing by 20% could save ${savings_potential:.2f}.",
                "potential_savings": round(savings_potential, 2),
                "priority_score": 8,
                "action": "Review discretionary spending categories"
            })
        
        # Check for subscription services
        subscription_transactions = [t for t in transactions if 'subscription' in t.description.lower() or 'subscription' in t.category.lower()]
        if subscription_transactions:
            subscription_total = sum(t.amount for t in subscription_transactions)
            recommendations.append({
                "type": "subscription_audit",
                "title": "Audit your subscriptions",
                "description": f"You have {len(subscription_transactions)} subscription transactions totaling ${subscription_total:.2f}. Review unused subscriptions.",
                "current_subscriptions": len(subscription_transactions),
                "priority_score": 7,
                "action": "Review and cancel unused subscriptions"
            })
        
        return recommendations
    
    def _analyze_category_trends(self, user_id: int) -> List[Dict]:
        """Analyze trends in spending categories"""
        recommendations = []
        
        # Compare last month vs previous month
        current_month_start = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        previous_month_start = (current_month_start - timedelta(days=1)).replace(day=1)
        
        current_month_transactions = self.db.query(Transaction).filter(
            Transaction.user_id == user_id,
            Transaction.type == "expense",
            Transaction.transaction_date >= current_month_start
        ).all()
        
        previous_month_transactions = self.db.query(Transaction).filter(
            Transaction.user_id == user_id,
            Transaction.type == "expense",
            Transaction.transaction_date >= previous_month_start,
            Transaction.transaction_date < current_month_start
        ).all()
        
        if not previous_month_transactions:
            return recommendations
        
        # Group by category
        current_categories = {}
        for t in current_month_transactions:
            current_categories[t.category] = current_categories.get(t.category, 0) + t.amount
        
        previous_categories = {}
        for t in previous_month_transactions:
            previous_categories[t.category] = previous_categories.get(t.category, 0) + t.amount
        
        # Find categories with significant increases
        for category, current_amount in current_categories.items():
            previous_amount = previous_categories.get(category, 0)
            if previous_amount > 0:
                increase_pct = ((current_amount - previous_amount) / previous_amount) * 100
                if increase_pct > 30:
                    recommendations.append({
                        "type": "trend_alert",
                        "category": category,
                        "title": f"{category} spending increased",
                        "description": f"Your {category} spending increased by {increase_pct:.1f}% compared to last month.",
                        "increase_percentage": round(increase_pct, 1),
                        "priority_score": 7,
                        "action": f"Investigate {category} spending increase"
                    })
        
        return recommendations
    
    def _analyze_goal_progress(self, user_id: int) -> List[Dict]:
        """Analyze financial goal progress and provide recommendations"""
        recommendations = []
        
        goals = self.db.query(Goal).filter(Goal.user_id == user_id).all()
        
        for goal in goals:
            if goal.status == "active":
                progress_pct = (goal.current_amount / goal.target_amount * 100) if goal.target_amount > 0 else 0
                
                if progress_pct < 25:
                    recommendations.append({
                        "type": "goal_acceleration",
                        "goal_id": goal.id,
                        "title": f"Accelerate progress on {goal.name}",
                        "description": f"You're only {progress_pct:.1f}% towards your goal of ${goal.target_amount:.2f}. Consider increasing contributions.",
                        "current_progress": round(progress_pct, 1),
                        "priority_score": 8,
                        "action": f"Increase contributions to {goal.name}"
                    })
                elif progress_pct > 75:
                    recommendations.append({
                        "type": "goal_milestone",
                        "goal_id": goal.id,
                        "title": f"You're close to achieving {goal.name}",
                        "description": f"You've reached {progress_pct:.1f}% of your goal. Keep up the momentum!",
                        "current_progress": round(progress_pct, 1),
                        "priority_score": 5,
                        "action": f"Maintain contributions to {goal.name}"
                    })
        
        return recommendations
    
    def _analyze_budget_efficiency(self, user_id: int) -> List[Dict]:
        """Analyze budget efficiency and provide recommendations"""
        recommendations = []
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        
        transactions = self.db.query(Transaction).filter(
            Transaction.user_id == user_id,
            Transaction.transaction_date >= thirty_days_ago
        ).all()
        
        if not transactions:
            return recommendations
        
        income = sum(t.amount for t in transactions if t.type == "income")
        expenses = sum(t.amount for t in transactions if t.type == "expense")
        
        if income > 0:
            expense_ratio = (expenses / income) * 100
            
            if expense_ratio > 90:
                recommendations.append({
                    "type": "budget_warning",
                    "title": "High expense-to-income ratio",
                    "description": f"You're spending {expense_ratio:.1f}% of your income. Consider reducing expenses or increasing income.",
                    "expense_ratio": round(expense_ratio, 1),
                    "priority_score": 9,
                    "action": "Review and reduce expenses"
                })
            elif expense_ratio < 50:
                savings_amount = income - expenses
                recommendations.append({
                    "type": "savings_opportunity",
                    "title": "Great savings rate!",
                    "description": f"You're only spending {expense_ratio:.1f}% of your income. Consider investing the surplus.",
                    "monthly_surplus": round(savings_amount, 2),
                    "priority_score": 6,
                    "action": "Invest or save the surplus"
                })
        
        return recommendations
    
    def get_category_recommendations(self, user_id: int, category: str) -> Dict:
        """Get specific recommendations for a spending category"""
        ninety_days_ago = datetime.utcnow() - timedelta(days=90)
        
        category_transactions = self.db.query(Transaction).filter(
            Transaction.user_id == user_id,
            Transaction.type == "expense",
            Transaction.category == category,
            Transaction.transaction_date >= ninety_days_ago
        ).all()
        
        if not category_transactions:
            return {"status": "no_data", "category": category}
        
        amounts = [t.amount for t in category_transactions]
        total = sum(amounts)
        avg = total / len(amounts)
        
        recommendations = []
        
        # High variance analysis
        if len(amounts) > 1:
            std_dev = statistics.stdev(amounts)
            if std_dev > avg * 0.5:
                recommendations.append({
                    "type": "consistency",
                    "title": f"Stabilize {category} spending",
                    "description": f"Your {category} spending varies significantly. Try to maintain more consistent spending.",
                    "variance": round(std_dev, 2),
                    "action": f"Plan {category} purchases more consistently"
                })
        
        # Frequency analysis
        frequency = len(category_transactions) / 3  # Per month
        if frequency > 20:
            recommendations.append({
                "type": "frequency",
                "title": f"Reduce {category} transaction frequency",
                "description": f"You make {frequency:.0f} {category} transactions per month. Consider batch purchasing.",
                "frequency": round(frequency, 1),
                "action": f"Batch {category} purchases"
            })
        
        return {
            "status": "success",
            "category": category,
            "total_spending": round(total, 2),
            "average_transaction": round(avg, 2),
            "transaction_count": len(category_transactions),
            "recommendations": recommendations
        }
