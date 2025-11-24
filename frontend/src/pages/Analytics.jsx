import React, { useEffect, useState } from 'react';
import { useAuthStore } from '../store/authStore';
import apiClient from '../services/apiClient';
import { API_ENDPOINTS } from '../config/api';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, AreaChart, Area } from 'recharts';
import { TrendingUp, TrendingDown, Activity, PieChart as PieChartIcon } from 'lucide-react';

export default function Analytics() {
  const { user } = useAuthStore();
  const [spendingPatterns, setSpendingPatterns] = useState(null);
  const [incomeTrends, setIncomeTrends] = useState(null);
  const [savingsRate, setSavingsRate] = useState(null);
  const [cashFlow, setCashFlow] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchAnalyticsData();
  }, []);

  const fetchAnalyticsData = async () => {
    try {
      setLoading(true);
      
      // Fetch transactions for analysis
      const transRes = await apiClient.get(API_ENDPOINTS.TRANSACTIONS.LIST);
      const transactions = transRes.data;

      // Fetch spending patterns
      const spendingRes = await apiClient.post(
        API_ENDPOINTS.ANALYTICS.SPENDING_PATTERNS,
        { transactions, period_days: 90 }
      );
      setSpendingPatterns(spendingRes.data);

      // Fetch income trends
      const incomeRes = await apiClient.post(
        API_ENDPOINTS.ANALYTICS.INCOME_TRENDS,
        { transactions, period_days: 90 }
      );
      setIncomeTrends(incomeRes.data);

      // Fetch savings rate
      const savingsRes = await apiClient.post(
        API_ENDPOINTS.ANALYTICS.SAVINGS_RATE,
        {
          income: user?.monthly_income || 0,
          expenses: 0,
          savings: 0,
          period_days: 30,
        }
      );
      setSavingsRate(savingsRes.data);

      // Fetch cash flow
      const cashFlowRes = await apiClient.post(
        API_ENDPOINTS.ANALYTICS.CASH_FLOW,
        { transactions, period_days: 90 }
      );
      setCashFlow(cashFlowRes.data);
    } catch (err) {
      console.error('Error fetching analytics:', err);
      setError('Failed to load analytics data');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="flex items-center justify-center h-screen">Loading analytics...</div>;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-800">Advanced Analytics</h1>
          <p className="text-gray-600 mt-2">Comprehensive financial analysis and insights</p>
        </div>

        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">
            {error}
          </div>
        )}

        {/* Key Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <MetricCard
            icon={<TrendingUp className="w-8 h-8" />}
            title="Savings Rate"
            value={`${savingsRate?.savings_rate?.toFixed(2) || 0}%`}
            color="bg-green-500"
          />
          <MetricCard
            icon={<Activity className="w-8 h-8" />}
            title="Income Stability"
            value={`${incomeTrends?.income_stability?.toFixed(2) || 0}%`}
            color="bg-blue-500"
          />
          <MetricCard
            icon={<TrendingDown className="w-8 h-8" />}
            title="Expense Ratio"
            value={`${savingsRate?.expense_ratio?.toFixed(2) || 0}%`}
            color="bg-orange-500"
          />
          <MetricCard
            icon={<PieChartIcon className="w-8 h-8" />}
            title="Total Income"
            value={`₹${incomeTrends?.total_income?.toLocaleString() || 0}`}
            color="bg-purple-500"
          />
        </div>

        {/* Charts */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          {/* Spending Patterns */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-xl font-bold mb-4">Spending Patterns</h2>
            {spendingPatterns?.spending_by_category ? (
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={Object.entries(spendingPatterns.spending_by_category).map(([cat, amt]) => ({ category: cat, amount: amt }))}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="category" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="amount" fill="#8884d8" />
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <p className="text-gray-500">No spending data available</p>
            )}
          </div>

          {/* Income Trends */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-xl font-bold mb-4">Income Trends</h2>
            {incomeTrends?.monthly_trend ? (
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={Object.entries(incomeTrends.monthly_trend).map(([month, amt]) => ({ month, amount: amt }))}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="month" />
                  <YAxis />
                  <Tooltip />
                  <Line type="monotone" dataKey="amount" stroke="#82ca9d" />
                </LineChart>
              </ResponsiveContainer>
            ) : (
              <p className="text-gray-500">No income data available</p>
            )}
          </div>

          {/* Cash Flow Analysis */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-xl font-bold mb-4">Cash Flow Analysis</h2>
            {cashFlow?.daily_cash_flow ? (
              <ResponsiveContainer width="100%" height={300}>
                <AreaChart data={cashFlow.daily_cash_flow.slice(0, 30)}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" />
                  <YAxis />
                  <Tooltip />
                  <Area type="monotone" dataKey="flow" fill="#ffc658" />
                </AreaChart>
              </ResponsiveContainer>
            ) : (
              <p className="text-gray-500">No cash flow data available</p>
            )}
          </div>

          {/* Savings Rate Details */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-xl font-bold mb-4">Savings Analysis</h2>
            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <span className="text-gray-600">Monthly Income</span>
                <span className="font-bold text-lg">₹{savingsRate?.income?.toLocaleString() || 0}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-600">Monthly Expenses</span>
                <span className="font-bold text-lg">₹{savingsRate?.expenses?.toLocaleString() || 0}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-600">Monthly Savings</span>
                <span className="font-bold text-lg text-green-600">₹{savingsRate?.savings?.toLocaleString() || 0}</span>
              </div>
              <div className="border-t pt-4 flex justify-between items-center">
                <span className="text-gray-600 font-semibold">Savings Rate</span>
                <span className="font-bold text-xl text-green-600">{savingsRate?.savings_rate?.toFixed(2) || 0}%</span>
              </div>
            </div>
          </div>
        </div>

        {/* Anomalies and Patterns */}
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h2 className="text-xl font-bold mb-4">Identified Patterns & Anomalies</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h3 className="font-semibold text-gray-700 mb-3">Spending Patterns</h3>
              {spendingPatterns?.patterns_identified?.length > 0 ? (
                <ul className="space-y-2">
                  {spendingPatterns.patterns_identified.map((pattern, idx) => (
                    <li key={idx} className="text-sm text-gray-600 flex items-start">
                      <span className="text-green-500 mr-2">✓</span>
                      {pattern}
                    </li>
                  ))}
                </ul>
              ) : (
                <p className="text-gray-500">No patterns identified yet</p>
              )}
            </div>
            <div>
              <h3 className="font-semibold text-gray-700 mb-3">Anomalies Detected</h3>
              {spendingPatterns?.anomalies?.length > 0 ? (
                <ul className="space-y-2">
                  {spendingPatterns.anomalies.map((anomaly, idx) => (
                    <li key={idx} className="text-sm text-gray-600 flex items-start">
                      <span className="text-orange-500 mr-2">⚠</span>
                      {anomaly}
                    </li>
                  ))}
                </ul>
              ) : (
                <p className="text-gray-500">No anomalies detected</p>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function MetricCard({ icon, title, value, color }) {
  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <div className={`${color} text-white w-12 h-12 rounded-lg flex items-center justify-center mb-4`}>
        {icon}
      </div>
      <p className="text-gray-600 text-sm">{title}</p>
      <p className="text-2xl font-bold text-gray-800 mt-2">{value}</p>
    </div>
  );
}
