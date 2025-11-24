import React, { useEffect, useState } from 'react';
import { useAuthStore } from '../store/authStore';
import apiClient from '../services/apiClient';
import { API_ENDPOINTS } from '../config/api';
import { BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, ScatterChart, Scatter } from 'recharts';
import { TrendingUp, AlertTriangle, Clock, Zap, Link2, Activity, CheckCircle } from 'lucide-react';

export default function PatternRecognition() {
  const { user } = useAuthStore();
  const [patterns, setPatterns] = useState(null);
  const [activeTab, setActiveTab] = useState('all');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchPatterns();
  }, []);

  const fetchPatterns = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const endpoints = {
        all: API_ENDPOINTS.PATTERNS.ALL,
        spending: API_ENDPOINTS.PATTERNS.SPENDING,
        temporal: API_ENDPOINTS.PATTERNS.TEMPORAL,
        behavioral: API_ENDPOINTS.PATTERNS.BEHAVIORAL,
        anomalies: API_ENDPOINTS.PATTERNS.ANOMALIES,
        correlations: API_ENDPOINTS.PATTERNS.CORRELATIONS,
      };

      const response = await apiClient.get(endpoints[activeTab]);
      setPatterns(response.data);
    } catch (error) {
      console.error('Error fetching patterns:', error);
      setError('Failed to load patterns. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (activeTab) {
      fetchPatterns();
    }
  }, [activeTab]);

  const renderSpendingPatterns = () => {
    if (!patterns?.spending_patterns) return null;
    
    return (
      <div className="space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {patterns.spending_patterns.map((pattern, idx) => (
            <div key={idx} className="bg-white rounded-lg shadow-lg p-6">
              <h3 className="font-bold text-gray-800 mb-4 capitalize">{pattern.category}</h3>
              <div className="space-y-3">
                <div>
                  <p className="text-sm text-gray-600">Pattern Type</p>
                  <p className="text-lg font-semibold text-indigo-600">{pattern.pattern_type}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-600">Average Spending</p>
                  <p className="text-lg font-semibold text-gray-800">₹{pattern.average?.toLocaleString()}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-600">Variability</p>
                  <div className="w-full bg-gray-200 rounded-full h-2 mt-1">
                    <div
                      className="bg-indigo-600 h-2 rounded-full"
                      style={{ width: `${Math.min(pattern.std_dev / pattern.average * 100, 100)}%` }}
                    ></div>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  };

  const renderTemporalPatterns = () => {
    if (!patterns?.temporal_patterns) return null;
    
    const dayData = patterns.temporal_patterns.day_of_week || {};
    const hourData = patterns.temporal_patterns.hour_of_day || {};

    const dayChartData = Object.entries(dayData).map(([day, amount]) => ({
      name: day,
      amount: amount
    }));

    const hourChartData = Object.entries(hourData).map(([hour, amount]) => ({
      hour: `${hour}:00`,
      amount: amount
    }));

    return (
      <div className="space-y-6">
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h3 className="font-bold text-gray-800 mb-4 flex items-center gap-2">
            <Clock className="w-5 h-5" />
            Day of Week Spending Pattern
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={dayChartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip formatter={(value) => `₹${value.toLocaleString()}`} />
              <Bar dataKey="amount" fill="#4F46E5" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="bg-white rounded-lg shadow-lg p-6">
          <h3 className="font-bold text-gray-800 mb-4 flex items-center gap-2">
            <Zap className="w-5 h-5" />
            Hour of Day Spending Pattern
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={hourChartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="hour" />
              <YAxis />
              <Tooltip formatter={(value) => `₹${value.toLocaleString()}`} />
              <Line type="monotone" dataKey="amount" stroke="#4F46E5" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    );
  };

  const renderBehavioralPatterns = () => {
    if (!patterns?.behavioral_patterns) return null;
    
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {patterns.behavioral_patterns.map((behavior, idx) => (
          <div key={idx} className="bg-white rounded-lg shadow-lg p-6">
            <h3 className="font-bold text-gray-800 mb-4 capitalize">{behavior.behavior_type}</h3>
            <div className="space-y-3">
              <div>
                <p className="text-sm text-gray-600">Category</p>
                <p className="text-lg font-semibold text-indigo-600 capitalize">{behavior.category}</p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Frequency</p>
                <p className="text-lg font-semibold text-gray-800">{behavior.frequency} times</p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Total Amount</p>
                <p className="text-lg font-semibold text-gray-800">₹{behavior.total_amount?.toLocaleString()}</p>
              </div>
            </div>
          </div>
        ))}
      </div>
    );
  };

  const renderAnomalies = () => {
    if (!patterns?.anomalies) return null;
    
    return (
      <div className="space-y-4">
        {patterns.anomalies.length === 0 ? (
          <div className="bg-green-50 border border-green-200 rounded-lg p-6 text-center">
            <CheckCircle className="w-12 h-12 text-green-600 mx-auto mb-3" />
            <p className="text-green-800 font-semibold">No anomalies detected!</p>
            <p className="text-green-700 mt-2">Your spending patterns are normal.</p>
          </div>
        ) : (
          patterns.anomalies.map((anomaly, idx) => (
            <div key={idx} className="bg-red-50 border border-red-200 rounded-lg p-6">
              <div className="flex items-start gap-4">
                <AlertTriangle className="w-6 h-6 text-red-600 mt-1 flex-shrink-0" />
                <div className="flex-1">
                  <h3 className="font-bold text-red-900 capitalize">{anomaly.anomaly_type}</h3>
                  <p className="text-red-800 mt-2">{anomaly.description}</p>
                  <div className="mt-3 grid grid-cols-2 gap-4">
                    <div>
                      <p className="text-sm text-red-700">Amount</p>
                      <p className="font-semibold text-red-900">₹{anomaly.amount?.toLocaleString()}</p>
                    </div>
                    <div>
                      <p className="text-sm text-red-700">Category</p>
                      <p className="font-semibold text-red-900 capitalize">{anomaly.category}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    );
  };

  const renderCorrelations = () => {
    if (!patterns?.correlations) return null;
    
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {patterns.correlations.map((corr, idx) => (
          <div key={idx} className="bg-white rounded-lg shadow-lg p-6">
            <div className="flex items-center gap-2 mb-4">
              <Link2 className="w-5 h-5 text-indigo-600" />
              <h3 className="font-bold text-gray-800">Category Correlation</h3>
            </div>
            <div className="space-y-3">
              <div>
                <p className="text-sm text-gray-600">Categories</p>
                <p className="text-lg font-semibold text-gray-800">
                  {corr.category1} ↔ {corr.category2}
                </p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Correlation Strength</p>
                <p className={`text-lg font-semibold ${corr.correlation_type === 'positive' ? 'text-green-600' : 'text-red-600'}`}>
                  {corr.correlation_type === 'positive' ? '↑' : '↓'} {corr.strength}
                </p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Correlation Value</p>
                <p className="text-lg font-semibold text-indigo-600">{(corr.correlation_value * 100).toFixed(1)}%</p>
              </div>
            </div>
          </div>
        ))}
      </div>
    );
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Analyzing patterns...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-800 flex items-center gap-3">
            <Activity className="w-10 h-10 text-indigo-600" />
            Pattern Recognition & Analysis
          </h1>
          <p className="text-gray-600 mt-2">Discover spending patterns and behavioral insights</p>
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6 text-red-700">
            {error}
          </div>
        )}

        {/* Tabs */}
        <div className="flex flex-wrap gap-2 mb-8 bg-white rounded-lg shadow-lg p-2">
          {[
            { id: 'all', label: 'All Patterns' },
            { id: 'spending', label: 'Spending Patterns' },
            { id: 'temporal', label: 'Temporal Patterns' },
            { id: 'behavioral', label: 'Behavioral Patterns' },
            { id: 'anomalies', label: 'Anomalies' },
            { id: 'correlations', label: 'Correlations' },
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`px-4 py-2 rounded-lg font-semibold transition ${
                activeTab === tab.id
                  ? 'bg-indigo-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>

        {/* Content */}
        <div>
          {activeTab === 'all' && patterns && (
            <div className="space-y-8">
              <div>
                <h2 className="text-2xl font-bold text-gray-800 mb-4">Spending Patterns</h2>
                {renderSpendingPatterns()}
              </div>
              <div>
                <h2 className="text-2xl font-bold text-gray-800 mb-4">Temporal Patterns</h2>
                {renderTemporalPatterns()}
              </div>
              <div>
                <h2 className="text-2xl font-bold text-gray-800 mb-4">Behavioral Patterns</h2>
                {renderBehavioralPatterns()}
              </div>
              <div>
                <h2 className="text-2xl font-bold text-gray-800 mb-4">Anomalies</h2>
                {renderAnomalies()}
              </div>
              <div>
                <h2 className="text-2xl font-bold text-gray-800 mb-4">Category Correlations</h2>
                {renderCorrelations()}
              </div>
            </div>
          )}
          {activeTab === 'spending' && renderSpendingPatterns()}
          {activeTab === 'temporal' && renderTemporalPatterns()}
          {activeTab === 'behavioral' && renderBehavioralPatterns()}
          {activeTab === 'anomalies' && renderAnomalies()}
          {activeTab === 'correlations' && renderCorrelations()}
        </div>
      </div>
    </div>
  );
}
