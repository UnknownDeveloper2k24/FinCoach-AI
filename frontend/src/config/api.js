// API Configuration
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

export const API_ENDPOINTS = {
  // Auth
  AUTH: {
    REGISTER: `${API_BASE_URL}/auth/register`,
    LOGIN: `${API_BASE_URL}/auth/login`,
    REFRESH: `${API_BASE_URL}/auth/refresh`,
  },
  // Users
  USERS: {
    ME: `${API_BASE_URL}/users/me`,
    PROFILE: (id) => `${API_BASE_URL}/users/${id}`,
  },
  // Transactions
  TRANSACTIONS: {
    LIST: `${API_BASE_URL}/transactions`,
    CREATE: `${API_BASE_URL}/transactions`,
    GET: (id) => `${API_BASE_URL}/transactions/${id}`,
    UPDATE: (id) => `${API_BASE_URL}/transactions/${id}`,
    DELETE: (id) => `${API_BASE_URL}/transactions/${id}`,
    SUMMARY: `${API_BASE_URL}/transactions/stats/summary`,
  },
  // Jars
  JARS: {
    LIST: `${API_BASE_URL}/jars`,
    CREATE: `${API_BASE_URL}/jars`,
    GET: (id) => `${API_BASE_URL}/jars/${id}`,
    UPDATE: (id) => `${API_BASE_URL}/jars/${id}`,
    DELETE: (id) => `${API_BASE_URL}/jars/${id}`,
    ADD_FUNDS: (id) => `${API_BASE_URL}/jars/${id}/add-funds`,
    PROGRESS: (id) => `${API_BASE_URL}/jars/${id}/progress`,
  },
  // Goals
  GOALS: {
    LIST: `${API_BASE_URL}/goals`,
    CREATE: `${API_BASE_URL}/goals`,
    GET: (id) => `${API_BASE_URL}/goals/${id}`,
    UPDATE: (id) => `${API_BASE_URL}/goals/${id}`,
    DELETE: (id) => `${API_BASE_URL}/goals/${id}`,
    ADD_PROGRESS: (id) => `${API_BASE_URL}/goals/${id}/add-progress`,
    PROGRESS: (id) => `${API_BASE_URL}/goals/${id}/progress`,
  },
  // Alerts
  ALERTS: {
    LIST: `${API_BASE_URL}/alerts`,
    CREATE: `${API_BASE_URL}/alerts`,
    GET: (id) => `${API_BASE_URL}/alerts/${id}`,
    MARK_READ: (id) => `${API_BASE_URL}/alerts/${id}/mark-as-read`,
    DELETE: (id) => `${API_BASE_URL}/alerts/${id}`,
    SUMMARY: `${API_BASE_URL}/alerts/stats/summary`,
  },
  // Advanced Analytics
  ANALYTICS: {
    SPENDING_PATTERNS: `${API_BASE_URL}/analytics/spending-patterns`,
    INCOME_TRENDS: `${API_BASE_URL}/analytics/income-trends`,
    SAVINGS_RATE: `${API_BASE_URL}/analytics/savings-rate`,
    BUDGET_VARIANCE: `${API_BASE_URL}/analytics/budget-variance`,
    CASH_FLOW: `${API_BASE_URL}/analytics/cash-flow`,
    COMPREHENSIVE_REPORT: `${API_BASE_URL}/analytics/comprehensive-report`,
  },
  // Predictive Insights
  PREDICTIONS: {
    SPENDING_FORECAST: `${API_BASE_URL}/predictions/spending-forecast`,
    INCOME_FORECAST: `${API_BASE_URL}/predictions/income-forecast`,
    SAVINGS_PROJECTION: `${API_BASE_URL}/predictions/savings-projection`,
    GOAL_ACHIEVEMENT: `${API_BASE_URL}/predictions/goal-achievement`,
    FINANCIAL_HEALTH: `${API_BASE_URL}/predictions/financial-health`,
    ANOMALY_DETECTION: `${API_BASE_URL}/predictions/anomaly-detection`,
    PREDICTION_HISTORY: `${API_BASE_URL}/predictions/prediction-history`,
  },
  // Multi-Agent System
  MULTI_AGENT: {
    EXECUTE_TASK: `${API_BASE_URL}/multi-agent/execute-task`,
    SYSTEM_STATUS: `${API_BASE_URL}/multi-agent/system-status`,
    AGENT_HISTORY: `${API_BASE_URL}/multi-agent/agent-history`,
    FINANCIAL_PLANNING: `${API_BASE_URL}/multi-agent/financial-planning`,
    PORTFOLIO_OPTIMIZATION: `${API_BASE_URL}/multi-agent/portfolio-optimization`,
    USER_COACHING: `${API_BASE_URL}/multi-agent/user-coaching`,
  },
};

export default API_BASE_URL;
