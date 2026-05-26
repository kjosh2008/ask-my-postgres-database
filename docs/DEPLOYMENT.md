# Deployment Guide

Guide for deploying Ask My PostgreSQL Database to production.

## Table of Contents

1. [Docker Deployment](#docker-deployment)
2. [Cloud Deployment](#cloud-deployment)
3. [Environment Variables](#environment-variables)
4. [Security Considerations](#security-considerations)

## Docker Deployment

### Create Dockerfile for Backend

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install PostgreSQL client
RUN apt-get update && apt-get install -y postgresql-client

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Create Dockerfile for Frontend

```dockerfile
FROM node:18-alpine as build

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

### Docker Compose

```yaml
version: '3.8'

services:
  postgres:
    image: pgvector/pgvector:pg16
    environment:
      POSTGRES_DB: companydb
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  backend:
    build: ./backend
    environment:
      DB_HOST: postgres
      DB_NAME: companydb
      DB_USER: postgres
      DB_PASSWORD: ${DB_PASSWORD}
      OLLAMA_HOST: http://ollama:11434
    ports:
      - "8000:8000"
    depends_on:
      - postgres

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend

  ollama:
    image: ollama/ollama
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama

volumes:
  postgres_data:
  ollama_data:
```

### Deploy with Docker Compose

```bash
# Set environment variables
export DB_PASSWORD=your_secure_password

# Start all services
docker-compose up -d

# Pull Ollama model
docker exec -it <ollama_container_id> ollama pull llama3.2

# Check logs
docker-compose logs -f
```

## Cloud Deployment

### Deploy to GCP (Google Cloud Platform)

**1. Create VM Instance**

```bash
gcloud compute instances create ask-postgres-app \
  --zone=us-central1-a \
  --machine-type=e2-medium \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --boot-disk-size=50GB
```

**2. Install Dependencies**

```bash
# SSH into instance
gcloud compute ssh ask-postgres-app

# Install Docker
sudo apt-get update
sudo apt-get install -y docker.io docker-compose

# Clone repository
git clone https://github.com/kjosh2008/ask-my-postgres-database.git
cd ask-my-postgres-database
```

**3. Configure and Deploy**

```bash
# Set environment variables
echo "DB_PASSWORD=your_password" > .env

# Start services
sudo docker-compose up -d
```

**4. Configure Firewall**

```bash
gcloud compute firewall-rules create allow-http \
  --allow tcp:80 \
  --target-tags http-server

gcloud compute firewall-rules create allow-api \
  --allow tcp:8000 \
  --target-tags api-server
```

### Deploy to AWS

**1. Create EC2 Instance**

- AMI: Ubuntu 20.04 LTS
- Instance Type: t3.medium
- Storage: 50GB
- Security Group: Allow ports 80, 8000, 22

**2. Install and Configure**

```bash
# SSH into instance
ssh -i your-key.pem ubuntu@your-instance-ip

# Install Docker
sudo apt-get update
sudo apt-get install -y docker.io docker-compose

# Clone and deploy (same as GCP)
```

### Deploy Frontend to Vercel/Netlify

**1. Build Frontend**

```bash
cd frontend
npm run build
```

**2. Deploy to Vercel**

```bash
npm install -g vercel
vercel deploy --prod
```

**3. Update API URL**

Update `VITE_API_URL` in Vercel environment variables to point to your backend.

## Environment Variables

### Production Environment Variables

**Backend (.env)**
```env
# Database - Use production credentials
DB_HOST=your-db-host
DB_NAME=production_db
DB_USER=app_user
DB_PASSWORD=strong_random_password
DB_PORT=5432

# Ollama
OLLAMA_HOST=http://ollama:11434
OLLAMA_MODEL=llama3.2

# Security
ALLOWED_ORIGINS=https://your-frontend-domain.com

# Optional
SENTRY_DSN=your_sentry_dsn
LOG_LEVEL=INFO
```

**Frontend**
```env
VITE_API_URL=https://api.your-domain.com
```

## Security Considerations

### 1. Database Security

- ✅ Use strong passwords
- ✅ Enable SSL/TLS for database connections
- ✅ Use separate database user with limited permissions
- ✅ Regularly backup database
- ✅ Keep PostgreSQL updated

**Create Limited User:**
```sql
CREATE USER app_user WITH PASSWORD 'strong_password';
GRANT SELECT ON ALL TABLES IN SCHEMA public TO app_user;
```

### 2. API Security

**Add Rate Limiting:**
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/query")
@limiter.limit("10/minute")
async def execute_query(request: Request):
    # ...
```

**Add Authentication:**
```python
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

@app.post("/query")
async def execute_query(
    request: QueryRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    # Verify token
    # ...
```

### 3. HTTPS/SSL

**Use Let's Encrypt with Nginx:**
```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

### 4. Environment Variables

- ✅ Never commit `.env` files
- ✅ Use secret managers (AWS Secrets Manager, GCP Secret Manager)
- ✅ Rotate credentials regularly

### 5. Monitoring

**Add Logging:**
```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.post("/query")
async def execute_query(request: QueryRequest):
    logger.info(f"Query received: {request.question}")
    # ...
```

**Add Health Checks:**
```python
@app.get("/healthz")
async def health():
    # Check database connection
    # Check Ollama connection
    return {"status": "healthy"}
```

## Performance Optimization

### 1. Database Optimization

- Create indexes on frequently queried columns
- Use connection pooling
- Enable query caching

### 2. Backend Optimization

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def get_schema_context():
    # Cache schema for faster responses
    pass
```

### 3. Frontend Optimization

- Enable gzip compression
- Use CDN for static assets
- Implement lazy loading

## Monitoring & Logging

### Sentry Integration

```python
import sentry_sdk

sentry_sdk.init(
    dsn="your-sentry-dsn",
    traces_sample_rate=1.0,
)
```

### Prometheus Metrics

```python
from prometheus_fastapi_instrumentator import Instrumentator

Instrumentator().instrument(app).expose(app)
```

## Backup Strategy

### Database Backups

```bash
# Automated daily backups
0 2 * * * pg_dump -U postgres companydb > /backups/db_$(date +\%Y\%m\%d).sql
```

### Application Backups

- Regular snapshots of VM instances
- Git repository for code
- S3/GCS for file storage

## Rollback Plan

1. Keep previous Docker images tagged
2. Maintain database migrations
3. Document deployment steps
4. Test rollback procedure

---

**Need help with deployment?** Open an issue on GitHub!
