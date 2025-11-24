"""
Multi-Agent AI System Orchestrator
Coordinates multiple AI agents to provide comprehensive financial guidance
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class AgentType(str, Enum):
    """Types of agents in the system"""
    FINANCIAL_ADVISOR = "financial_advisor"
    RISK_ASSESSOR = "risk_assessor"
    PREDICTION_AGENT = "prediction_agent"
    COACHING_AGENT = "coaching_agent"
    PORTFOLIO_OPTIMIZER = "portfolio_optimizer"
    MARKET_ANALYST = "market_analyst"


class MultiAgentOrchestrator:
    """
    Orchestrates multiple AI agents to work together
    Coordinates agent interactions and synthesizes their outputs
    """

    def __init__(self):
        self.agents: Dict[AgentType, Any] = {}
        self.agent_history: List[Dict[str, Any]] = []
        self.collaboration_rules: Dict[str, List[AgentType]] = {
            "financial_planning": [
                AgentType.FINANCIAL_ADVISOR,
                AgentType.RISK_ASSESSOR,
                AgentType.PREDICTION_AGENT,
            ],
            "portfolio_optimization": [
                AgentType.PORTFOLIO_OPTIMIZER,
                AgentType.MARKET_ANALYST,
                AgentType.RISK_ASSESSOR,
            ],
            "user_coaching": [
                AgentType.COACHING_AGENT,
                AgentType.FINANCIAL_ADVISOR,
                AgentType.PREDICTION_AGENT,
            ],
        }

    def register_agent(self, agent_type: AgentType, agent_instance: Any) -> None:
        """Register an agent in the system"""
        self.agents[agent_type] = agent_instance
        logger.info(f"Agent registered: {agent_type}")

    def get_agent(self, agent_type: AgentType) -> Optional[Any]:
        """Get a specific agent"""
        return self.agents.get(agent_type)

    async def execute_collaborative_task(
        self,
        task_type: str,
        user_data: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Execute a task using multiple agents collaboratively
        
        Args:
            task_type: Type of task (e.g., 'financial_planning')
            user_data: User financial data
            context: Additional context for the task
            
        Returns:
            Synthesized response from all agents
        """
        agents_to_use = self.collaboration_rules.get(task_type, [])
        
        if not agents_to_use:
            logger.warning(f"No agents configured for task type: {task_type}")
            return {"error": f"Unknown task type: {task_type}"}

        results = {}
        execution_log = {
            "task_type": task_type,
            "timestamp": datetime.utcnow().isoformat(),
            "agents_used": [],
            "results": {},
        }

        # Execute each agent
        for agent_type in agents_to_use:
            agent = self.get_agent(agent_type)
            if not agent:
                logger.warning(f"Agent not found: {agent_type}")
                continue

            try:
                # Execute agent with user data and context
                agent_result = await self._execute_agent(
                    agent, agent_type, user_data, context
                )
                results[agent_type.value] = agent_result
                execution_log["agents_used"].append(agent_type.value)
                execution_log["results"][agent_type.value] = agent_result
            except Exception as e:
                logger.error(f"Error executing agent {agent_type}: {str(e)}")
                results[agent_type.value] = {"error": str(e)}

        # Store execution log
        self.agent_history.append(execution_log)

        # Synthesize results
        synthesized = self._synthesize_results(results, task_type)
        
        return {
            "task_type": task_type,
            "timestamp": datetime.utcnow().isoformat(),
            "agent_results": results,
            "synthesized_recommendation": synthesized,
            "execution_log": execution_log,
        }

    async def _execute_agent(
        self,
        agent: Any,
        agent_type: AgentType,
        user_data: Dict[str, Any],
        context: Optional[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Execute a single agent"""
        # This would call the actual agent's analyze or process method
        if hasattr(agent, "analyze"):
            return await agent.analyze(user_data, context)
        elif hasattr(agent, "process"):
            return await agent.process(user_data, context)
        else:
            return {"status": "Agent method not found"}

    def _synthesize_results(
        self, results: Dict[str, Any], task_type: str
    ) -> Dict[str, Any]:
        """
        Synthesize results from multiple agents
        Combines insights and creates unified recommendations
        """
        synthesis = {
            "task_type": task_type,
            "confidence_score": self._calculate_confidence(results),
            "key_insights": self._extract_key_insights(results),
            "recommendations": self._generate_recommendations(results, task_type),
            "risk_assessment": self._aggregate_risk_assessment(results),
            "next_steps": self._determine_next_steps(results, task_type),
        }
        return synthesis

    def _calculate_confidence(self, results: Dict[str, Any]) -> float:
        """Calculate overall confidence score based on agent agreement"""
        if not results:
            return 0.0
        
        # Simple confidence calculation based on number of successful agents
        successful_agents = sum(
            1 for r in results.values() if not isinstance(r, dict) or "error" not in r
        )
        return min(1.0, successful_agents / len(results))

    def _extract_key_insights(self, results: Dict[str, Any]) -> List[str]:
        """Extract key insights from agent results"""
        insights = []
        for agent_name, result in results.items():
            if isinstance(result, dict):
                if "insights" in result:
                    insights.extend(result["insights"])
                elif "analysis" in result:
                    insights.append(result["analysis"])
        return insights[:5]  # Return top 5 insights

    def _generate_recommendations(
        self, results: Dict[str, Any], task_type: str
    ) -> List[str]:
        """Generate unified recommendations from agent results"""
        recommendations = []
        for agent_name, result in results.items():
            if isinstance(result, dict):
                if "recommendations" in result:
                    recommendations.extend(result["recommendations"])
                elif "suggestion" in result:
                    recommendations.append(result["suggestion"])
        return recommendations[:5]  # Return top 5 recommendations

    def _aggregate_risk_assessment(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Aggregate risk assessments from all agents"""
        risk_scores = []
        risk_factors = []
        
        for agent_name, result in results.items():
            if isinstance(result, dict):
                if "risk_score" in result:
                    risk_scores.append(result["risk_score"])
                if "risk_factors" in result:
                    risk_factors.extend(result["risk_factors"])
        
        avg_risk = sum(risk_scores) / len(risk_scores) if risk_scores else 0.5
        
        return {
            "overall_risk_score": avg_risk,
            "risk_level": self._categorize_risk(avg_risk),
            "identified_risks": list(set(risk_factors))[:5],
        }

    def _categorize_risk(self, score: float) -> str:
        """Categorize risk level based on score"""
        if score < 0.3:
            return "Low"
        elif score < 0.6:
            return "Medium"
        elif score < 0.8:
            return "High"
        else:
            return "Very High"

    def _determine_next_steps(
        self, results: Dict[str, Any], task_type: str
    ) -> List[str]:
        """Determine next steps based on agent recommendations"""
        next_steps = []
        
        if task_type == "financial_planning":
            next_steps = [
                "Review and adjust budget allocations",
                "Set up automated savings transfers",
                "Schedule quarterly financial review",
                "Monitor investment performance",
            ]
        elif task_type == "portfolio_optimization":
            next_steps = [
                "Rebalance portfolio according to recommendations",
                "Review asset allocation",
                "Monitor market trends",
                "Adjust risk exposure if needed",
            ]
        elif task_type == "user_coaching":
            next_steps = [
                "Complete financial literacy modules",
                "Track spending patterns",
                "Review progress on financial goals",
                "Schedule coaching session",
            ]
        
        return next_steps

    def get_agent_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent agent execution history"""
        return self.agent_history[-limit:]

    def get_system_status(self) -> Dict[str, Any]:
        """Get current system status"""
        return {
            "registered_agents": list(self.agents.keys()),
            "total_agents": len(self.agents),
            "total_executions": len(self.agent_history),
            "collaboration_rules": list(self.collaboration_rules.keys()),
            "last_execution": (
                self.agent_history[-1]["timestamp"]
                if self.agent_history
                else None
            ),
        }
