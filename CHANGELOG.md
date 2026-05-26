# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-05-26

### Added
- Initial release of Ask My PostgreSQL Database
- Natural language to SQL conversion using Ollama
- React frontend with beautiful UI
- FastAPI backend with RESTful API
- PostgreSQL integration with pgvector support
- Query history logging
- Database statistics dashboard
- Example questions for quick testing
- Safe query execution (SELECT only)
- CORS protection
- Environment-based configuration
- Comprehensive documentation
- Docker support
- Deployment guides

### Features
- **AI-Powered**: Uses local LLM (Ollama) for natural language understanding
- **Privacy First**: 100% local processing, no external API calls
- **Fast**: Optimized PostgreSQL queries with caching
- **Secure**: Read-only queries, SQL injection protection
- **Beautiful UI**: Modern, responsive React interface
- **Extensible**: Easy to customize and extend

### Supported Models
- Llama 3.2 (default)
- Mistral
- Gemma
- Qwen
- Any Ollama-compatible model

### Database Features
- PostgreSQL 13+
- pgvector for semantic search
- Connection pooling
- SSH tunnel support
- Cloud database support (GCP, AWS, Azure)

## [Unreleased]

### Planned Features
- Authentication and user management
- Query result caching
- Export to CSV/Excel
- Data visualization charts
- Multi-database support
- Query templates
- Scheduled queries
- Email notifications
- API documentation (Swagger/OpenAPI)
- Mobile app

### Under Consideration
- Support for other databases (MySQL, MongoDB)
- Graph visualizations
- AI-powered data insights
- Natural language report generation
- Integration with BI tools
- Real-time collaboration

---

## Version History

### Version 1.0.0 (2026-05-26)
- First stable release
- Production-ready
- Full documentation
- Docker support

---

**Note:** For detailed changes, see the [commit history](https://github.com/kjosh2008/ask-my-postgres-database/commits/main).
