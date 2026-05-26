# Ask My PostgreSQL Database 🤖

Natural language interface for PostgreSQL databases using AI. Ask questions in plain English and get SQL queries, natural language answers, and data visualizations.

![Demo](docs/demo.gif)

## ✨ Features

- 🗣️ **Natural Language Queries** - Ask questions in plain English
- 🤖 **Local LLM** - Uses Ollama (100% free, no API costs)
- 🔒 **Safe Execution** - Only SELECT queries allowed
- 📊 **Beautiful UI** - Modern React interface
- 🚀 **Fast** - All processing happens locally
- 🔍 **Vector Search** - Semantic search with pgvector (optional)
- 📝 **Query History** - All queries logged automatically

## 🏗️ Architecture

```
┌─────────────────┐
│  React Frontend │ (http://localhost:3000)
│   (Vite + CSS)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  FastAPI Backend│ (http://localhost:8000)
│   + Ollama LLM  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   PostgreSQL    │ (Local or Remote)
│   + pgvector    │
└─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.10+**
- **Node.js 18+**
- **PostgreSQL 13+** (local or remote)
- **Ollama** (for local LLM)

### Installation

**1. Clone the repository**

```bash
git clone https://github.com/kjosh2008/ask-my-postgres-database.git
cd ask-my-postgres-database
```

**2. Install Ollama and pull model**

```bash
# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.com/install.sh | sh

# Pull the model
ollama pull llama3.2
```

**3. Setup Backend**

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure database connection
cp .env.example .env
# Edit .env with your database credentials
```

**4. Setup Frontend**

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

**5. Start the application**

```bash
# Terminal 1: Start backend
cd backend
source venv/bin/activate
python main.py

# Terminal 2: Start frontend
cd frontend
npm run dev
```

Open http://localhost:3000 in your browser! 🎉

## 📖 Usage Examples

**Simple Questions:**
- "Who are the highest paid employees?"
- "Show me all employees in Finance"
- "What's the average salary by department?"

**Complex Queries:**
- "Which departments are over budget?"
- "List employees hired in the last 6 months"
- "Show me projects that are in progress with their budgets"

**Analytical Questions:**
- "What's the salary distribution across departments?"
- "Who got raises in the last year?"
- "Show me performance review trends"

## 🔧 Configuration

### Backend Configuration

Edit `backend/.env`:

```env
# Database
DB_HOST=localhost
DB_NAME=your_database
DB_USER=postgres
DB_PASSWORD=your_password
DB_PORT=5432

# Ollama
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama3.2
```

### Frontend Configuration

Edit `frontend/src/App.jsx`:

```javascript
const API_URL = 'http://localhost:8000'  // Backend URL
```

## 🗄️ Database Setup

### Enable pgvector (Optional - for semantic search)

```sql
CREATE EXTENSION vector;
```

### Create Embedding Tables (Optional)

```sql
-- Employee embeddings for semantic search
CREATE TABLE employee_embeddings (
    id serial PRIMARY KEY,
    employee_id integer REFERENCES employees(employee_id),
    content text,
    embedding vector(1536),
    created_at timestamp DEFAULT now()
);

-- Create HNSW index for fast similarity search
CREATE INDEX ON employee_embeddings USING hnsw (embedding vector_cosine_ops);
```

### Generate Embeddings (Optional)

```bash
# Requires OpenAI API key
export OPENAI_API_KEY='your-key'
python generate_embeddings.py
```

## 🔒 Security Features

- ✅ **Read-only queries** - Only SELECT statements allowed
- ✅ **SQL injection protection** - Parameterized queries
- ✅ **Keyword blocking** - Dangerous operations blocked (DROP, DELETE, etc.)
- ✅ **Query logging** - All queries logged to database
- ✅ **CORS protection** - Only localhost allowed in development

## 📊 API Endpoints

### GET /
Health check and service info

### GET /health
Check database and Ollama connectivity

### POST /query
Execute natural language query
```json
{
  "question": "Who are the highest paid employees?"
}
```

### GET /stats
Get database statistics

### GET /employees
Get all employees with job and department info

### GET /departments
Get all departments with statistics

## 🎨 Customization

### Change Color Theme

Edit `frontend/src/App.css`:

```css
:root {
  --primary: #2563eb;      /* Your brand color */
  --primary-dark: #1e40af;
  /* ... */
}
```

### Add Example Questions

Edit `frontend/src/App.jsx`:

```javascript
const exampleQuestions = [
  "Your custom question here",
  // ...
]
```

### Use Different LLM Model

```bash
# Pull a different model
ollama pull mistral

# Update .env
OLLAMA_MODEL=mistral
```

## 🐛 Troubleshooting

**Backend won't start:**
- Check Ollama is running: `ollama list`
- Verify database connection: `psql -h localhost -U postgres -d dbname`

**Frontend shows blank page:**
- Check browser console (F12) for errors
- Verify backend is running: http://localhost:8000

**Database connection failed:**
- Check credentials in `.env`
- Ensure PostgreSQL is running
- For remote DB, check firewall rules

**"Failed to fetch" error:**
- Backend not running on port 8000
- CORS issue - check allowed origins in `main.py`

## 📁 Project Structure

```
ask-my-postgres-database/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── requirements.txt     # Python dependencies
│   ├── .env.example         # Environment template
│   └── generate_embeddings.py  # Optional embeddings
├── frontend/
│   ├── src/
│   │   ├── App.jsx          # Main React component
│   │   ├── App.css          # Styles
│   │   └── main.jsx         # Entry point
│   ├── package.json         # Node dependencies
│   └── vite.config.js       # Vite configuration
├── docs/                    # Documentation
├── .gitignore
└── README.md
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Ollama](https://ollama.com/) - Local LLM runtime
- [pgvector](https://github.com/pgvector/pgvector) - Vector similarity search
- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [React](https://react.dev/) - UI framework
- [Vite](https://vitejs.dev/) - Frontend build tool

## 📧 Contact

Kshitij Joshi - [@kjosh2008](https://github.com/kjosh2008)

Project Link: [https://github.com/kjosh2008/ask-my-postgres-database](https://github.com/kjosh2008/ask-my-postgres-database)

---

**Built with ❤️ using PostgreSQL + Ollama + FastAPI + React**

**100% Open Source • No API Costs • Privacy First**
