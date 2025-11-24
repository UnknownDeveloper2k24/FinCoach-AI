import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '../store/authStore';
import { LogOut, Menu, BarChart3, TrendingUp, Bot, Lightbulb, Activity } from 'lucide-react';

export default function Navbar() {
  const navigate = useNavigate();
  const { user, logout } = useAuthStore();
  const [isOpen, setIsOpen] = React.useState(false);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <nav className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center">
            <h1 className="text-2xl font-bold">FINCoach AI</h1>
          </div>

          <div className="hidden md:flex items-center space-x-6">
            <a href="/dashboard" className="hover:text-blue-200 transition flex items-center space-x-1">
              <span>Dashboard</span>
            </a>
            <a href="/analytics" className="hover:text-blue-200 transition flex items-center space-x-1">
              <BarChart3 className="w-4 h-4" />
              <span>Analytics</span>
            </a>
            <a href="/predictions" className="hover:text-blue-200 transition flex items-center space-x-1">
              <TrendingUp className="w-4 h-4" />
              <span>Predictions</span>
            </a>
            <a href="/multi-agent" className="hover:text-blue-200 transition flex items-center space-x-1">
              <Bot className="w-4 h-4" />
              <span>AI Agents</span>
            </a>
            <a href="/recommendations" className="hover:text-blue-200 transition flex items-center space-x-1">
              <Lightbulb className="w-4 h-4" />
              <span>Recommendations</span>
            </a>
            <a href="/patterns" className="hover:text-blue-200 transition flex items-center space-x-1">
              <Activity className="w-4 h-4" />
              <span>Patterns</span>
            </a>
          </div>

          <div className="flex items-center space-x-4">
            <span className="text-sm hidden sm:inline">{user?.full_name}</span>
            <button
              onClick={handleLogout}
              className="flex items-center space-x-2 bg-red-500 hover:bg-red-600 px-4 py-2 rounded-lg transition"
            >
              <LogOut className="w-4 h-4" />
              <span>Logout</span>
            </button>
          </div>

          <button
            onClick={() => setIsOpen(!isOpen)}
            className="md:hidden"
          >
            <Menu className="w-6 h-6" />
          </button>
        </div>

        {isOpen && (
          <div className="md:hidden pb-4 space-y-2">
            <a href="/dashboard" className="block hover:text-blue-200 transition">Dashboard</a>
            <a href="/analytics" className="block hover:text-blue-200 transition flex items-center space-x-1">
              <BarChart3 className="w-4 h-4" />
              <span>Analytics</span>
            </a>
            <a href="/predictions" className="block hover:text-blue-200 transition flex items-center space-x-1">
              <TrendingUp className="w-4 h-4" />
              <span>Predictions</span>
            </a>
            <a href="/multi-agent" className="block hover:text-blue-200 transition flex items-center space-x-1">
              <Bot className="w-4 h-4" />
              <span>AI Agents</span>
            </a>
            <a href="/recommendations" className="block hover:text-blue-200 transition flex items-center space-x-1">
              <Lightbulb className="w-4 h-4" />
              <span>Recommendations</span>
            </a>
            <a href="/patterns" className="block hover:text-blue-200 transition flex items-center space-x-1">
              <Activity className="w-4 h-4" />
              <span>Patterns</span>
            </a>
          </div>
        )}
      </div>
    </nav>
  );
}
