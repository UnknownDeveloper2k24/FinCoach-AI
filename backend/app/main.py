"""Main FastAPI Application for FINCoach AI Backend"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from app.api import auth, users, transactions, jars, goals, alerts, agents, ml_modules, analytics, mobile, notifications, social, advanced_analytics, predictive_insights, multi_agent_system
from app.core.config import settings
from app.core.database import engine, Base

# Create tables
Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 FINCoach AI Backend Starting...")
    yield
    # Shutdown
    print("🛑 FINCoach AI Backend Shutting Down...")

app = FastAPI(
    title="FINCoach AI Backend",
    description="AI-powered personal finance management system with Advanced Analytics, Multi-Agent AI System, Predictive Insights, Mobile Integration, Real-time Notifications, and Social Features",
    version="1.2.0",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers - Core Features
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(transactions.router, prefix="/api/v1/transactions", tags=["Transactions"])
app.include_router(jars.router, prefix="/api/v1/jars", tags=["Jars"])
app.include_router(goals.router, prefix="/api/v1/goals", tags=["Goals"])
app.include_router(alerts.router, prefix="/api/v1/alerts", tags=["Alerts"])

# Include routers - AI & ML
app.include_router(agents.router, tags=["AI Agents"])
app.include_router(ml_modules.router, tags=["ML Modules"])

# Include routers - Advanced Features (Phase 2)
app.include_router(advanced_analytics.router, tags=["Advanced Analytics"])
app.include_router(predictive_insights.router, tags=["Predictive Insights"])
app.include_router(multi_agent_system.router, tags=["Multi-Agent System"])

# Include routers - New Features (Phase 2)
app.include_router(analytics.router, tags=["Analytics"])
app.include_router(mobile.router, tags=["Mobile Integration"])
app.include_router(notifications.router, tags=["Real-time Notifications"])
app.include_router(social.router, tags=["Social Features"])

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "FINCoach AI Backend",
        "version": "1.2.0"
    }

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to FINCoach AI Backend",
        "version": "1.2.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "features": {
            "core": [
                "Authentication",
                "Users",
                "Transactions",
                "Jars",
                "Goals",
                "Alerts"
            ],
            "ai_agents": [
                "Financial Advisor",
                "Risk Assessor",
                "Prediction Agent",
                "Coaching Agent",
                "Portfolio Optimizer",
                "Market Analyst"
            ],
            "ml_modules": [
                "Prediction Engine",
                "Transaction Categorizer",
                "Anomaly Detector",
                "Advanced Analytics",
                "Predictive Insights"
            ],
            "advanced_features": [
                "Multi-Agent AI System",
                "Advanced Analytics",
                "Predictive Insights",
                "Mobile App Integration",
                "Real-time Notifications",
                "Social Features"
            ]
        },
        "endpoints": {
            "advanced_analytics": "/api/v1/analytics",
            "predictive_insights": "/api/v1/predictions",
            "multi_agent_system": "/api/v1/multi-agent",
            "mobile": "/api/v1/mobile",
            "notifications": "/api/v1/notifications",
            "social": "/api/v1/social"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
