#!/bin/bash

# FINCoach AI - Quick Start Script
# This script sets up and runs both backend and frontend

set -e

echo "🚀 FINCoach AI - Quick Start"
echo "=============================="

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check prerequisites
echo -e "${BLUE}Checking prerequisites...${NC}"

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    exit 1
fi

if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed"
    exit 1
fi

if ! command -v psql &> /dev/null; then
    echo "⚠️  PostgreSQL client not found. Make sure PostgreSQL server is running."
fi

echo -e "${GREEN}✓ Prerequisites check passed${NC}"

# Setup Backend
echo -e "\n${BLUE}Setting up Backend...${NC}"
cd backend

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt > /dev/null 2>&1

if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo -e "${YELLOW}⚠️  Please edit backend/.env with your database credentials${NC}"
fi

echo -e "${GREEN}✓ Backend setup complete${NC}"

# Setup Frontend
echo -e "\n${BLUE}Setting up Frontend...${NC}"
cd ../frontend

if [ ! -d "node_modules" ]; then
    echo "Installing dependencies..."
    npm install > /dev/null 2>&1
fi

echo -e "${GREEN}✓ Frontend setup complete${NC}"

# Summary
echo -e "\n${GREEN}=============================="
echo "✓ Setup Complete!"
echo "==============================${NC}"

echo -e "\n${BLUE}To start the application:${NC}"
echo ""
echo "Terminal 1 - Backend:"
echo "  cd backend"
echo "  source venv/bin/activate"
echo "  python -m uvicorn app.main:app --reload"
echo ""
echo "Terminal 2 - Frontend:"
echo "  cd frontend"
echo "  npm run dev"
echo ""
echo -e "${BLUE}Then open:${NC}"
echo "  Frontend: http://localhost:5173"
echo "  Backend API: http://localhost:8000"
echo "  API Docs: http://localhost:8000/docs"
echo ""
