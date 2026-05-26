# Detailed Setup Guide

This guide will walk you through setting up the application step by step.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Database Setup](#database-setup)
3. [Backend Setup](#backend-setup)
4. [Frontend Setup](#frontend-setup)
5. [Production Deployment](#production-deployment)

## Prerequisites

### Required Software

- **Python 3.10 or higher**
  ```bash
  python --version  # Should show 3.10+
  ```

- **Node.js 18 or higher**
  ```bash
  node --version  # Should show 18+
  ```

- **PostgreSQL 13 or higher**
  ```bash
  psql --version  # Should show 13+
  ```

- **Ollama**
  ```bash
  ollama --version
  ```

### Optional Software

- **Git** for version control
- **Docker** for containerized deployment

## Database Setup

### Local PostgreSQL

**1. Install PostgreSQL**

```bash
# macOS
brew install postgresql@18

# Ubuntu/Debian
sudo apt install postgresql-18

# Start service
brew services start postgresql@18  # macOS
sudo systemctl start postgresql     # Linux
```

**2. Create Database**

```bash
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE companydb;

# Connect to it
\c companydb

# Create sample tables (optional)
-- See schema.sql in docs/
```

**3. Install pgvector (Optional)**

```bash
# macOS
brew install pgvector

# Ubuntu/Debian
sudo apt install postgresql-18-pgvector

# Enable in database
psql -U postgres -d companydb
CREATE EXTENSION vector;
```

### Remote PostgreSQL (GCP, AWS, etc.)

**1. Create SSH Tunnel**

```bash
# For GCP
gcloud compute ssh your-vm-name \
  --zone=your-zone \
  -- -L 5432:localhost:5432 -N
```

**2. Configure Connection**

Update `backend/.env`:
```env
DB_HOST=localhost  # When using SSH tunnel
DB_NAME=your_database
DB_USER=your_user
DB_PASSWORD=your_password
```

## Backend Setup

**1. Navigate to Backend Directory**

```bash
cd backend
```

**2. Create Virtual Environment**

```bash
# Create venv
python -m venv venv

# Activate
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

**3. Install Dependencies**

```bash
pip install -r requirements.txt
```

**4. Configure Environment**

```bash
# Copy example env file
cp .env.example .env

# Edit with your values
nano .env  # or use your preferred editor
```

**5. Test Backend**

```bash
python main.py
```

Visit http://localhost:8000 - you should see:
```json
{
  "status": "running",
  "service": "Company AI Assistant API"
}
```

## Frontend Setup

**1. Navigate to Frontend Directory**

```bash
cd frontend
```

**2. Install Dependencies**

```bash
npm install
```

**3. Configure API URL**

If your backend is not on `localhost:8000`, edit `src/App.jsx`:

```javascript
const API_URL = 'http://your-backend-url:8000'
```

**4. Start Development Server**

```bash
npm run dev
```

Visit http://localhost:3000

## Ollama Setup

**1. Install Ollama**

```bash
# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.com/install.sh | sh

# Windows - Download from ollama.com
```

**2. Pull Model**

```bash
ollama pull llama3.2
```

**3. Verify Installation**

```bash
ollama list
# Should show llama3.2
```

**4. Test Ollama**

```bash
ollama run llama3.2 "Hello"
```

## Running the Application

### Development Mode

**Terminal 1: Backend**
```bash
cd backend
source venv/bin/activate
export DB_HOST=localhost
export DB_PASSWORD=your_password
python main.py
```

**Terminal 2: Frontend**
```bash
cd frontend
npm run dev
```

**Terminal 3: SSH Tunnel (if using remote DB)**
```bash
gcloud compute ssh your-vm --zone=your-zone -- -L 5432:localhost:5432 -N
```

### Accessing the Application

Open http://localhost:3000 in your browser!

## Troubleshooting

### Backend Issues

**Database Connection Failed**
```bash
# Test connection manually
psql -h localhost -U postgres -d companydb

# Check SSH tunnel is running
ps aux | grep "5432:localhost:5432"
```

**Ollama Connection Failed**
```bash
# Check if Ollama is running
ollama list

# Start Ollama service
ollama serve
```

**Port Already in Use**
```bash
# Find process using port 8000
lsof -ti:8000

# Kill it
kill -9 $(lsof -ti:8000)
```

### Frontend Issues

**Failed to Fetch**
- Check backend is running on port 8000
- Check CORS settings in `main.py`
- Check browser console for errors

**Blank Page**
- Open browser console (F12)
- Check for JavaScript errors
- Verify API_URL in `App.jsx`

### Database Issues

**Authentication Failed**
- Check password in `.env`
- Verify user exists: `psql -U postgres -c "\du"`
- Check `pg_hba.conf` for authentication method

**Connection Timeout**
- Check firewall rules
- Verify PostgreSQL is listening on correct port
- Check `listen_addresses` in `postgresql.conf`

## Next Steps

- Add your own database schema
- Customize the UI
- Deploy to production (see DEPLOYMENT.md)
- Enable semantic search with embeddings

## Getting Help

- Check existing [GitHub Issues](https://github.com/kjosh2008/ask-my-postgres-database/issues)
- Read the [FAQ](docs/FAQ.md)
- Open a new issue if you're stuck

---

Happy coding! 🚀
