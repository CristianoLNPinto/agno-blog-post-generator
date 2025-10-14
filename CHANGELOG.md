# Changelog

All notable changes to this project will be documented in this file.

## [2.1.0] - 2025-10-14

### Added
- **Smart Model Factory**: Intelligent LLM provider selection based on agent requirements
  - `get_model(use_tools=bool)` - Automatically selects Gemini for tool-based agents, respects LLM_PROVIDER for others
  - Handles Groq's limitation (JSON mode + tools incompatibility) transparently
  - Single source of truth for provider selection logic
- **Groq LLM Provider Support**: Added Groq as an alternative LLM provider for ultra-fast inference
  - New `groq_provider.py` module in `infrastructure/llm_providers/`
  - Support for multiple Groq models (qwen/qwen3-32b, llama-3.3-70b-versatile, etc.)
  - Streaming and async support
- **Hybrid Provider Architecture**: Optimized provider usage per agent
  - Research Agent: Uses Gemini (needs tools + structured output)
  - Scraper Agent: Uses Gemini (needs tools + structured output)
  - Writer Agent: Uses Groq (ultra-fast generation, no tools needed)
- **Configuration Updates**: Enhanced configuration system for multi-provider support
  - `LLM_PROVIDER` setting to choose between "gemini" and "groq"
  - `GROQ_API_KEY` and `GROQ_MODEL_ID` environment variables
  - Updated `.env.example` with Groq configuration
- **Documentation**:
  - `GROQ_QUICK_START.md` - 5-minute quick start guide
  - `SMART_MODEL_FACTORY.md` - Smart factory pattern documentation
  - `docs/guides/GROQ_LIMITATIONS.md` - Groq tool use limitations and workarounds
- **Examples and Tests**:
  - `examples/groq_example.py` - Runnable examples (sync, streaming, async)
  - `tests/test_groq_provider.py` - Unit and integration tests
  - `tests/test_model_factory.py` - Model factory tests with tool selection logic
- **Dependency**: Added `groq>=0.9.0` to project dependencies

### Changed
- **Model Factory**: Enhanced with smart provider selection based on tool requirements
- **All Agents**: Updated to use smart model factory instead of hardcoded providers
- **README.md**: Updated to mention hybrid provider approach
- **Documentation Index**: Streamlined Groq documentation
- **pyproject.toml**: Added Groq SDK dependency

## [2.0.0] - 2025-10-14

### Added
- **Comprehensive Swagger/OpenAPI Documentation**: Enhanced FastAPI with detailed API documentation
  - Rich endpoint descriptions with examples
  - Request/response model documentation with validation
  - Interactive Swagger UI at `/docs`
  - ReDoc documentation at `/redoc`
  - OpenAPI tags for endpoint organization
- **Structured Documentation**: New `/docs` directory with organized documentation
  - `docs/api/API_REFERENCE.md` - Complete REST API reference
  - `docs/architecture/ARCHITECTURE.md` - System architecture and design patterns
  - `docs/guides/GETTING_STARTED.md` - Comprehensive getting started guide
  - `docs/guides/OBSERVABILITY.md` - Observability setup and best practices
  - `docs/guides/DEVELOPMENT.md` - Development workflow and guidelines
  - `docs/README.md` - Documentation index and navigation
- **Enhanced API Models**: Improved Pydantic models with examples and detailed descriptions
- **Badges**: Added Python, License, and FastAPI version badges to README

### Changed
- **README.md**: Completely restructured with cleaner organization
  - Added badges and better formatting
  - Simplified quick start section
  - Added links to comprehensive documentation
  - Improved navigation and structure
- **Project Structure**: Cleaned up root directory
  - Removed redundant documentation files
  - Consolidated observability docs
  - Removed internal implementation notes
  - Removed legacy test files from root

### Removed
- **Redundant Documentation Files**:
  - `COMET_ML_SETUP.md` (consolidated into docs/guides/OBSERVABILITY.md)
  - `COMET_QUICK_REFERENCE.md` (consolidated)
  - `IMPLEMENTATION_SUMMARY.md` (internal notes)
  - `MIGRATION_GUIDE.md` (outdated)
  - `OBSERVABILITY.md` (moved to docs/guides/)
  - `OPIK_BUGFIX.md` (internal notes)
  - `OPIK_FINAL_IMPLEMENTATION.md` (internal notes)
  - `OPIK_IMPLEMENTATION_SUMMARY.md` (internal notes)
  - `OPIK_QUICK_REFERENCE.md` (consolidated)
  - `OPIK_SETUP.md` (consolidated)
  - `STREAMLIT_GUIDE.md` (consolidated into getting started)
- **Legacy Files**:
  - `blog_post_generator.py` (replaced by modular architecture)
  - `setup_comet_env.sh` (replaced with better documentation)
  - `test_comet_integration.py` (moved to tests/)
  - `test_opik_integration_fixed.py` (moved to tests/)
  - `tmp/` directory (temporary files)

### Improved
- **API Documentation**: Now production-ready with comprehensive Swagger docs
- **Developer Experience**: Clear documentation structure and navigation
- **Project Organization**: Cleaner root directory with better file organization
- **Documentation Quality**: Professional, comprehensive, and well-structured docs

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
