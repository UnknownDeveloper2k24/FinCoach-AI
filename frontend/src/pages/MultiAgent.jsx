import React, { useEffect, useState } from 'react';
import { useAuthStore } from '../store/authStore';
import apiClient from '../services/apiClient';
import { API_ENDPOINTS } from '../config/api';
import { Bot, Zap, Target, TrendingUp, Users, BarChart3 } from 'lucide-react';

export default function MultiAgent() {
  const { user } = useAuthStore();
  const [systemStatus, setSystemStatus] = useState(null);
  const [agentHistory, setAgentHistory] = useState([]);
  const [selectedTask, setSelectedTask] = useState('financial_planning');
  const [loading, setLoading] = useState(true);
  const [executing, setExecuting] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchSystemStatus();
  }, []);

  const fetchSystemStatus = async () => {
    try {
      setLoading(true);
      const statusRes = await apiClient.get(API_ENDPOINTS.MULTI_AGENT.SYSTEM_STATUS);
      setSystemStatus(statusRes.data);

      const historyRes = await apiClient.get(API_ENDPOINTS.MULTI_AGENT.AGENT_HISTORY);
      setAgentHistory(historyRes.data);
    } catch (err) {
      console.error('Error fetching system status:', err);
      setError('Failed to load multi-agent system status');
    } finally {
      setLoading(false);
    }
  };

  const executeTask = async (taskType) => {
    try {
      setExecuting(true);
      setError(null);
      setResult(null);

      let endpoint = API_ENDPOINTS.MULTI_AGENT.EXECUTE_TASK;
      let payload = { task_type: taskType, user_data: user };

      if (taskType === 'financial_planning') {
        endpoint = API_ENDPOINTS.MULTI_AGENT.FINANCIAL_PLANNING;
      } else if (taskType === 'portfolio_optimization') {
        endpoint = API_ENDPOINTS.MULTI_AGENT.PORTFOLIO_OPTIMIZATION;
      } else if (taskType === 'user_coaching') {
        endpoint = API_ENDPOINTS.MULTI_AGENT.USER_COACHING;
      }

      const res = await apiClient.post(endpoint, payload);
      setResult(res.data);
      
      // Refresh history
      fetchSystemStatus();
    } catch (err) {
      console.error('Error executing task:', err);
      setError('Failed to execute task');
    } finally {
      setExecuting(false);
    }
  };

  if (loading) {
    return <div className="flex items-center justify-center h-screen">Loading multi-agent system...</div>;
  }

  const agents = [
    {
      id: 'financial_advisor',
      name: 'Financial Advisor',
      icon: <TrendingUp className="w-6 h-6" />,
      description: 'Provides comprehensive financial planning advice',
      color: 'bg-blue-500',
    },
    {
      id: 'risk_assessor',
      name: 'Risk Assessor',
      icon: <Zap className="w-6 h-6" />,
      description: 'Evaluates financial risks and vulnerabilities',
      color: 'bg-orange-500',
    },
    {
      id: 'prediction_agent',
      name: 'Prediction Agent',
      icon: <BarChart3 className="w-6 h-6" />,
      description: 'Makes financial predictions and forecasts',
      color: 'bg-purple-500',
    },
    {
      id: 'coaching_agent',
      name: 'Coaching Agent',
      icon: <Users className="w-6 h-6" />,
      description: 'Provides personalized financial coaching',
      color: 'bg-green-500',
    },
    {
      id: 'portfolio_optimizer',
      name: 'Portfolio Optimizer',
      icon: <Target className="w-6 h-6" />,
      description: 'Optimizes investment portfolios',
      color: 'bg-indigo-500',
    },
    {
      id: 'market_analyst',
      name: 'Market Analyst',
      icon: <BarChart3 className="w-6 h-6" />,
      description: 'Analyzes market trends and opportunities',
      color: 'bg-pink-500',
    },
  ];

  const tasks = [
    {
      id: 'financial_planning',
      name: 'Financial Planning',
      description: 'Get comprehensive financial planning with risk assessment and predictions',
      agents: ['Financial Advisor', 'Risk Assessor', 'Prediction Agent'],
    },
    {
      id: 'portfolio_optimization',
      name: 'Portfolio Optimization',
      description: 'Optimize your investment portfolio with market analysis',
      agents: ['Portfolio Optimizer', 'Market Analyst', 'Risk Assessor'],
    },
    {
      id: 'user_coaching',
      name: 'User Coaching',
      description: 'Get personalized financial coaching and guidance',
      agents: ['Coaching Agent', 'Financial Advisor', 'Prediction Agent'],
    },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 to-blue-100 p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-800 flex items-center">
            <Bot className="w-10 h-10 mr-3 text-indigo-600" />
            Multi-Agent AI System
          </h1>
          <p className="text-gray-600 mt-2">Collaborative AI agents for comprehensive financial guidance</p>
        </div>

        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">
            {error}
          </div>
        )}

        {/* System Status */}
        {systemStatus && (
          <div className="bg-white rounded-lg shadow-lg p-6 mb-8">
            <h2 className="text-xl font-bold mb-4">System Status</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div>
                <p className="text-gray-600 text-sm">Active Agents</p>
                <p className="text-3xl font-bold text-indigo-600">{systemStatus.active_agents || 0}</p>
              </div>
              <div>
                <p className="text-gray-600 text-sm">Total Tasks Executed</p>
                <p className="text-3xl font-bold text-green-600">{systemStatus.total_tasks || 0}</p>
              </div>
              <div>
                <p className="text-gray-600 text-sm">System Status</p>
                <p className="text-3xl font-bold text-blue-600">{systemStatus.status || 'Unknown'}</p>
              </div>
            </div>
          </div>
        )}

        {/* Available Agents */}
        <div className="mb-8">
          <h2 className="text-2xl font-bold mb-4">Available Agents</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {agents.map((agent) => (
              <div key={agent.id} className="bg-white rounded-lg shadow-lg p-6">
                <div className={`${agent.color} text-white w-12 h-12 rounded-lg flex items-center justify-center mb-4`}>
                  {agent.icon}
                </div>
                <h3 className="text-lg font-bold text-gray-800">{agent.name}</h3>
                <p className="text-gray-600 text-sm mt-2">{agent.description}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Task Execution */}
        <div className="bg-white rounded-lg shadow-lg p-6 mb-8">
          <h2 className="text-2xl font-bold mb-6">Execute Collaborative Tasks</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
            {tasks.map((task) => (
              <div
                key={task.id}
                className={`p-6 rounded-lg border-2 cursor-pointer transition ${
                  selectedTask === task.id
                    ? 'border-indigo-600 bg-indigo-50'
                    : 'border-gray-200 bg-gray-50 hover:border-indigo-300'
                }`}
                onClick={() => setSelectedTask(task.id)}
              >
                <h3 className="text-lg font-bold text-gray-800">{task.name}</h3>
                <p className="text-gray-600 text-sm mt-2">{task.description}</p>
                <div className="mt-4">
                  <p className="text-xs font-semibold text-gray-600 mb-2">Agents Involved:</p>
                  <div className="flex flex-wrap gap-2">
                    {task.agents.map((agent, idx) => (
                      <span key={idx} className="text-xs bg-indigo-100 text-indigo-700 px-2 py-1 rounded">
                        {agent}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
            ))}
          </div>

          <button
            onClick={() => executeTask(selectedTask)}
            disabled={executing}
            className="w-full bg-indigo-600 hover:bg-indigo-700 disabled:bg-gray-400 text-white font-bold py-3 px-6 rounded-lg transition"
          >
            {executing ? 'Executing...' : 'Execute Task'}
          </button>
        </div>

        {/* Task Result */}
        {result && (
          <div className="bg-white rounded-lg shadow-lg p-6 mb-8">
            <h2 className="text-2xl font-bold mb-4">Task Result</h2>
            <div className="bg-gray-50 p-6 rounded-lg">
              <pre className="text-sm text-gray-800 overflow-auto max-h-96">
                {JSON.stringify(result, null, 2)}
              </pre>
            </div>
          </div>
        )}

        {/* Agent History */}
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h2 className="text-2xl font-bold mb-4">Recent Agent Activity</h2>
          {agentHistory.length > 0 ? (
            <div className="space-y-4">
              {agentHistory.slice(0, 10).map((entry, idx) => (
                <div key={idx} className="p-4 bg-gray-50 rounded-lg border border-gray-200">
                  <div className="flex justify-between items-start">
                    <div>
                      <p className="font-semibold text-gray-800">{entry.agent_name || 'Unknown Agent'}</p>
                      <p className="text-sm text-gray-600 mt-1">{entry.task_type || 'Unknown Task'}</p>
                    </div>
                    <span className={`text-xs font-bold px-3 py-1 rounded ${
                      entry.status === 'completed' ? 'bg-green-100 text-green-700' : 'bg-yellow-100 text-yellow-700'
                    }`}>
                      {entry.status || 'Unknown'}
                    </span>
                  </div>
                  {entry.timestamp && (
                    <p className="text-xs text-gray-500 mt-2">{new Date(entry.timestamp).toLocaleString()}</p>
                  )}
                </div>
              ))}
            </div>
          ) : (
            <p className="text-gray-500">No agent activity yet</p>
          )}
        </div>
      </div>
    </div>
  );
}
