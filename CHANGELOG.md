# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2025-10-02

### Added
- **DDD Architecture**: Restructured project following Domain-Driven Design principles
  - Domain layer: Core business logic (agents, models, prompts, tools)
  - Application layer: Use cases and services (blog generation service)
  - Infrastructure layer: External interfaces (API, DB, LLM providers)
- **FastAPI REST API**: Production-ready API with endpoints:
  - `GET /` - Root endpoint
  - `GET /health` - Health check
  - `POST /generate` - Blog post generation
  - `GET /docs` - Swagger UI documentation
  - `GET /redoc` - ReDoc documentation
- **Docker Support**: Dockerfile and docker-compose.yaml for containerization
- **Makefile Commands**: Common development tasks with uv package manager
  - `make sync` - Sync all dependencies
  - `make run-api` - Run FastAPI server
  - `make stop-api` - Stop API server
  - `make check-api` - Check API status
  - `make run-cli` - Run CLI
  - `make test` - Run tests
  - `make format` - Format code
  - `make lint` - Run linters
  - `make clean` - Clean temporary files
- **Configuration Management**: Centralized config with pydantic-settings
- **Test Structure**: pytest-based test suite
- **Documentation**:
  - README.md - Comprehensive project documentation
  - MIGRATION_GUIDE.md - Detailed migration from monolithic to DDD
  - QUICK_START.md - Quick reference guide
  - CHANGELOG.md - This file
- **Example Notebook**: Jupyter notebook demonstrating programmatic usage

### Changed
- **Package Name**: Renamed from `agno` to `agno-blog` to avoid conflict with agno framework
- **Model**: Migrated from OpenAI to Google Gemini API
- **Package Manager**: Using `uv` for faster dependency management
- **Project Structure**: Moved from single file to modular architecture

### Fixed
- **Import Conflicts**: Resolved naming conflict between local package and agno framework
- **Environment Variables**: Proper .env loading with python-dotenv
- **Caching**: Improved caching mechanism for search results and scraped articles

### Technical Details
- Python 3.12+
- FastAPI 0.118.0+
- Uvicorn with auto-reload
- Google Gemini API (gemini-2.0-flash-exp)
- SQLite for workflow state management
- Pydantic v2 for data validation
- Type hints throughout codebase

### Migration Notes
- Original `blog_post_generator.py` preserved for reference
- All functionality maintained while improving architecture
- API provides new integration possibilities
- Docker support for easy deployment

## [0.1.0] - Initial Version
- Single-file blog post generator
- OpenAI GPT integration
- Basic caching mechanism
