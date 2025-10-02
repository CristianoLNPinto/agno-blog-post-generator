# Migration Guide: Monolithic to DDD Architecture

This document explains the restructuring of the blog post generator from a single-file script to a Domain-Driven Design (DDD) architecture following the [agent-api-cookiecutter](https://github.com/neural-maze/agent-api-cookiecutter) template.

## What Changed

### Before (Monolithic)
```
agno/
├── blog_post_generator.py  # Everything in one file
├── .env
└── tmp/
```

### After (DDD Architecture)
```
agno/
├── src/agno/
│   ├── domain/              # Business logic
│   │   ├── agents/         # Agent definitions
│   │   ├── models/         # Data models
│   │   ├── prompts/        # Prompt templates
│   │   └── tools/          # Custom tools
│   ├── application/        # Use cases
│   │   └── blog_generation_service/
│   ├── infrastructure/     # External interfaces
│   │   ├── api/           # FastAPI endpoints
│   │   ├── db/            # Database
│   │   └── llm_providers/ # LLM configs
│   └── config.py          # Configuration
├── tests/                  # Test suite
├── notebooks/              # Jupyter notebooks
├── data/                   # Data storage
├── static/                 # Static assets
├── Dockerfile
├── docker-compose.yaml
├── Makefile
└── pyproject.toml
```

## Key Benefits

### 1. **Separation of Concerns**
- **Domain Layer**: Pure business logic (agents, models)
- **Application Layer**: Orchestration (services, workflows)
- **Infrastructure Layer**: External dependencies (API, DB, LLM)

### 2. **Testability**
- Each layer can be tested independently
- Mock external dependencies easily
- Unit tests for business logic

### 3. **Maintainability**
- Clear structure makes code easier to navigate
- Changes in one layer don't affect others
- Easy to add new features

### 4. **Scalability**
- FastAPI for production-ready REST API
- Docker support for containerization
- Easy to add new agents or services

## Migration Steps Completed

### 1. ✅ Domain Layer
- Moved agent definitions to `domain/agents/`
- Extracted Pydantic models to `domain/models/`
- Created exception classes in `domain/exceptions.py`

### 2. ✅ Application Layer
- Created `BlogGenerationService` in `application/blog_generation_service/`
- Separated caching logic to `cache.py`
- Workflow orchestration in service methods

### 3. ✅ Infrastructure Layer
- FastAPI endpoints in `infrastructure/api/`
- Database configuration in `infrastructure/db/`
- LLM provider setup in `infrastructure/llm_providers/`

### 4. ✅ Configuration Management
- Centralized config in `config.py`
- Environment variables via `.env`
- Pydantic settings for type safety

### 5. ✅ Development Tools
- `Makefile` for common tasks
- `Dockerfile` and `docker-compose.yaml`
- `pyproject.toml` for dependencies
- Test structure in `tests/`

## How to Use

### CLI Mode (Same as before)
```bash
python -m src.agno.cli
```

### API Mode (New!)
```bash
# Start the API server
make run-api

# Or manually
uvicorn src.agno.infrastructure.api.main:app --reload
```

### Docker Mode (New!)
```bash
make docker-build
make docker-run
```

### Programmatic Usage
```python
from agno.application.blog_generation_service import BlogGenerationService
from agno.workflow.workflow import Workflow
from agno.infrastructure.db import get_workflow_db

service = BlogGenerationService()

async def execution(session_state, topic: str = None, **kwargs):
    return await service.generate_blog_post(session_state, topic, **kwargs)

workflow = Workflow(
    name="Blog Generator",
    db=get_workflow_db(),
    steps=execution,
    session_state={},
)

response = await workflow.arun(topic="Your Topic")
```

## API Endpoints

### Health Check
```bash
GET http://localhost:8000/health
```

### Generate Blog Post
```bash
POST http://localhost:8000/generate
Content-Type: application/json

{
  "topic": "The Future of AI",
  "use_search_cache": true,
  "use_scrape_cache": true,
  "use_blog_cache": true
}
```

## Configuration

All configuration is managed through `src/agno/config.py` and `.env`:

```bash
# .env
GOOGLE_API_KEY=your_api_key_here
```

Additional settings can be modified in `config.py`:
- Model ID
- Database file path
- Cache settings
- Search parameters

## Testing

```bash
# Run all tests
make test

# Run specific test
pytest tests/test_blog_generator.py -v
```

## Code Quality

```bash
# Format code
make format

# Run linters
make lint

# Clean temporary files
make clean
```

## What Stayed the Same

- ✅ Core functionality (research → scrape → write)
- ✅ Gemini API integration
- ✅ Caching mechanism
- ✅ Agent definitions and prompts
- ✅ Output quality

## What's New

- ✅ REST API with FastAPI
- ✅ Docker support
- ✅ Proper project structure
- ✅ Test framework
- ✅ Development tools (Makefile)
- ✅ Configuration management
- ✅ Better error handling
- ✅ Type hints throughout

## Next Steps

1. **Add More Tests**: Expand test coverage
2. **Add Authentication**: Secure the API endpoints
3. **Add Monitoring**: Implement logging and metrics
4. **Add Rate Limiting**: Prevent API abuse
5. **Add Documentation**: Auto-generate API docs
6. **Add CI/CD**: Automated testing and deployment

## Troubleshooting

### Import Errors
Make sure you're running from the project root and the virtual environment is activated:
```bash
source .venv/bin/activate
python -m src.agno.cli
```

### API Not Starting
Check that port 8000 is available:
```bash
lsof -i :8000
```

### Database Issues
Delete the database file and let it recreate:
```bash
rm -rf tmp/blog_generator.db
```

## Original File

The original monolithic file is still available at `blog_post_generator.py` for reference, but it's recommended to use the new structure going forward.
