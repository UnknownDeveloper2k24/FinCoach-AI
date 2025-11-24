# FINCoach AI - Complete Setup Guide

This guide will help you set up and run the complete FINCoach AI application (Backend + Frontend).

## 📋 Prerequisites

- Python 3.9+
- Node.js 16+
- PostgreSQL 12+
- Git
- npm or yarn

## 🔧 Backend Setup

### Step 1: Navigate to Backend Directory
```bash
cd backend
```

### Step 2: Create Virtual Environment
```bash
# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables
```bash
cp .env.example .env
```

Edit `.env` with your settings:
```
DATABASE_URL=postgresql://username:password@localhost:5432/fincoach_db
SECRET_KEY=your-super-secret-key-change-this
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Step 5: Create Database
```bash
createdb -h localhost -U postgres fincoach_db
```

### Step 6: Run Database Migrations
```bash
alembic upgrade head
```

### Step 7: Start Backend Server
```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

✅ Backend is now running at: `http://localhost:8000`

**API Documentation:**
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

## 🎨 Frontend Setup

### Step 1: Navigate to Frontend Directory
```bash
cd frontend
```

### Step 2: Install Dependencies
```bash
npm install
```

### Step 3: Configure Environment Variables
The `.env` file is already configured:
```
VITE_API_URL=http://localhost:8000/api/v1
```

If your backend is on a different URL, update this value.

### Step 4: Start Development Server
```bash
npm run dev
```

✅ Frontend is now running at: `http://localhost:5173`

---

## 🚀 Running Both Services

### Option 1: Using Two Terminal Windows

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
python -m uvicorn app.main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

### Option 2: Using Docker (Optional)

Create a `docker-compose.yml` in the root directory:

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: fincoach_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  backend:
    build: ./backend
    command: python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://postgres:postgres@postgres:5432/fincoach_db
      SECRET_KEY: your-secret-key
    depends_on:
      - postgres
    volumes:
      - ./backend:/app

  frontend:
    build: ./frontend
    command: npm run dev
    ports:
      - "5173:5173"
    environment:
      VITE_API_URL: http://localhost:8000/api/v1
    volumes:
      - ./frontend:/app
      - /app/node_modules

volumes:
  postgres_data:
```

Then run:
```bash
docker-compose up
```

---

## 📝 First Time Usage

### 1. Create an Account
- Go to `http://localhost:5173`
- Click "Register"
- Fill in your details:
  - Full Name
  - Email
  - Username
  - Password
  - Monthly Income
  - Monthly Budget

### 2. Login
- Use your credentials to login
- You'll be redirected to the Dashboard

### 3. Explore Features
- **Dashboard**: View your financial overview
- **Transactions**: Add income/expense transactions
- **Goals**: Set and track financial goals
- **Jars**: Create savings jars for specific purposes
- **Alerts**: Receive financial alerts

---

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
pytest --cov=app  # With coverage
```

### Frontend Tests
```bash
cd frontend
npm test
```

---

## 🔍 Troubleshooting

### Backend Issues

**Issue: Database connection error**
```
Solution: Ensure PostgreSQL is running and DATABASE_URL is correct
```

**Issue: Port 8000 already in use**
```bash
# Use a different port
python -m uvicorn app.main:app --reload --port 8001
```

**Issue: Module not found errors**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Frontend Issues

**Issue: API connection errors**
```
Solution: Check VITE_API_URL in .env matches your backend URL
```

**Issue: Port 5173 already in use**
```bash
# Vite will automatically use the next available port
npm run dev
```

**Issue: Node modules issues**
```bash
rm -rf node_modules package-lock.json
npm install
```

---

## 📦 Building for Production

### Backend
```bash
cd backend
# Create a production-ready build
pip install gunicorn
gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker
```

### Frontend
```bash
cd frontend
npm run build
# Output will be in dist/ directory
```

---

## 🌐 Deployment

### Deploy Backend to Heroku
```bash
cd backend
heroku create your-app-name
git push heroku main
```

### Deploy Frontend to Vercel
```bash
cd frontend
npm install -g vercel
vercel
```

---

## 📚 API Endpoints Reference

### Authentication
- `POST /api/v1/auth/register` - Register
- `POST /api/v1/auth/login` - Login
- `POST /api/v1/auth/refresh` - Refresh token

### Users
- `GET /api/v1/users/me` - Get current user
- `PUT /api/v1/users/me` - Update profile

### Transactions
- `GET /api/v1/transactions` - List transactions
- `POST /api/v1/transactions` - Create transaction
- `GET /api/v1/transactions/stats/summary` - Get summary

### Jars
- `GET /api/v1/jars` - List jars
- `POST /api/v1/jars` - Create jar
- `POST /api/v1/jars/{id}/add-funds` - Add funds

### Goals
- `GET /api/v1/goals` - List goals
- `POST /api/v1/goals` - Create goal
- `POST /api/v1/goals/{id}/add-progress` - Add progress

### Alerts
- `GET /api/v1/alerts` - List alerts
- `POST /api/v1/alerts` - Create alert

---

## 🆘 Getting Help

- Check the backend README: `backend/README.md`
- Check the frontend README: `frontend/README.md`
- Review API docs at: `http://localhost:8000/docs`
- Open an issue on GitHub

---

**Last Updated**: November 25, 2025
**Version**: 1.0.0
