# FINCoach AI - Complete Application

A comprehensive AI-powered personal finance management system with intelligent financial coaching and advanced predictive analytics.

## 📁 Project Structure

```
fincoach-integrated/
├── backend/                 # FastAPI Backend
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   ├── models/         # Database models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # Business logic
│   │   ├── agents/         # AI agents (Multi-Agent System)
│   │   ├── ml_modules/     # ML modules (Analytics & Predictions)
│   │   ├── core/           # Core config
│   │   └── utils/          # Utilities
│   ├── requirements.txt
│   ├── .env.example
│   ├── NEW_FEATURES_DOCUMENTATION.md
│   └── README.md
│
└── frontend/                # React + Vite Frontend
    ├── src/
    │   ├── pages/          # Page components
    │   ├── components/     # Reusable components
    │   ├── store/          # Zustand stores
    │   ├── services/       # API services
    │   ├── config/         # Configuration
    │   ├── App.jsx
    │   └── main.jsx
    ├── package.json
    ├── .env
    └── vite.config.js
```

## 🚀 Quick Start

### Backend Setup

1. **Navigate to backend directory**
```bash
cd backend
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your settings
```

5. **Create database**
```bash
createdb -h localhost fincoach_db
```

6. **Run migrations**
```bash
alembic upgrade head
```

7. **Start the server**
```bash
python -m uvicorn app.main:app --reload
```

Backend will be available at: `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory**
```bash
cd frontend
```

2. **Install dependencies**
```bash
npm install
```

3. **Start development server**
```bash
npm run dev
```

Frontend will be available at: `http://localhost:5173`

## 🎯 Features

### Core Features (Completed) ✅
- ✅ User Authentication & Authorization
- ✅ Transaction Management (Income/Expense tracking)
- ✅ Savings Jar System (Goal-based savings)
- ✅ Financial Goals Management
- ✅ Alert System (Real-time notifications)
- ✅ UPI SMS Parsing (Indian banks)
- ✅ Budget Tracking
- ✅ Dashboard with Analytics

### Upcoming Features (Now Implemented) 🎉

#### 🔄 Multi-Agent AI System
- Orchestrated AI agents for collaborative decision-making
- Financial Planning Agent
- Risk Assessment Agent
- Prediction Agent
- Coaching Agent
- Portfolio Optimizer Agent
- Market Analyst Agent
- **API Endpoints**: `/api/v1/multi-agent/*`

#### 🔄 Machine Learning Modules
- Advanced spending pattern analysis
- Income trend analysis
- Savings rate calculation
- Budget variance analysis
- Cash flow analysis
- Anomaly detection
- **API Endpoints**: `/api/v1/analytics/*`

#### 🔄 Advanced Analytics
- Comprehensive financial analytics
- Spending pattern insights
- Income stability assessment
- Category-wise analysis
- Temporal analysis
- Variance reporting
- **API Endpoints**: `/api/v1/analytics/*`

#### 🔄 Predictive Insights
- Spending forecasts with confidence intervals
- Income projections
- Savings growth projections
- Goal achievement predictions
- Financial health assessment
- Anomaly predictions
- **API Endpoints**: `/api/v1/predictions/*`

## 📊 API Documentation

### Access Points
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

### Main Endpoints

#### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login user
- `POST /api/v1/auth/refresh` - Refresh access token

#### Transactions
- `GET /api/v1/transactions` - List transactions
- `POST /api/v1/transactions` - Create transaction
- `GET /api/v1/transactions/{id}` - Get transaction
- `PUT /api/v1/transactions/{id}` - Update transaction
- `DELETE /api/v1/transactions/{id}` - Delete transaction
- `GET /api/v1/transactions/stats/summary` - Get summary

#### Jars
- `GET /api/v1/jars` - List jars
- `POST /api/v1/jars` - Create jar
- `POST /api/v1/jars/{id}/add-funds` - Add funds to jar
- `GET /api/v1/jars/{id}/progress` - Get jar progress

#### Goals
- `GET /api/v1/goals` - List goals
- `POST /api/v1/goals` - Create goal
- `POST /api/v1/goals/{id}/add-progress` - Add progress to goal
- `GET /api/v1/goals/{id}/progress` - Get goal progress

#### Alerts
- `GET /api/v1/alerts` - List alerts
- `POST /api/v1/alerts` - Create alert
- `PUT /api/v1/alerts/{id}/mark-as-read` - Mark alert as read

#### Multi-Agent System (NEW)
- `POST /api/v1/multi-agent/execute-task` - Execute collaborative task
- `GET /api/v1/multi-agent/system-status` - Get system status
- `GET /api/v1/multi-agent/agent-history` - Get execution history
- `POST /api/v1/multi-agent/financial-planning` - Financial planning task
- `POST /api/v1/multi-agent/portfolio-optimization` - Portfolio optimization
- `POST /api/v1/multi-agent/user-coaching` - User coaching task

#### Advanced Analytics (NEW)
- `POST /api/v1/analytics/spending-patterns` - Analyze spending patterns
- `POST /api/v1/analytics/income-trends` - Analyze income trends
- `POST /api/v1/analytics/savings-rate` - Calculate savings rate
- `POST /api/v1/analytics/budget-variance` - Analyze budget variance
- `POST /api/v1/analytics/cash-flow` - Analyze cash flow
- `GET /api/v1/analytics/comprehensive-report` - Get comprehensive report

#### Predictive Insights (NEW)
- `POST /api/v1/predictions/spending-forecast` - Forecast spending
- `POST /api/v1/predictions/income-forecast` - Forecast income
- `POST /api/v1/predictions/savings-projection` - Project savings
- `POST /api/v1/predictions/goal-achievement` - Predict goal achievement
- `POST /api/v1/predictions/financial-health` - Assess financial health
- `POST /api/v1/predictions/anomaly-detection` - Detect anomalies
- `GET /api/v1/predictions/prediction-history` - Get prediction history

## 🛠️ Technology Stack

### Backend
- **Framework**: FastAPI 0.104.1
- **Database**: PostgreSQL with SQLAlchemy 2.0.23
- **Authentication**: JWT with python-jose
- **Validation**: Pydantic 2.5.0
- **Migrations**: Alembic 1.12.1
- **ML/Analytics**: NumPy, Pandas, Scikit-learn ready

### Frontend
- **Framework**: React 18
- **Build Tool**: Vite
- **State Management**: Zustand
- **HTTP Client**: Axios
- **Routing**: React Router
- **Charts**: Recharts
- **Styling**: Tailwind CSS
- **Icons**: Lucide React

## 🔐 Security

- JWT-based authentication
- bcrypt password hashing
- CORS protection
- SQL injection prevention
- Environment variable management
- HTTPS ready
- Rate limiting ready

## 📝 Environment Variables

### Backend (.env)
```
DATABASE_URL=postgresql://user:password@localhost/fincoach_db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Frontend (.env)
```
VITE_API_URL=http://localhost:8000/api/v1
```

## 🧪 Testing

### Backend
```bash
cd backend
pytest
pytest --cov=app
```

### Frontend
```bash
cd frontend
npm test
```

## 📚 Documentation

- **Backend**: See `backend/README.md`
- **Frontend**: See `frontend/README.md`
- **New Features**: See `backend/NEW_FEATURES_DOCUMENTATION.md`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 👥 Authors

- **Suchita Nigam** - Initial development
- **FINCoach Team** - Ongoing development

## 📞 Support

For support, email support@fincoach.ai or open an issue on GitHub.

---

**Last Updated**: November 25, 2025  
**Version**: 2.0.0  
**Status**: Production Ready with Advanced Features

## 🎉 What's New in v2.0.0

- ✨ Multi-Agent AI System for collaborative financial decision-making
- 📊 Advanced Analytics with comprehensive financial insights
- 🔮 Predictive Insights for spending and income forecasting
- 🤖 Machine Learning modules for pattern recognition and anomaly detection
- 📈 Financial health assessment with personalized recommendations
- 🎯 Goal achievement prediction and tracking
- 💡 Intelligent recommendations based on financial patterns
