# FinCoach AI - Phase 3: Intelligent Recommendations & Pattern Recognition

## Overview
Phase 3 introduces two powerful ML modules that enhance the FinCoach AI system with intelligent recommendations and advanced pattern recognition capabilities.

## New Features

### 1. 💡 Intelligent Recommendations Module
**File:** `app/ml_modules/intelligent_recommender.py`

#### Features:
- **Personalized Recommendations**: Generates tailored financial recommendations based on user spending patterns
- **Spending Pattern Analysis**: Analyzes spending habits across categories
- **Savings Opportunity Detection**: Identifies potential areas to reduce spending
- **Category Trend Analysis**: Tracks spending trends across categories
- **Goal Progress Monitoring**: Provides recommendations based on financial goal progress
- **Budget Efficiency Analysis**: Evaluates expense-to-income ratios

#### Key Methods:
```python
# Get personalized recommendations
recommender.get_personalized_recommendations(user_id)

# Get category-specific recommendations
recommender.get_category_recommendations(user_id, category)
```

#### API Endpoints:
- `GET /api/v1/recommendations/personalized` - Get all personalized recommendations
- `GET /api/v1/recommendations/category/{category}` - Get recommendations for specific category

#### Recommendation Types:
1. **Consolidation**: Suggests consolidating multiple small purchases
2. **Budget Review**: Recommends reviewing high-spending categories
3. **Savings Opportunity**: Identifies discretionary spending that can be reduced
4. **Subscription Audit**: Detects and recommends auditing subscriptions
5. **Trend Alert**: Alerts about significant spending increases
6. **Goal Acceleration**: Recommends increasing contributions to financial goals
7. **Goal Milestone**: Celebrates progress towards goals
8. **Budget Warning**: Alerts when expense-to-income ratio is too high

### 2. 🤖 Pattern Recognition Module
**File:** `app/ml_modules/pattern_recognition.py`

#### Features:
- **Spending Pattern Detection**: Identifies consistent spending patterns across categories
- **Temporal Pattern Analysis**: Detects day-of-week and time-of-day spending patterns
- **Behavioral Pattern Recognition**: Identifies spending behaviors (impulse buying, large purchases, etc.)
- **Advanced Anomaly Detection**: Uses statistical methods (IQR) to detect outliers
- **Spending Correlations**: Identifies correlations between spending categories
- **Recurring Transaction Detection**: Identifies recurring expenses

#### Key Methods:
```python
# Detect all patterns
pattern_detector.detect_all_patterns(user_id)

# Detect specific pattern types
pattern_detector._detect_spending_patterns(user_id)
pattern_detector._detect_temporal_patterns(user_id)
pattern_detector._detect_behavioral_patterns(user_id)
pattern_detector._detect_advanced_anomalies(user_id)
pattern_detector._detect_spending_correlations(user_id)
```

#### API Endpoints:
- `GET /api/v1/patterns/all` - Detect all patterns
- `GET /api/v1/patterns/spending` - Detect spending patterns
- `GET /api/v1/patterns/temporal` - Detect temporal patterns
- `GET /api/v1/patterns/behavioral` - Detect behavioral patterns
- `GET /api/v1/patterns/anomalies` - Detect advanced anomalies
- `GET /api/v1/patterns/correlations` - Detect spending correlations

#### Pattern Types:

##### Spending Patterns:
- **Consistent**: Low variance in spending (std_dev < 20% of average)
- **Moderate Variable**: Medium variance (20-80% of average)
- **Highly Variable**: High variance (std_dev > 80% of average)

##### Temporal Patterns:
- Day-of-week spending distribution
- Hour-of-day spending distribution
- Peak spending times

##### Behavioral Patterns:
- Frequent small purchases (impulse buying)
- Large purchases
- Recurring transactions
- High transaction velocity

##### Anomalies:
- Outlier transactions (using IQR method)
- Potential duplicate transactions
- Unusual spending spikes

##### Correlations:
- Positive correlations between categories
- Negative correlations between categories
- Correlation strength (moderate/strong)

## Technical Details

### Machine Learning Algorithms Used:

1. **Exponential Smoothing**: For spending predictions
2. **Z-Score Analysis**: For anomaly detection
3. **Interquartile Range (IQR)**: For outlier detection
4. **Pearson Correlation**: For category correlations
5. **Statistical Analysis**: Mean, standard deviation, variance calculations

### Data Processing:

- **Time Windows**: 30-day, 90-day, and 6-month analysis windows
- **Category Grouping**: Transactions grouped by category
- **Temporal Grouping**: Transactions grouped by day, week, and hour
- **Statistical Calculations**: Mean, median, standard deviation, variance

## Integration

### Updated Files:
1. `app/ml_modules/__init__.py` - Added new module exports
2. `app/main.py` - Added new API routes
3. `app/api/__init__.py` - Added new API module imports

### New Files:
1. `app/ml_modules/intelligent_recommender.py` - Intelligent recommendations
2. `app/ml_modules/pattern_recognition.py` - Pattern recognition
3. `app/api/intelligent_recommendations.py` - Recommendations API
4. `app/api/pattern_recognition.py` - Pattern recognition API

## Usage Examples

### Get Personalized Recommendations:
```bash
curl -X GET "http://localhost:8000/api/v1/recommendations/personalized" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Get Category Recommendations:
```bash
curl -X GET "http://localhost:8000/api/v1/recommendations/category/dining" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Detect All Patterns:
```bash
curl -X GET "http://localhost:8000/api/v1/patterns/all" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Detect Spending Patterns:
```bash
curl -X GET "http://localhost:8000/api/v1/patterns/spending" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Detect Anomalies:
```bash
curl -X GET "http://localhost:8000/api/v1/patterns/anomalies" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Response Examples

### Personalized Recommendations Response:
```json
{
  "status": "success",
  "total_recommendations": 5,
  "recommendations": [
    {
      "type": "budget_warning",
      "title": "High expense-to-income ratio",
      "description": "You're spending 92% of your income...",
      "priority_score": 9,
      "action": "Review and reduce expenses"
    },
    {
      "type": "savings_opportunity",
      "title": "Reduce discretionary spending",
      "description": "You spend $450 on discretionary items...",
      "potential_savings": 90.0,
      "priority_score": 8,
      "action": "Review discretionary spending categories"
    }
  ],
  "generated_at": "2025-11-25T01:05:00"
}
```

### Pattern Detection Response:
```json
{
  "status": "success",
  "patterns": {
    "spending_patterns": {
      "status": "success",
      "patterns": [
        {
          "category": "dining",
          "pattern_type": "moderate_variable",
          "average_transaction": 25.50,
          "std_deviation": 12.30,
          "transaction_count": 15,
          "total_spending": 382.50,
          "consistency_score": 75.5
        }
      ]
    },
    "temporal_patterns": {
      "status": "success",
      "peak_spending_day": "Friday",
      "peak_spending_hour": 19
    },
    "behavioral_patterns": {
      "status": "success",
      "behaviors": [
        {
          "behavior": "frequent_small_purchases",
          "severity": "medium",
          "description": "12 small purchases detected",
          "percentage": 65.2
        }
      ]
    },
    "anomalies": {
      "status": "success",
      "anomalies": [],
      "total_anomalies": 0
    }
  }
}
```

## Performance Considerations

- **Database Queries**: Optimized with time-window filtering
- **Computation**: Efficient statistical calculations
- **Memory**: Minimal memory footprint for large datasets
- **Scalability**: Designed to handle thousands of transactions

## Future Enhancements

1. **Machine Learning Models**: Implement scikit-learn for advanced ML
2. **Deep Learning**: LSTM networks for time-series forecasting
3. **Real-time Processing**: Stream processing for real-time recommendations
4. **Personalization**: User preference learning
5. **Explainability**: SHAP values for recommendation explanations
6. **A/B Testing**: Test recommendation effectiveness

## Version
- **Version**: 1.3.0
- **Release Date**: November 25, 2025
- **Status**: Production Ready
