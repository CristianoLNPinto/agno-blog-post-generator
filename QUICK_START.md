# Quick Start Guide

## Setup (5 minutes)

1. **Activate virtual environment**
```bash
source .venv/bin/activate
```

2. **Set your API key**
```bash
# Edit .env file
GOOGLE_API_KEY=your_actual_api_key_here
```

3. **Install dependencies**
```bash
# Sync all dependencies (recommended)
make sync

# Or install manually
uv pip install agno==2.1.0
uv pip install -e ".[dev]"
```

## Usage

### Option 1: CLI (Command Line)
```bash
python -m src.agno.cli
```

### Option 2: API Server
```bash
# Start server
make run-api

# In another terminal, make a request
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{"topic": "The Future of AI"}'
```

### Option 3: Docker
```bash
make docker-build
make docker-run
```

## Common Commands

```bash
make help          # Show all available commands
make sync          # Sync all dependencies (agno framework + local package)
make run-cli       # Run CLI
make run-api       # Run API server
make stop-api      # Stop API server
make check-api     # Check if API is running
make test          # Run tests
make format        # Format code
make clean         # Clean temporary files
```

## Project Structure

```
src/agno/
├── domain/              # Core business logic
│   ├── agents/         # AI agents (research, scraper, writer)
│   └── models/         # Data models
├── application/        # Services (blog generation)
└── infrastructure/     # API, DB, LLM providers
```

## API Endpoints

- `GET /health` - Health check
- `POST /generate` - Generate blog post

## Documentation

- Full API docs: http://localhost:8000/docs (when server is running)
- Migration guide: [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md)
- Main README: [README.md](README.md)
