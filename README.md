# 🏦 FINCoach AI - AI-Powered Personal Finance Management System

![Version](https://img.shields.io/badge/version-1.2.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-Production%20Ready-brightgreen.svg)

## 📋 Overview

**FINCoach AI** is a comprehensive, AI-powered personal finance management system that combines advanced analytics, machine learning, and multi-agent AI orchestration to provide intelligent financial guidance and decision-making support.

### 🎯 Key Features

- **🤖 Multi-Agent AI System**: Collaborative AI agents (Financial Advisor, Risk Assessor, Prediction Agent, Coaching Agent, Portfolio Optimizer, Market Analyst)
- **📊 Advanced Analytics**: Spending patterns, income trends, savings rate, budget variance, and cash flow analysis
- **🔮 Predictive Insights**: Spending forecasts, income projections, savings predictions, and financial health assessment
- **💰 Transaction Management**: Track income and expenses with automatic categorization
- **🎯 Goal Tracking**: Set and monitor financial goals with progress tracking
- **🏺 Jar System**: Allocate funds to different savings categories
- **⚠️ Smart Alerts**: Real-time notifications for budget overruns and financial anomalies
- **📱 Mobile Integration**: Seamless mobile app support
- **🔔 Real-time Notifications**: Instant alerts for important financial events
- **👥 Social Features**: Share achievements and connect with other users

---

## 🏗️ Architecture

### Technology Stack

**Backend:**
- FastAPI (Python)
- PostgreSQL Database
- SQLAlchemy ORM
- Pydantic for data validation
- JWT Authentication

**Frontend:**
- React 19
- Vite
- Tailwind CSS
- Recharts for visualizations
- Zustand for state management
- React Router for navigation

**AI/ML:**
- Multi-Agent Orchestration System
- Advanced Analytics Engine
- Predictive Insights Engine
- Machine Learning Modules

---

## 📁 Project Structure

```
FinCoach-AI/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── auth.py                 # Authentication endpoints
│   │   │   ├── users.py                # User management
│   │   │   ├── transactions.py         # Transaction management
│   │   │   ├── jars.py                 # Jar system
│   │   │   ├── goals.py                # Goal tracking
│   │   │   ├── alerts.py               # Alert system
│   │   │   ├── advanced_analytics.py   # Advanced analytics endpoints
│   │   │   ├── predictive_insights.py  # Predictive insights endpoints
│   │   │   ├── multi_agent_system.py   # Multi-agent system endpoints
│   │   │   ├── agents.py               # AI agents endpoints
│   │   │   ├── ml_modules.py           # ML modules endpoints
│   │   │   ├── analytics.py            # Analytics endpoints
│   │   │   ├── mobile.py               # Mobile integration
│   │   │   ├── notifications.py        # Notifications
│   │   │   └── social.py               # Social features
│   │   ├── agents/
│   │   │   ├── financial_advisor.py    # Financial advisor agent
│   │   │   ├── risk_assessor.py        # Risk assessment agent
│   │   │   ├── prediction_agent.py     # Prediction agent
│   │   │   ├── coaching_agent.py       # Coaching agent
│   │   │   └── multi_agent_orchestrator.py  # Agent orchestration
│   │   ├── ml_modules/
│   │   │   ├── advanced_analytics.py   # Advanced analytics engine
│   │   │   └── predictive_insights.py  # Predictive insights engine
│   │   ├── core/
│   │   │   ├── config.py               # Configuration
│   │   │   ├── database.py             # Database setup
│   │   │   └── security.py             # Security utilities
│   │   ├── models/
│   │   │   ├── user.py                 # User model
│   │   │   ├── transaction.py          # Transaction model
│   │   │   ├── jar.py                  # Jar model
│   │   │   ├── goal.py                 # Goal model
│   │   │   └── alert.py                # Alert model
│   │   └── main.py                     # FastAPI application
│   ├── requirements.txt
│   ├── setup.sh
│   └── README.md
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Login.jsx               # Login page
│   │   │   ├── Register.jsx            # Registration page
│   │   │   ├── Dashboard.jsx           # Main dashboard
│   │   │   ├── Analytics.jsx           # Advanced analytics page
│   │   │   ├── Predictions.jsx         # Predictive insights page
│   │   │   └── MultiAgent.jsx          # Multi-agent system page
│   │   ├── components/
│   │   │   └── Navbar.jsx              # Navigation bar
│   │   ├── services/
│   │   │   └── apiClient.js            # API client
│   │   ├── config/
│   │   │   └── api.js                  # API endpoints configuration
│   │   ├── store/
│   │   │   └── authStore.js            # Authentication store
│   │   ├── App.jsx                     # Main app component
│   │   └── main.jsx                    # Entry point
│   ├── package.json
│   ├── vite.config.js
│   └── README.md
├── DEPLOYMENT_GUIDE.md
├── SETUP_GUIDE.md
├── NEW_FEATURES_DOCUMENTATION.md
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- PostgreSQL 12+
- Git

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run setup script
bash setup.sh

# Start the server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: `http://localhost:8000`
API Documentation: `http://localhost:8000/docs`

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will be available at: `http://localhost:5173`

---

## 📚 API Documentation

### Core Endpoints

#### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login user
- `POST /api/v1/auth/refresh` - Refresh token

#### Users
- `GET /api/v1/users/me` - Get current user profile
- `GET /api/v1/users/{id}` - Get user profile

#### Transactions
- `GET /api/v1/transactions` - List transactions
- `POST /api/v1/transactions` - Create transaction
- `GET /api/v1/transactions/{id}` - Get transaction
- `PUT /api/v1/transactions/{id}` - Update transaction
- `DELETE /api/v1/transactions/{id}` - Delete transaction
- `GET /api/v1/transactions/stats/summary` - Get transaction summary

#### Goals
- `GET /api/v1/goals` - List goals
- `POST /api/v1/goals` - Create goal
- `GET /api/v1/goals/{id}` - Get goal
- `PUT /api/v1/goals/{id}` - Update goal
- `DELETE /api/v1/goals/{id}` - Delete goal
- `POST /api/v1/goals/{id}/add-progress` - Add progress to goal

#### Jars
- `GET /api/v1/jars` - List jars
- `POST /api/v1/jars` - Create jar
- `GET /api/v1/jars/{id}` - Get jar
- `PUT /api/v1/jars/{id}` - Update jar
- `DELETE /api/v1/jars/{id}` - Delete jar
- `POST /api/v1/jars/{id}/add-funds` - Add funds to jar

### Advanced Features

#### Advanced Analytics
- `POST /api/v1/analytics/spending-patterns` - Analyze spending patterns
- `POST /api/v1/analytics/income-trends` - Analyze income trends
- `POST /api/v1/analytics/savings-rate` - Calculate savings rate
- `POST /api/v1/analytics/budget-variance` - Analyze budget variance
- `POST /api/v1/analytics/cash-flow` - Analyze cash flow
- `GET /api/v1/analytics/comprehensive-report` - Get comprehensive report

#### Predictive Insights
- `POST /api/v1/predictions/spending-forecast` - Forecast spending
- `POST /api/v1/predictions/income-forecast` - Forecast income
- `POST /api/v1/predictions/savings-projection` - Project savings
- `POST /api/v1/predictions/goal-achievement` - Predict goal achievement
- `POST /api/v1/predictions/financial-health` - Assess financial health
- `POST /api/v1/predictions/anomaly-detection` - Detect anomalies
- `GET /api/v1/predictions/prediction-history` - Get prediction history

#### Multi-Agent System
- `POST /api/v1/multi-agent/execute-task` - Execute collaborative task
- `GET /api/v1/multi-agent/system-status` - Get system status
- `GET /api/v1/multi-agent/agent-history` - Get agent history
- `POST /api/v1/multi-agent/financial-planning` - Execute financial planning
- `POST /api/v1/multi-agent/portfolio-optimization` - Optimize portfolio
- `POST /api/v1/multi-agent/user-coaching` - Get user coaching

---

## 🤖 AI Agents

### Available Agents

1. **Financial Advisor** 💼
   - Provides comprehensive financial planning advice
   - Analyzes financial goals and creates action plans
   - Offers personalized recommendations

2. **Risk Assessor** ⚠️
   - Evaluates financial risks and vulnerabilities
   - Identifies potential financial threats
   - Suggests risk mitigation strategies

3. **Prediction Agent** 🔮
   - Makes financial predictions and forecasts
   - Analyzes trends and patterns
   - Provides confidence intervals for predictions

4. **Coaching Agent** 👨‍🏫
   - Provides personalized financial coaching
   - Tracks progress towards goals
   - Offers motivational guidance

5. **Portfolio Optimizer** 📈
   - Optimizes investment portfolios
   - Suggests asset allocation strategies
   - Rebalances portfolios based on market conditions

6. **Market Analyst** 📊
   - Analyzes market trends and opportunities
   - Provides market insights
   - Identifies investment opportunities

### Agent Collaboration

Agents work together in predefined collaboration patterns:

- **Financial Planning**: Financial Advisor + Risk Assessor + Prediction Agent
- **Portfolio Optimization**: Portfolio Optimizer + Market Analyst + Risk Assessor
- **User Coaching**: Coaching Agent + Financial Advisor + Prediction Agent

---

## 📊 Advanced Analytics Features

### Spending Pattern Analysis
- Categorized spending breakdown
- Daily/weekly spending statistics
- Pattern identification
- Anomaly detection
- Volatility analysis

### Income Analysis
- Income stability scoring
- Source-based income breakdown
- Trend analysis
- Annual income projection

### Savings Rate Calculation
- Savings rate percentage
- Expense ratio analysis
- Target comparison
- Recommendations

### Budget Variance Analysis
- Category-wise variance
- Over/under budget identification
- Overall variance percentage
- Actionable insights

### Cash Flow Analysis
- Daily/cumulative cash flow
- Inflow/outflow tracking
- Flow volatility measurement
- Positive/negative flow days

---

## 🔮 Predictive Insights Features

### Spending Forecast
- Exponential smoothing
- Confidence intervals
- Trend detection
- 30-day default forecast

### Income Forecast
- Linear regression trend
- Monthly projections
- Confidence intervals
- Annual income projection

### Savings Projection
- Compound interest calculation
- Monthly growth tracking
- Interest earned calculation
- Customizable return rates

### Goal Achievement Prediction
- Probability calculation
- Timeline estimation
- Required contribution analysis
- Status tracking

### Financial Health Assessment
- Health score (0-100)
- Metric analysis
- Strength/weakness identification
- Personalized recommendations

### Anomaly Detection
- Statistical threshold calculation
- Anomaly probability
- Risk level assessment
- Early warning system

---

## 🔐 Security Features

- JWT-based authentication
- Password hashing with bcrypt
- CORS protection
- SQL injection prevention
- Rate limiting
- Input validation
- Secure token refresh

---

## 📱 Frontend Pages

### Dashboard
- Overview of financial status
- Recent transactions
- Expense breakdown
- Key metrics

### Analytics
- Spending patterns visualization
- Income trends analysis
- Savings rate metrics
- Cash flow analysis
- Identified patterns and anomalies

### Predictions
- Spending forecasts
- Income projections
- Savings projections
- Financial health score
- Anomaly detection results
- Personalized recommendations

### Multi-Agent System
- Available agents overview
- Collaborative task execution
- System status monitoring
- Agent activity history

---

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest tests/
```

### Frontend Tests
```bash
cd frontend
npm test
```

---

## 📦 Deployment

### Docker Deployment

```bash
# Build Docker images
docker-compose build

# Start services
docker-compose up -d
```

### Production Deployment

See [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) for detailed deployment instructions.

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 👨‍💻 Developer

**Harsh Tambade**

---

## 📞 Support

For support, email support@fincoach.ai or open an issue on GitHub.

---

## 🙏 Acknowledgments

- FastAPI for the amazing web framework
- React for the powerful UI library
- PostgreSQL for reliable data storage
- All contributors and users

---

## 📈 Roadmap

- [ ] Mobile app (iOS/Android)
- [ ] Advanced portfolio management
- [ ] Cryptocurrency support
- [ ] Investment recommendations
- [ ] Tax optimization
- [ ] Insurance recommendations
- [ ] Debt management tools
- [ ] Retirement planning
- [ ] Real-time market data integration
- [ ] Advanced ML models

---

**Last Updated**: November 25, 2025
**Version**: 1.2.0
**Status**: Production Ready ✅

---

Made with ❤️ by Harsh Tambade
