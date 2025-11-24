# FINCoach AI - Deployment Guide

Complete guide for deploying FINCoach AI to production.

## 🚀 Deployment Options

### Option 1: Deploy to AWS

#### Backend (EC2 + RDS)

1. **Create EC2 Instance**
   - Ubuntu 22.04 LTS
   - t3.medium or larger
   - Security group: Allow ports 22, 80, 443, 8000

2. **Install Dependencies**
   ```bash
   sudo apt update && sudo apt upgrade -y
   sudo apt install python3.11 python3-pip python3-venv nginx -y
   ```

3. **Clone Repository**
   ```bash
   git clone https://github.com/UnknownDeveloper2k24/FinCoach-AI.git
   cd FinCoach-AI/backend
   ```

4. **Setup Backend**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

5. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with production values
   ```

6. **Setup Nginx**
   ```bash
   sudo nano /etc/nginx/sites-available/fincoach
   ```
   
   Add:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

7. **Enable Site**
   ```bash
   sudo ln -s /etc/nginx/sites-available/fincoach /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

8. **Run Backend with Gunicorn**
   ```bash
   pip install gunicorn
   gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
   ```

#### Frontend (S3 + CloudFront)

1. **Build Frontend**
   ```bash
   cd frontend
   npm run build
   ```

2. **Create S3 Bucket**
   - Enable static website hosting
   - Upload `dist/` contents

3. **Setup CloudFront**
   - Create distribution pointing to S3
   - Set default root object to `index.html`

---

### Option 2: Deploy to Heroku

#### Backend

1. **Install Heroku CLI**
   ```bash
   curl https://cli-assets.heroku.com/install.sh | sh
   ```

2. **Login to Heroku**
   ```bash
   heroku login
   ```

3. **Create Heroku App**
   ```bash
   cd backend
   heroku create your-app-name
   ```

4. **Add PostgreSQL**
   ```bash
   heroku addons:create heroku-postgresql:standard-0
   ```

5. **Set Environment Variables**
   ```bash
   heroku config:set SECRET_KEY=your-secret-key
   heroku config:set ALGORITHM=HS256
   ```

6. **Create Procfile**
   ```
   web: gunicorn app.main:app --worker-class uvicorn.workers.UvicornWorker
   ```

7. **Deploy**
   ```bash
   git push heroku main
   ```

#### Frontend

1. **Deploy to Vercel**
   ```bash
   cd frontend
   npm install -g vercel
   vercel
   ```

2. **Configure Environment**
   - Set `VITE_API_URL` to your Heroku backend URL

---

### Option 3: Deploy with Docker

1. **Create Backend Dockerfile**
   ```dockerfile
   FROM python:3.11-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   CMD ["gunicorn", "app.main:app", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
   ```

2. **Create Frontend Dockerfile**
   ```dockerfile
   FROM node:18-alpine as build
   WORKDIR /app
   COPY package*.json .
   RUN npm install
   COPY . .
   RUN npm run build

   FROM nginx:alpine
   COPY --from=build /app/dist /usr/share/nginx/html
   EXPOSE 80
   CMD ["nginx", "-g", "daemon off;"]
   ```

3. **Build Images**
   ```bash
   docker build -t fincoach-backend ./backend
   docker build -t fincoach-frontend ./frontend
   ```

4. **Push to Docker Hub**
   ```bash
   docker tag fincoach-backend your-username/fincoach-backend
   docker push your-username/fincoach-backend
   ```

---

## 🔒 Security Checklist

- [ ] Change SECRET_KEY to a strong random value
- [ ] Set DEBUG=False in production
- [ ] Use HTTPS/SSL certificates
- [ ] Configure CORS properly
- [ ] Set up database backups
- [ ] Enable database encryption
- [ ] Use environment variables for secrets
- [ ] Set up monitoring and logging
- [ ] Configure rate limiting
- [ ] Enable CSRF protection
- [ ] Set up firewall rules
- [ ] Regular security updates

---

## 📊 Monitoring & Logging

### Backend Monitoring
```bash
# Install monitoring tools
pip install prometheus-client
pip install python-json-logger
```

### Frontend Monitoring
```bash
# Install Sentry for error tracking
npm install @sentry/react
```

---

## 🔄 CI/CD Pipeline

### GitHub Actions Example

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Deploy Backend
        run: |
          cd backend
          pip install -r requirements.txt
          # Add deployment commands
      
      - name: Deploy Frontend
        run: |
          cd frontend
          npm install
          npm run build
          # Add deployment commands
```

---

## 📈 Scaling Considerations

1. **Database**
   - Use read replicas for scaling reads
   - Implement caching (Redis)
   - Regular backups

2. **Backend**
   - Use load balancer
   - Horizontal scaling with multiple instances
   - API rate limiting

3. **Frontend**
   - CDN for static assets
   - Lazy loading
   - Code splitting

---

## 🆘 Troubleshooting

### Backend Won't Start
```bash
# Check logs
journalctl -u fincoach -f

# Verify database connection
psql -h localhost -U postgres -d fincoach_db
```

### Frontend Not Loading
```bash
# Check build
npm run build

# Verify environment variables
echo $VITE_API_URL
```

---

**Last Updated**: November 25, 2025
