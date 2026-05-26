# Contributing to Ask My PostgreSQL Database

First off, thank you for considering contributing! 🎉

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues. When creating a bug report, include:

- **Clear description** of the issue
- **Steps to reproduce** the behavior
- **Expected behavior**
- **Screenshots** if applicable
- **Environment details** (OS, Python version, Node version)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- **Clear description** of the enhancement
- **Use case** - why would this be useful?
- **Possible implementation** (if you have ideas)

### Pull Requests

1. Fork the repo and create your branch from `main`
2. If you've added code, add tests
3. Ensure the test suite passes
4. Make sure your code follows the existing style
5. Write a clear commit message

## Development Setup

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Coding Standards

### Python (Backend)

- Follow PEP 8 style guide
- Use type hints where appropriate
- Add docstrings for functions
- Keep functions focused and small

### JavaScript/React (Frontend)

- Use functional components with hooks
- Follow React best practices
- Use meaningful variable names
- Add comments for complex logic

## Testing

### Backend Tests

```bash
cd backend
pytest
```

### Frontend Tests

```bash
cd frontend
npm test
```

## Documentation

- Update README.md if you change functionality
- Add comments for complex code
- Update API documentation if you add endpoints

## Questions?

Feel free to open an issue with your question!

Thank you! ❤️
