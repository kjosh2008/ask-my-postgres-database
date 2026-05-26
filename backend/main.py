"""
FastAPI Backend for Company AI Assistant
Connects to remote PostgreSQL on GCP and provides REST API
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import psycopg
from psycopg.rows import dict_row
import requests
import os
from typing import List, Dict, Any
import json

app = FastAPI(title="Company AI Assistant API")

# CORS - Allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', '34.19.137.246'),
    'dbname': os.getenv('DB_NAME', 'companydb'),  # ← CHANGED
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', ''),
    'port': os.getenv('DB_PORT', '5432')
}

# Ollama configuration (optional - can run on your Mac or GCP)
OLLAMA_HOST = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'llama3.2')


class QueryRequest(BaseModel):
    question: str


class QueryResponse(BaseModel):
    question: str
    sql: str
    results: List[Dict[str, Any]]
    answer: str
    row_count: int


def get_db_connection():
    """Get database connection"""
    try:
        conn = psycopg.connect(**DB_CONFIG, row_factory=dict_row)
        return conn
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")


def get_schema_context():
    """Get database schema for LLM context"""
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT 
                    table_name,
                    column_name,
                    data_type
                FROM information_schema.columns
                WHERE table_schema = 'public'
                AND table_name IN ('employees', 'departments', 'jobs', 'projects', 
                                  'performance_reviews', 'salary_history')
                ORDER BY table_name, ordinal_position;
            """)
            schema = cur.fetchall()
        
        schema_text = "DATABASE SCHEMA:\n\n"
        current_table = None
        for row in schema:
            if row['table_name'] != current_table:
                current_table = row['table_name']
                schema_text += f"\nTable: {current_table}\n"
            schema_text += f"  - {row['column_name']} ({row['data_type']})\n"
        
        return schema_text
    finally:
        conn.close()


def is_safe_query(sql: str) -> tuple[bool, str]:
    """Safety check for SQL queries"""
    sql_upper = sql.upper().strip()
    
    dangerous_keywords = ['DROP', 'DELETE', 'TRUNCATE', 'ALTER', 'CREATE', 'INSERT', 'UPDATE']
    for keyword in dangerous_keywords:
        if keyword in sql_upper:
            return False, f"Query contains dangerous keyword: {keyword}"
    
    if not sql_upper.startswith('SELECT'):
        return False, "Only SELECT queries are allowed"
    
    return True, "Query is safe"


def generate_sql_with_ollama(question: str) -> str:
    """Generate SQL using Ollama"""
    schema = get_schema_context()
    
    prompt = f"""You are a PostgreSQL expert. Convert the user's question into a safe SQL query.

{schema}

RULES:
- Generate ONLY SELECT queries
- Use proper JOINs
- Format currency with TO_CHAR(amount, '$999,999.99')
- Add LIMIT clauses for large results
- Return ONLY the SQL query, no explanations

USER QUESTION: {question}

SQL QUERY:"""

    try:
        response = requests.post(
            f"{OLLAMA_HOST}/api/generate",
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0.1}
            },
            timeout=30
        )
        
        if response.status_code == 200:
            sql = response.json()['response'].strip()
            
            # Clean up
            if sql.startswith('```sql'):
                sql = sql.replace('```sql', '').replace('```', '').strip()
            elif sql.startswith('```'):
                sql = sql.replace('```', '').strip()
            
            # Extract just SQL
            lines = sql.split('\n')
            sql_lines = [line.strip() for line in lines 
                        if line.strip() and not line.strip().startswith(('--', '#'))]
            sql = ' '.join(sql_lines)
            
            return sql
        else:
            raise Exception(f"Ollama API error: {response.status_code}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate SQL: {str(e)}")


def format_results_with_ollama(results: List[Dict], question: str) -> str:
    """Format results using Ollama"""
    if not results:
        return "No results found."
    
    results_text = json.dumps(results, indent=2, default=str)
    
    prompt = f"""Summarize these database results in natural language.

USER ASKED: {question}

RESULTS:
{results_text}

Provide a clear, concise summary. Include specific numbers and names."""

    try:
        response = requests.post(
            f"{OLLAMA_HOST}/api/generate",
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0.3}
            },
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()['response'].strip()
        else:
            # Fallback
            return f"Found {len(results)} result(s). See the data table below."
    except:
        return f"Found {len(results)} result(s). See the data table below."


@app.get("/")
async def root():
    """Health check"""
    return {
        "status": "running",
        "service": "Company AI Assistant API",
        "database": DB_CONFIG['host'],
        "ollama": OLLAMA_HOST
    }


@app.get("/health")
async def health_check():
    """Check if database and Ollama are accessible"""
    status = {
        "database": "disconnected",
        "ollama": "disconnected"
    }
    
    # Check database
    try:
        conn = get_db_connection()
        conn.close()
        status["database"] = "connected"
    except:
        pass
    
    # Check Ollama
    try:
        response = requests.get(f"{OLLAMA_HOST}/api/tags", timeout=5)
        if response.status_code == 200:
            status["ollama"] = "connected"
    except:
        pass
    
    return status


@app.get("/schema")
async def get_schema():
    """Get database schema"""
    return {"schema": get_schema_context()}


@app.get("/stats")
async def get_stats():
    """Get database statistics"""
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT 
                    'Employees' as table_name, COUNT(*) as count FROM employees
                UNION ALL
                SELECT 'Departments', COUNT(*) FROM departments
                UNION ALL
                SELECT 'Projects', COUNT(*) FROM projects
                UNION ALL
                SELECT 'Jobs', COUNT(*) FROM jobs
                UNION ALL
                SELECT 'Performance Reviews', COUNT(*) FROM performance_reviews
                UNION ALL
                SELECT 'Salary History', COUNT(*) FROM salary_history
                ORDER BY count DESC;
            """)
            stats = cur.fetchall()
        return {"statistics": stats}
    finally:
        conn.close()


@app.post("/query", response_model=QueryResponse)
async def execute_query(request: QueryRequest):
    """Execute natural language query"""
    question = request.question.strip()
    
    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
    # Generate SQL
    sql = generate_sql_with_ollama(question)
    
    # Safety check
    is_safe, safety_msg = is_safe_query(sql)
    if not is_safe:
        raise HTTPException(status_code=400, detail=f"Unsafe query: {safety_msg}")
    
    # Execute query
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
            results = [dict(row) for row in cur.fetchall()]
        
        # Format results
        answer = format_results_with_ollama(results, question)
        
        return QueryResponse(
            question=question,
            sql=sql,
            results=results,
            answer=answer,
            row_count=len(results)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query execution failed: {str(e)}")
    finally:
        conn.close()


@app.get("/employees")
async def get_employees():
    """Get all employees"""
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT 
                    e.*,
                    j.job_title,
                    d.dept_name
                FROM employees e
                JOIN jobs j ON e.job_id = j.job_id
                JOIN departments d ON e.dept_id = d.dept_id
                ORDER BY e.salary DESC
            """)
            employees = cur.fetchall()
        return {"employees": employees}
    finally:
        conn.close()


@app.get("/departments")
async def get_departments():
    """Get all departments with stats"""
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT 
                    d.*,
                    COUNT(e.employee_id) as employee_count,
                    COALESCE(SUM(e.salary), 0) as total_salaries,
                    ROUND(AVG(e.salary), 2) as avg_salary
                FROM departments d
                LEFT JOIN employees e ON d.dept_id = e.dept_id
                GROUP BY d.dept_id
                ORDER BY d.dept_name
            """)
            departments = cur.fetchall()
        return {"departments": departments}
    finally:
        conn.close()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
