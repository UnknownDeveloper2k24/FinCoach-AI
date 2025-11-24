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
};

export default API_BASE_URL;
