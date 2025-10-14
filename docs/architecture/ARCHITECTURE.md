# Architecture Documentation

## Overview

The Agno Blog Generator follows **Domain-Driven Design (DDD)** principles with a clean architecture pattern. This ensures separation of concerns, testability, and maintainability.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     Presentation Layer                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Streamlit UI │  │  FastAPI     │  │     CLI      │      │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘      │
└─────────┼──────────────────┼──────────────────┼─────────────┘
          │                  │                  │
          └──────────────────┼──────────────────┘
                             │
┌────────────────────────────┼─────────────────────────────────┐
│                     Application Layer                         │
│                  ┌─────────┴──────────┐                      │
│                  │ BlogGenerationService│                     │
│                  │  - generate_blog_post│                     │
│                  │  - Cache Management  │                     │
│                  └─────────┬──────────┘                      │
└────────────────────────────┼─────────────────────────────────┘
                             │
┌────────────────────────────┼─────────────────────────────────┐
│                       Domain Layer                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │Research Agent│  │Scraper Agent │  │ Writer Agent │      │
│  │              │  │              │  │              │      │
│  │ - search()   │  │ - scrape()   │  │ - write()    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Models     │  │   Prompts    │  │    Tools     │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└───────────────────────────────────────────────────────────────┘
                             │
┌────────────────────────────┼─────────────────────────────────┐
│                   Infrastructure Layer                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  LLM Provider│  │   Database   │  │Observability │      │
│  │   (Gemini)   │  │   (SQLite)   │  │ (Comet/Opik) │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└───────────────────────────────────────────────────────────────┘
```

## Layer Responsibilities

### 1. Presentation Layer

**Purpose**: Handle user interactions and present information

**Components**:
- **Streamlit UI** (`streamlit_app.py`): Web interface with real-time progress tracking
- **FastAPI** (`infrastructure/api/`): RESTful API with OpenAPI documentation
- **CLI** (`cli.py`): Command-line interface for quick generation

**Responsibilities**:
- Accept user input
- Display results
- Handle user interactions
- Format output

### 2. Application Layer

**Purpose**: Orchestrate business logic and use cases

**Components**:
- **BlogGenerationService** (`application/blog_generation_service/`):
  - Orchestrates the blog generation workflow
  - Manages caching at all levels
  - Coordinates between agents
  - Handles observability tracking

**Responsibilities**:
- Implement use cases
- Coordinate domain objects
- Manage transactions
- Handle caching logic

### 3. Domain Layer

**Purpose**: Core business logic and rules

**Components**:

#### Agents (`domain/agents/`)
- **ResearchAgent**: Searches for relevant articles
- **ScraperAgent**: Extracts content from URLs
- **WriterAgent**: Generates blog posts

#### Models (`domain/models/`)
- **BlogPost**: Blog post data structure
- **SearchResult**: Search result data
- **ArticleContent**: Scraped article data

#### Prompts (`domain/prompts/`)
- Agent-specific prompt templates
- Structured prompt engineering

#### Tools (`domain/tools/`)
- Custom tools for agents
- Utility functions

**Responsibilities**:
- Define business entities
- Implement business rules
- Maintain domain invariants
- Pure business logic (no infrastructure dependencies)

### 4. Infrastructure Layer

**Purpose**: External integrations and technical concerns

**Components**:

#### LLM Providers (`infrastructure/llm_providers/`)
- **Gemini**: Google Gemini API integration
- Configuration and client management

#### Database (`infrastructure/db/`)
- **SQLite**: Workflow state persistence
- Cache storage

#### Observability (`infrastructure/observability/`)
- **CometTracker**: Experiment tracking with Comet ML
- **OpikTracer**: LLM call tracing with Opik

**Responsibilities**:
- External API integrations
- Database operations
- File system operations
- Logging and monitoring

## Design Patterns

### 1. Dependency Injection

Dependencies are injected rather than created within classes:

```python
class BlogGenerationService:
    def __init__(self, comet_tracker: Optional[CometTracker] = None):
        self.comet_tracker = comet_tracker or CometTracker()
```

### 2. Repository Pattern

Database access is abstracted through repositories:

```python
def get_workflow_db() -> SqlWorkflowDb:
    """Get workflow database instance."""
    return SqlWorkflowDb(db_file=str(settings.db_path))
```

### 3. Agent Pattern

Specialized agents handle specific tasks:

```python
research_agent = Agent(
    name="Research Agent",
    instructions="Search for relevant articles...",
    model=get_gemini_model(),
)
```

### 4. Caching Strategy

Multi-level caching for performance:

```python
# Search cache
search_cache = SearchCache(cache_dir=settings.cache_dir)

# Scrape cache
scrape_cache = ScrapeCache(cache_dir=settings.cache_dir)

# Blog cache
blog_cache = BlogCache(cache_dir=settings.cache_dir)
```

## Data Flow

### Blog Generation Flow

```
1. User Request
   ↓
2. BlogGenerationService.generate_blog_post()
   ↓
3. Check Blog Cache
   ├─ Hit → Return cached blog
   └─ Miss → Continue
   ↓
4. Research Phase
   ├─ Check Search Cache
   ├─ Research Agent searches
   └─ Cache results
   ↓
5. Extraction Phase
   ├─ Check Scrape Cache
   ├─ Scraper Agent extracts
   └─ Cache results
   ↓
6. Writing Phase
   ├─ Writer Agent generates
   └─ Cache blog post
   ↓
7. Return Result
```

## Configuration Management

Configuration is centralized in `config.py` using Pydantic Settings:

```python
class Settings(BaseSettings):
    # API Keys
    google_api_key: str
    
    # Observability
    comet_api_key: Optional[str] = None
    opik_api_key: Optional[str] = None
    
    # Paths
    cache_dir: Path
    db_path: Path
    
    class Config:
        env_file = ".env"
```

## Error Handling

Errors are handled at appropriate layers:

1. **Domain Layer**: Business rule violations
2. **Application Layer**: Use case failures
3. **Infrastructure Layer**: External service failures
4. **Presentation Layer**: User-friendly error messages

## Testing Strategy

### Unit Tests
- Test domain logic in isolation
- Mock external dependencies
- Fast execution

### Integration Tests
- Test component interactions
- Use test databases
- Verify workflows

### End-to-End Tests
- Test complete user flows
- Use real dependencies (in test mode)
- Verify system behavior

## Scalability Considerations

### Current Architecture
- Single-process application
- Local SQLite database
- File-based caching

### Future Enhancements
- **Horizontal Scaling**: Add load balancer and multiple instances
- **Database**: Migrate to PostgreSQL for production
- **Caching**: Use Redis for distributed caching
- **Queue System**: Add Celery for async processing
- **API Gateway**: Add rate limiting and authentication

## Security Considerations

### Current Implementation
- API keys stored in environment variables
- No authentication on API endpoints
- CORS enabled for all origins

### Production Recommendations
1. Implement API key authentication
2. Add rate limiting
3. Restrict CORS origins
4. Use HTTPS
5. Implement request validation
6. Add audit logging

## Observability

### Metrics Tracked
- **Performance**: Response times, cache hit rates
- **Quality**: Success rates, error rates
- **Usage**: Request counts, topic distribution

### Tools
- **Comet ML**: Experiment tracking and metrics
- **Opik**: LLM call tracing and debugging

## Dependencies

### Core Dependencies
- **agno**: Agent framework
- **fastapi**: Web framework
- **streamlit**: UI framework
- **pydantic**: Data validation
- **sqlalchemy**: Database ORM

### LLM Dependencies
- **google-generativeai**: Gemini API

### Observability Dependencies
- **comet-ml**: Experiment tracking
- **opik**: LLM tracing

## Directory Structure

```
src/agno_blog/
├── domain/              # Core business logic
│   ├── agents/         # AI agent definitions
│   ├── models/         # Pydantic data models
│   ├── prompts/        # Prompt templates
│   └── tools/          # Custom tools
├── application/        # Use cases & services
│   └── blog_generation_service/
│       ├── service.py  # Main service
│       └── cache.py    # Caching logic
├── infrastructure/     # External interfaces
│   ├── api/           # FastAPI endpoints
│   ├── db/            # Database connections
│   ├── llm_providers/ # LLM configurations
│   └── observability/ # Tracking systems
├── config.py          # Configuration
└── cli.py             # CLI entry point
```

## Best Practices

1. **Separation of Concerns**: Each layer has clear responsibilities
2. **Dependency Direction**: Dependencies point inward (toward domain)
3. **Testability**: Easy to test with mocked dependencies
4. **Maintainability**: Clear structure and organization
5. **Extensibility**: Easy to add new features or agents
6. **Documentation**: Comprehensive inline and external docs

## References

- [Domain-Driven Design](https://martinfowler.com/bliki/DomainDrivenDesign.html)
- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Agno Framework](https://github.com/agno-ai/agno)
