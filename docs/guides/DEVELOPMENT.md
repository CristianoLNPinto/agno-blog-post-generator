# Development Guide

## Development Setup

### Prerequisites

- Python 3.12+
- Git
- Make (optional, but recommended)

### Initial Setup

1. **Clone and setup**:
   ```bash
   git clone https://github.com/CristianoLNPinto/agno-blog-post-generator.git
   cd agno-blog-post-generator
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. **Install development dependencies**:
   ```bash
   make dev-install
   # Or manually:
   pip install -e ".[dev]"
   ```

3. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

## Project Structure

```
agno-blog-post-generator/
├── src/agno_blog/           # Source code
│   ├── domain/              # Core business logic
│   │   ├── agents/         # AI agents
│   │   ├── models/         # Data models
│   │   ├── prompts/        # Prompt templates
│   │   └── tools/          # Custom tools
│   ├── application/        # Use cases
│   │   └── blog_generation_service/
│   ├── infrastructure/     # External integrations
│   │   ├── api/           # FastAPI
│   │   ├── db/            # Database
│   │   ├── llm_providers/ # LLM clients
│   │   └── observability/ # Tracking
│   ├── config.py          # Configuration
│   └── cli.py             # CLI interface
├── tests/                  # Test suite
├── docs/                   # Documentation
├── data/                   # Data storage
├── notebooks/              # Jupyter notebooks
├── .env.example           # Environment template
├── pyproject.toml         # Project metadata
├── Makefile               # Development commands
└── README.md              # Main documentation
```

## Development Workflow

### 1. Create a Feature Branch

```bash
# Create and switch to a new branch
git checkout -b feature/your-feature-name
```

### 2. Make Changes

Edit the code following the project structure and conventions.

### 3. Run Tests

```bash
# Run all tests
make test

# Run specific test file
pytest tests/test_blog_generator.py

# Run with coverage
pytest --cov=src/agno_blog tests/
```

### 4. Format Code

```bash
# Format with black
make format

# Or manually
black src/ tests/
```

### 5. Lint Code

```bash
# Run all linters
make lint

# Or manually
ruff check src/ tests/
mypy src/
```

### 6. Commit Changes

```bash
git add .
git commit -m "feat: add new feature"
```

### 7. Push and Create PR

```bash
git push origin feature/your-feature-name
# Create pull request on GitHub
```

## Coding Standards

### Python Style

- **PEP 8**: Follow Python style guide
- **Line Length**: Max 100 characters
- **Imports**: Organized (stdlib, third-party, local)
- **Type Hints**: Use type hints where appropriate

### Naming Conventions

- **Classes**: `PascalCase` (e.g., `BlogGenerationService`)
- **Functions**: `snake_case` (e.g., `generate_blog_post`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `MAX_RETRIES`)
- **Private**: Prefix with `_` (e.g., `_internal_method`)

### Documentation

- **Docstrings**: Use Google style docstrings
- **Comments**: Explain why, not what
- **Type Hints**: Document parameter and return types

Example:

```python
def generate_blog_post(
    topic: str,
    use_cache: bool = True
) -> BlogPost:
    """Generate a blog post on the given topic.
    
    Args:
        topic: The topic for the blog post
        use_cache: Whether to use cached results
        
    Returns:
        Generated blog post with metadata
        
    Raises:
        ValueError: If topic is empty
        GenerationError: If generation fails
    """
    pass
```

## Testing

### Test Structure

```
tests/
├── __init__.py
├── conftest.py              # Pytest fixtures
├── test_blog_generator.py   # Main tests
└── integration/             # Integration tests
```

### Writing Tests

```python
import pytest
from src.agno_blog.application.blog_generation_service import BlogGenerationService

def test_blog_generation():
    """Test basic blog generation."""
    service = BlogGenerationService()
    result = service.generate_blog_post(
        topic="Test Topic",
        use_cache=False
    )
    assert result is not None
    assert len(result.content) > 0

@pytest.mark.asyncio
async def test_async_generation():
    """Test async blog generation."""
    service = BlogGenerationService()
    result = await service.generate_blog_post_async(
        topic="Test Topic"
    )
    assert result is not None
```

### Running Tests

```bash
# All tests
pytest

# Specific test
pytest tests/test_blog_generator.py::test_blog_generation

# With coverage
pytest --cov=src/agno_blog --cov-report=html

# Verbose output
pytest -v

# Stop on first failure
pytest -x
```

### Test Coverage

Aim for:
- **Overall**: > 80%
- **Domain Layer**: > 90%
- **Application Layer**: > 85%
- **Infrastructure Layer**: > 70%

## Debugging

### Using Debugger

```python
# Add breakpoint
import pdb; pdb.set_trace()

# Or use built-in breakpoint()
breakpoint()
```

### Logging

```python
import logging

logger = logging.getLogger(__name__)

logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
```

### Debugging with Observability

1. Enable Comet ML and Opik
2. Run your code
3. View traces and metrics
4. Identify issues

## Common Tasks

### Adding a New Agent

1. Create agent file in `src/agno_blog/domain/agents/`
2. Define agent with instructions and tools
3. Add tests in `tests/`
4. Update documentation

Example:

```python
from agno import Agent
from ..llm_providers import get_gemini_model

summary_agent = Agent(
    name="Summary Agent",
    instructions="Summarize the given text...",
    model=get_gemini_model(),
)
```

### Adding a New Endpoint

1. Add endpoint in `src/agno_blog/infrastructure/api/main.py`
2. Define request/response models in `models.py`
3. Add tests
4. Update API documentation

Example:

```python
@app.post("/summarize", response_model=SummaryResponse)
async def summarize_text(request: SummaryRequest):
    """Summarize the given text."""
    # Implementation
    pass
```

### Adding Configuration

1. Add field to `Settings` in `config.py`
2. Add to `.env.example`
3. Update documentation

Example:

```python
class Settings(BaseSettings):
    new_setting: str = Field(
        default="default_value",
        description="Description of setting"
    )
```

### Modifying Prompts

1. Edit prompts in `src/agno_blog/domain/prompts/`
2. Test with different inputs
3. Monitor quality with observability
4. Document changes

## Performance Optimization

### Profiling

```bash
# Profile with cProfile
python -m cProfile -o output.prof script.py

# Analyze with snakeviz
pip install snakeviz
snakeviz output.prof
```

### Caching

- Use search, scrape, and blog caches
- Monitor cache hit rates
- Clear cache when needed

### Async Operations

- Use async/await for I/O operations
- Batch API calls when possible
- Use connection pooling

## Database Migrations

Currently using SQLite with no migrations. For future:

1. Add Alembic for migrations
2. Create migration scripts
3. Test migrations thoroughly

## Docker Development

### Build Image

```bash
docker build -t agno-blog .
```

### Run Container

```bash
docker run -p 8000:8000 --env-file .env agno-blog
```

### Docker Compose

```bash
# Start services
docker-compose up

# Stop services
docker-compose down

# Rebuild
docker-compose up --build
```

## CI/CD

### GitHub Actions (Future)

```yaml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.12'
      - run: pip install -e ".[dev]"
      - run: pytest
      - run: ruff check .
      - run: black --check .
```

## Makefile Commands

```bash
# Installation
make install          # Install package
make dev-install      # Install with dev dependencies

# Running
make run-streamlit    # Run Streamlit UI
make run-api          # Run FastAPI server
make run-cli          # Run CLI

# Testing
make test             # Run tests
make test-cov         # Run tests with coverage

# Code Quality
make format           # Format code
make lint             # Run linters
make type-check       # Run type checker

# Cleanup
make clean            # Clean cache and temp files
make clean-all        # Clean everything including venv

# Docker
make docker-build     # Build Docker image
make docker-run       # Run Docker container

# Help
make help             # Show all commands
```

## Troubleshooting

### Import Errors

```bash
# Reinstall in editable mode
pip install -e .
```

### Test Failures

```bash
# Run with verbose output
pytest -v

# Run specific test
pytest tests/test_file.py::test_function -v
```

### Linting Errors

```bash
# Auto-fix with ruff
ruff check --fix .

# Format with black
black .
```

## Best Practices

1. **Write Tests First**: TDD approach
2. **Small Commits**: Commit often with clear messages
3. **Code Review**: Always get code reviewed
4. **Documentation**: Update docs with code changes
5. **Type Hints**: Use type hints for better IDE support
6. **Error Handling**: Handle errors gracefully
7. **Logging**: Add appropriate logging
8. **Performance**: Profile before optimizing

## Git Workflow

Following GitFlow:

1. **Main Branch**: Production-ready code
2. **Develop Branch**: Integration branch
3. **Feature Branches**: `feature/name`
4. **Release Branches**: `release/version`
5. **Hotfix Branches**: `hotfix/name`

See `.windsurf/rules/gitflow-rules.md` for details.

## Resources

- **Python Docs**: https://docs.python.org/3/
- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **Streamlit Docs**: https://docs.streamlit.io/
- **Agno Docs**: https://github.com/agno-ai/agno
- **Pytest Docs**: https://docs.pytest.org/

## Getting Help

- Check documentation in `/docs`
- Search GitHub issues
- Ask in discussions
- Review code examples

---

Happy coding! 🚀
