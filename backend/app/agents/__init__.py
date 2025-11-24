"""Multi-Agent System for FINCoach AI"""
from app.agents.financial_advisor import FinancialAdvisor
from app.agents.risk_assessor import RiskAssessor
from app.agents.prediction_agent import PredictionAgent
from app.agents.coaching_agent import CoachingAgent
from app.agents.multi_agent_orchestrator import MultiAgentOrchestrator, AgentType

__all__ = [
    "FinancialAdvisor",
    "RiskAssessor",
    "PredictionAgent",
    "CoachingAgent",
    "MultiAgentOrchestrator",
    "AgentType",
]
