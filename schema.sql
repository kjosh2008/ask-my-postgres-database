-- Sample Database Schema for Company Database
-- This creates the example tables used in the demo

-- Create tables
CREATE TABLE IF NOT EXISTS departments (
    dept_id SERIAL PRIMARY KEY,
    dept_name VARCHAR(100) NOT NULL,
    location VARCHAR(100),
    budget DECIMAL(12,2),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS jobs (
    job_id VARCHAR(20) PRIMARY KEY,
    job_title VARCHAR(100) NOT NULL,
    min_salary DECIMAL(10,2),
    max_salary DECIMAL(10,2)
);

CREATE TABLE IF NOT EXISTS employees (
    employee_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(20),
    hire_date DATE,
    job_id VARCHAR(20) REFERENCES jobs(job_id),
    salary DECIMAL(10,2),
    dept_id INTEGER REFERENCES departments(dept_id),
    manager_id INTEGER REFERENCES employees(employee_id),
    status VARCHAR(20) DEFAULT 'ACTIVE',
    created_at TIMESTAMP DEFAULT NOW(),
    modified_by VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS projects (
    project_id SERIAL PRIMARY KEY,
    project_name VARCHAR(200) NOT NULL,
    description TEXT,
    start_date DATE,
    end_date DATE,
    budget DECIMAL(12,2),
    dept_id INTEGER REFERENCES departments(dept_id),
    status VARCHAR(20) DEFAULT 'PLANNING'
);

CREATE TABLE IF NOT EXISTS performance_reviews (
    review_id SERIAL PRIMARY KEY,
    employee_id INTEGER REFERENCES employees(employee_id),
    review_date DATE DEFAULT CURRENT_DATE,
    reviewer_id INTEGER,
    rating DECIMAL(2,1),
    comments VARCHAR(1000),
    goals_met VARCHAR(10)
);

CREATE TABLE IF NOT EXISTS salary_history (
    history_id SERIAL PRIMARY KEY,
    employee_id INTEGER REFERENCES employees(employee_id),
    old_salary DECIMAL(10,2),
    new_salary DECIMAL(10,2),
    change_date TIMESTAMP DEFAULT NOW(),
    change_reason VARCHAR(200),
    changed_by VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS ai_query_history (
    id SERIAL PRIMARY KEY,
    user_question TEXT,
    generated_sql TEXT,
    result_summary TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Optional: pgvector tables for semantic search
-- Requires: CREATE EXTENSION vector;

CREATE TABLE IF NOT EXISTS employee_embeddings (
    id SERIAL PRIMARY KEY,
    employee_id INTEGER REFERENCES employees(employee_id),
    content TEXT,
    embedding VECTOR(1536),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS department_embeddings (
    id SERIAL PRIMARY KEY,
    dept_id INTEGER REFERENCES departments(dept_id),
    content TEXT,
    embedding VECTOR(1536),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX idx_employees_dept ON employees(dept_id);
CREATE INDEX idx_employees_job ON employees(job_id);
CREATE INDEX idx_employees_status ON employees(status);
CREATE INDEX idx_projects_dept ON projects(dept_id);
CREATE INDEX idx_projects_status ON projects(status);

-- Create HNSW indexes for vector search (requires pgvector)
-- CREATE INDEX ON employee_embeddings USING hnsw (embedding vector_cosine_ops);
-- CREATE INDEX ON department_embeddings USING hnsw (embedding vector_cosine_ops);

-- Insert sample data (optional)
INSERT INTO departments (dept_name, location, budget) VALUES
    ('Information Technology', 'Edmonton', 150000.00),
    ('Human Resources', 'Edmonton', 80000.00),
    ('Finance', 'Toronto', 200000.00),
    ('Marketing', 'Vancouver', 120000.00),
    ('Sales', 'Calgary', 300000.00),
    ('AI Research', 'Edmonton', 250000.00);

INSERT INTO jobs (job_id, job_title, min_salary, max_salary) VALUES
    ('IT_PROG', 'IT Programmer', 50000.00, 120000.00),
    ('IT_MGR', 'IT Manager', 80000.00, 150000.00),
    ('DBA', 'Database Administrator', 70000.00, 140000.00),
    ('AI_ENG', 'AI Engineer', 90000.00, 180000.00),
    ('HR_REP', 'HR Representative', 40000.00, 80000.00),
    ('HR_MGR', 'HR Manager', 60000.00, 120000.00),
    ('FIN_ANA', 'Financial Analyst', 55000.00, 110000.00),
    ('FIN_MGR', 'Finance Manager', 75000.00, 145000.00),
    ('MKT_REP', 'Marketing Representative', 45000.00, 90000.00),
    ('MKT_MGR', 'Marketing Manager', 65000.00, 130000.00),
    ('SA_REP', 'Sales Representative', 40000.00, 100000.00),
    ('SA_MGR', 'Sales Manager', 70000.00, 140000.00);

-- Add more sample data as needed
