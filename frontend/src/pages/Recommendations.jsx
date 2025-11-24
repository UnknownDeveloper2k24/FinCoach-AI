import React, { useEffect, useState } from 'react';
import { useAuthStore } from '../store/authStore';
import apiClient from '../services/apiClient';
import { API_ENDPOINTS } from '../config/api';
import { Lightbulb, TrendingDown, Target, AlertCircle, CheckCircle } from 'lucide-react';

export default function Recommendations() {
  const { user } = useAuthStore();
  const [recommendations, setRecommendations] = useState([]);
  const [categoryRecommendations, setCategoryRecommendations] = useState({});
  const [loading, setLoading] = useState(true);
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchRecommendations();
  }, []);

  const fetchRecommendations = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await apiClient.get(API_ENDPOINTS.RECOMMENDATIONS.PERSONALIZED);
      setRecommendations(response.data.recommendations || []);
    } catch (error) {
      console.error('Error fetching recommendations:', error);
      setError('Failed to load recommendations. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const fetchCategoryRecommendations = async (category) => {
    try {
      if (categoryRecommendations[category]) {
        setSelectedCategory(category);
        return;
      }
      const response = await apiClient.get(API_ENDPOINTS.RECOMMENDATIONS.CATEGORY(category));
      setCategoryRecommendations(prev => ({
        ...prev,
        [category]: response.data.recommendations || []
      }));
      setSelectedCategory(category);
    } catch (error) {
      console.error('Error fetching category recommendations:', error);
      setError('Failed to load category recommendations.');
    }
  };

  const getRecommendationIcon = (type) => {
    switch (type) {
      case 'Consolidation':
        return <TrendingDown className="w-5 h-5" />;
      case 'Budget Review':
        return <AlertCircle className="w-5 h-5" />;
      case 'Savings Opportunity':
        return <Target className="w-5 h-5" />;
      case 'Goal Acceleration':
        return <CheckCircle className="w-5 h-5" />;
      default:
        return <Lightbulb className="w-5 h-5" />;
    }
  };

  const getRecommendationColor = (type) => {
    switch (type) {
      case 'Consolidation':
        return 'bg-blue-50 border-blue-200';
      case 'Budget Review':
        return 'bg-orange-50 border-orange-200';
      case 'Savings Opportunity':
        return 'bg-green-50 border-green-200';
      case 'Goal Acceleration':
        return 'bg-purple-50 border-purple-200';
      case 'Subscription Audit':
        return 'bg-red-50 border-red-200';
      case 'Trend Alert':
        return 'bg-yellow-50 border-yellow-200';
      default:
        return 'bg-gray-50 border-gray-200';
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading recommendations...</p>
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
            <Lightbulb className="w-10 h-10 text-yellow-500" />
            Personalized Recommendations
          </h1>
          <p className="text-gray-600 mt-2">AI-powered insights to improve your financial health</p>
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6 text-red-700">
            {error}
          </div>
        )}

        {recommendations.length === 0 ? (
          <div className="bg-white rounded-lg shadow-lg p-12 text-center">
            <Lightbulb className="w-16 h-16 text-gray-300 mx-auto mb-4" />
            <p className="text-gray-600 text-lg">No recommendations available yet.</p>
            <p className="text-gray-500 mt-2">Add more transactions to get personalized recommendations.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Main Recommendations */}
            <div className="lg:col-span-2">
              <div className="space-y-4">
                {recommendations.map((rec, index) => (
                  <div
                    key={index}
                    className={`border-l-4 rounded-lg p-6 ${getRecommendationColor(rec.type)}`}
                  >
                    <div className="flex items-start gap-4">
                      <div className="text-indigo-600 mt-1">
                        {getRecommendationIcon(rec.type)}
                      </div>
                      <div className="flex-1">
                        <h3 className="font-bold text-gray-800 text-lg">{rec.type}</h3>
                        <p className="text-gray-700 mt-2">{rec.description}</p>
                        {rec.potential_savings && (
                          <div className="mt-3 bg-white bg-opacity-60 rounded p-3">
                            <p className="text-sm text-gray-600">
                              <span className="font-semibold">Potential Savings:</span> ₹{rec.potential_savings.toLocaleString()}
                            </p>
                          </div>
                        )}
                        {rec.category && (
                          <div className="mt-2">
                            <span className="inline-block bg-white bg-opacity-60 px-3 py-1 rounded-full text-sm text-gray-700">
                              {rec.category}
                            </span>
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Categories Sidebar */}
            <div className="lg:col-span-1">
              <div className="bg-white rounded-lg shadow-lg p-6 sticky top-8">
                <h3 className="font-bold text-gray-800 mb-4">Category Insights</h3>
                <div className="space-y-2">
                  {['dining', 'shopping', 'entertainment', 'utilities', 'transportation'].map((category) => (
                    <button
                      key={category}
                      onClick={() => fetchCategoryRecommendations(category)}
                      className={`w-full text-left px-4 py-2 rounded-lg transition ${
                        selectedCategory === category
                          ? 'bg-indigo-600 text-white'
                          : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                      }`}
                    >
                      <span className="capitalize">{category}</span>
                    </button>
                  ))}
                </div>

                {selectedCategory && categoryRecommendations[selectedCategory] && (
                  <div className="mt-6 pt-6 border-t">
                    <h4 className="font-semibold text-gray-800 mb-3 capitalize">
                      {selectedCategory} Recommendations
                    </h4>
                    <div className="space-y-2">
                      {categoryRecommendations[selectedCategory].map((rec, idx) => (
                        <div key={idx} className="bg-indigo-50 p-3 rounded text-sm text-gray-700">
                          <p className="font-semibold text-indigo-900">{rec.type}</p>
                          <p className="text-indigo-800 mt-1">{rec.description}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
