import { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [question, setQuestion] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const [stats, setStats] = useState(null)

  const API_URL = 'http://localhost:8000'

  // Fetch stats on load
 useEffect(() => {
  fetchStats()
  }, [])

  const fetchStats = async () => {
    try {
      const response = await fetch(`${API_URL}/stats`)
      const data = await response.json()
      setStats(data.statistics)
    } catch (err) {
      console.error('Failed to fetch stats:', err)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!question.trim()) return

    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const response = await fetch(`${API_URL}/query`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question: question.trim() }),
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Query failed')
      }

      const data = await response.json()
      setResult(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const exampleQuestions = [
    "Who are the highest paid employees?",
    "Which departments are over budget?",
    "Show me all employees hired in 2023",
    "What projects are in progress?",
    "What's the average salary by department?"
  ]

  return (
    <div className="app">
      <header className="header">
        <h1>🤖 Company AI Assistant</h1>
        <p>Ask questions about your company database in natural language</p>
      </header>

      <main className="main">
        {/* Stats Section */}
        {stats && (
          <div className="stats-grid">
            {stats.map((stat, idx) => (
              <div key={idx} className="stat-card">
                <div className="stat-value">{stat.count}</div>
                <div className="stat-label">{stat.table_name}</div>
              </div>
            ))}
          </div>
        )}

        {/* Query Form */}
        <form onSubmit={handleSubmit} className="query-form">
          <div className="input-group">
            <input
              type="text"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="Ask a question about your company data..."
              className="query-input"
              disabled={loading}
            />
            <button 
              type="submit" 
              className="submit-btn"
              disabled={loading || !question.trim()}
            >
              {loading ? '🔄 Thinking...' : '🚀 Ask'}
            </button>
          </div>
        </form>

        {/* Example Questions */}
        <div className="examples">
          <p className="examples-label">Try these examples:</p>
          <div className="examples-grid">
            {exampleQuestions.map((q, idx) => (
              <button
                key={idx}
                onClick={() => setQuestion(q)}
                className="example-btn"
                disabled={loading}
              >
                {q}
              </button>
            ))}
          </div>
        </div>

        {/* Error Display */}
        {error && (
          <div className="error-box">
            <strong>❌ Error:</strong> {error}
          </div>
        )}

        {/* Results Display */}
        {result && (
          <div className="results">
            <div className="result-section">
              <h3>💭 Your Question</h3>
              <p className="question-text">{result.question}</p>
            </div>

            <div className="result-section">
              <h3>📝 Generated SQL</h3>
              <pre className="sql-code">{result.sql}</pre>
            </div>

            <div className="result-section">
              <h3>💡 Answer</h3>
              <p className="answer-text">{result.answer}</p>
              <p className="row-count">({result.row_count} row{result.row_count !== 1 ? 's' : ''} returned)</p>
            </div>

            {result.results && result.results.length > 0 && (
              <div className="result-section">
                <h3>📊 Data</h3>
                <div className="table-container">
                  <table className="results-table">
                    <thead>
                      <tr>
                        {Object.keys(result.results[0]).map((key) => (
                          <th key={key}>{key}</th>
                        ))}
                      </tr>
                    </thead>
                    <tbody>
                      {result.results.map((row, idx) => (
                        <tr key={idx}>
                          {Object.values(row).map((value, vidx) => (
                            <td key={vidx}>{String(value)}</td>
                          ))}
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}
          </div>
        )}
      </main>

      <footer className="footer">
        <p>Powered by PostgreSQL + Ollama + FastAPI + React</p>
      </footer>
    </div>
  )
}

export default App
