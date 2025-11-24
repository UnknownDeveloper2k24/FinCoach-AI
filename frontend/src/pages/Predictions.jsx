import React, { useEffect, useState } from 'react';
import { useAuthStore } from '../store/authStore';
import apiClient from '../services/apiClient';
import { API_ENDPOINTS } from '../config/api';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar } from 'recharts';
import { Zap, Target, TrendingUp, AlertTriangle, CheckCircle } from 'lucide-react';

export default function Predictions() {
  const { user } = useAuthStore();
  const [spendingForecast, setSpendingForecast] = useState(null);
  const [incomeForecast, setIncomeForecast] = useState(null);
  const [savingsProjection, setSavingsProjection] = useState(null);
  const [financialHealth, setFinancialHealth] = useState(null);
  const [anomalies, setAnomalies] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchPredictions();
  }, []);

  const fetchPredictions = async () => {
    try {
      setLoading(true);

      // Fetch transactions for predictions
      const transRes = await apiClient.get(API_ENDPOINTS.TRANSACTIONS.LIST);
      const transactions = transRes.data;

      // Fetch spending forecast
      const spendingRes = await apiClient.post(
        API_ENDPOINTS.PREDICTIONS.SPENDING_FORECAST,
        { historical_spending: transactions, forecast_days: 30, confidence_level: 0.95 }
      );
      setSpendingForecast(spendingRes.data);

      // Fetch income forecast
      const incomeRes = await apiClient.post(
        API_ENDPOINTS.PREDICTIONS.INCOME_FORECAST,
        { historical_income: transactions, forecast_months: 6, confidence_level: 0.95 }
      );
      setIncomeForecast(incomeRes.data);

      // Fetch savings projection
      const savingsRes = await apiClient.post(
        API_ENDPOINTS.PREDICTIONS.SAVINGS_PROJECTION,
        {
          current_savings: user?.savings || 0,
          monthly_savings_rate: user?.monthly_budget ? user.monthly_budget * 0.2 : 0,
          annual_return_rate: 0.05,
          projection_months: 12,
        }
      );
      setSavingsProjection(savingsRes.data);

      // Fetch financial health
      const healthRes = await apiClient.post(
        API_ENDPOINTS.PREDICTIONS.FINANCIAL_HEALTH,
        {
          income: user?.monthly_income || 0,
          expenses: 0,
          savings: user?.savings || 0,
          debt: 0,
          emergency_fund: user?.emergency_fund || 0,
        }
      );
      setFinancialHealth(healthRes.data);

      // Fetch anomaly detection
      const anomalyRes = await apiClient.post(
        API_ENDPOINTS.PREDICTIONS.ANOMALY_DETECTION,
        { historical_data: transactions, sensitivity: 0.8 }
      );
      setAnomalies(anomalyRes.data);
    } catch (err) {
      console.error('Error fetching predictions:', err);
      setError('Failed to load predictions');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="flex items-center justify-center h-screen">Loading predictions...</div>;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-pink-100 p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-800">Predictive Insights</h1>
          <p className="text-gray-600 mt-2">AI-powered financial forecasts and predictions</p>
        </div>

        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">
            {error}
          </div>
        )}

        {/* Financial Health Score */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <PredictionCard
            icon={<Zap className="w-8 h-8" />}
            title="Financial Health"
            value={`${financialHealth?.health_score || 0}/100`}
            color="bg-green-500"
            subtitle={financialHealth?.health_status || 'Unknown'}
          />
          <PredictionCard
            icon={<TrendingUp className="w-8 h-8" />}
            title="30-Day Spending Forecast"
            value={`₹${spendingForecast?.forecast_value?.toLocaleString() || 0}`}
            color="bg-blue-500"
            subtitle={`±₹${spendingForecast?.confidence_interval?.toLocaleString() || 0}`}
          />
          <PredictionCard
            icon={<Target className="w-8 h-8" />}
            title="6-Month Income Forecast"
            value={`₹${incomeForecast?.forecast_value?.toLocaleString() || 0}`}
            color="bg-purple-500"
            subtitle="Average monthly"
          />
          <PredictionCard
            icon={<CheckCircle className="w-8 h-8" />}
            title="12-Month Savings"
            value={`₹${savingsProjection?.projected_savings?.toLocaleString() || 0}`}
            color="bg-indigo-500"
            subtitle={`+₹${savingsProjection?.interest_earned?.toLocaleString() || 0} interest`}
          />
        </div>

        {/* Charts */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          {/* Spending Forecast */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-xl font-bold mb-4">30-Day Spending Forecast</h2>
            {spendingForecast?.forecast_data ? (
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={spendingForecast.forecast_data}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="day" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Line type="monotone" dataKey="forecast" stroke="#8884d8" name="Forecast" />
                  <Line type="monotone" dataKey="upper_bound" stroke="#82ca9d" strokeDasharray="5 5" name="Upper Bound" />
                  <Line type="monotone" dataKey="lower_bound" stroke="#ffc658" strokeDasharray="5 5" name="Lower Bound" />
                </LineChart>
              </ResponsiveContainer>
            ) : (
              <p className="text-gray-500">No forecast data available</p>
            )}
          </div>

          {/* Income Forecast */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-xl font-bold mb-4">6-Month Income Forecast</h2>
            {incomeForecast?.forecast_data ? (
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={incomeForecast.forecast_data}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="month" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="forecast" fill="#82ca9d" name="Forecast" />
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <p className="text-gray-500">No forecast data available</p>
            )}
          </div>

          {/* Savings Projection */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-xl font-bold mb-4">12-Month Savings Projection</h2>
            {savingsProjection?.projection_data ? (
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={savingsProjection.projection_data}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="month" />
                  <YAxis />
                  <Tooltip />
                  <Line type="monotone" dataKey="projected_savings" stroke="#8884d8" name="Projected Savings" />
                </LineChart>
              </ResponsiveContainer>
            ) : (
              <p className="text-gray-500">No projection data available</p>
            )}
          </div>

          {/* Financial Health Radar */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-xl font-bold mb-4">Financial Health Metrics</h2>
            {financialHealth?.metrics ? (
              <ResponsiveContainer width="100%" height={300}>
                <RadarChart data={Object.entries(financialHealth.metrics).map(([key, val]) => ({ metric: key, value: val }))}>
                  <PolarGrid />
                  <PolarAngleAxis dataKey="metric" />
                  <PolarRadiusAxis angle={90} domain={[0, 100]} />
                  <Radar name="Score" dataKey="value" stroke="#8884d8" fill="#8884d8" fillOpacity={0.6} />
                </RadarChart>
              </ResponsiveContainer>
            ) : (
              <p className="text-gray-500">No metrics data available</p>
            )}
          </div>
        </div>

        {/* Anomalies and Recommendations */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Detected Anomalies */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-xl font-bold mb-4 flex items-center">
              <AlertTriangle className="w-5 h-5 mr-2 text-orange-500" />
              Detected Anomalies
            </h2>
            {anomalies?.anomalies?.length > 0 ? (
              <div className="space-y-3">
                {anomalies.anomalies.map((anomaly, idx) => (
                  <div key={idx} className="p-3 bg-orange-50 border border-orange-200 rounded">
                    <p className="font-semibold text-gray-800">{anomaly.description}</p>
                    <p className="text-sm text-gray-600 mt-1">
                      Probability: {(anomaly.probability * 100).toFixed(1)}%
                    </p>
                    <p className="text-sm text-orange-600 mt-1">Risk Level: {anomaly.risk_level}</p>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-gray-500">No anomalies detected</p>
            )}
          </div>

          {/* Recommendations */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-xl font-bold mb-4 flex items-center">
              <CheckCircle className="w-5 h-5 mr-2 text-green-500" />
              Recommendations
            </h2>
            {financialHealth?.recommendations?.length > 0 ? (
              <div className="space-y-3">
                {financialHealth.recommendations.map((rec, idx) => (
                  <div key={idx} className="p-3 bg-green-50 border border-green-200 rounded">
                    <p className="font-semibold text-gray-800">{rec.title}</p>
                    <p className="text-sm text-gray-600 mt-1">{rec.description}</p>
                    {rec.impact && (
                      <p className="text-sm text-green-600 mt-1">Impact: {rec.impact}</p>
                    )}
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-gray-500">No recommendations available</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

function PredictionCard({ icon, title, value, color, subtitle }) {
  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <div className={`${color} text-white w-12 h-12 rounded-lg flex items-center justify-center mb-4`}>
        {icon}
      </div>
      <p className="text-gray-600 text-sm">{title}</p>
      <p className="text-2xl font-bold text-gray-800 mt-2">{value}</p>
      {subtitle && <p className="text-xs text-gray-500 mt-1">{subtitle}</p>}
    </div>
  );
}
