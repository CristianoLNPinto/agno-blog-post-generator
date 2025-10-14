# 🎨 Agno - AI Blog Post Generator

An advanced AI-powered blog post generator that combines web research, content extraction, and professional writing using multiple LLM providers (Google Gemini, Groq).

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.119+-green.svg)](https://fastapi.tiangolo.com/)

## ✨ Features

- 🔍 **Intelligent Web Research**: Automatically finds and evaluates high-quality sources
- 📄 **Content Extraction**: Scrapes and processes articles with smart formatting
- ✍️ **Professional Writing**: Generates engaging, SEO-optimized blog posts
- 🤖 **Multiple LLM Providers**: Support for Google Gemini and Groq (ultra-fast inference)
- ⚡ **Multi-Level Caching**: Efficient caching at search, scrape, and blog levels
- 🎨 **Streamlit UI**: Beautiful web interface with real-time progress tracking
- 🚀 **REST API**: FastAPI with comprehensive Swagger/OpenAPI documentation
- 💻 **CLI Interface**: Command-line tool for quick blog generation
- 🐳 **Docker Support**: Containerized deployment ready
- 📊 **Observability**: Full experiment tracking with Comet ML and Opik integration

## 🏗️ Architecture

This project follows **Domain-Driven Design (DDD)** principles with a clean architecture:

```
src/agno_blog/
├── domain/              # Core business logic
│   ├── agents/         # AI agent definitions
│   ├── models/         # Pydantic data models
│   ├── prompts/        # Prompt templates
│   └── tools/          # Custom tools
├── application/        # Use cases & services
│   └── blog_generation_service/
├── infrastructure/     # External interfaces
│   ├── api/           # FastAPI endpoints
│   ├── db/            # Database connections
│   ├── llm_providers/ # LLM configurations
│   └── observability/ # Comet ML tracking
└── config.py          # Configuration management
```

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- LLM Provider API key:
  - **Google Gemini** ([Get one here](https://makersuite.google.com/app/apikey)), or
  - **Groq** ([Get one here](https://console.groq.com/keys)) - Ultra-fast inference

### Installation

```bash
# Clone the repository
git clone https://github.com/CristianoLNPinto/agno-blog-post-generator.git
cd agno-blog-post-generator

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -e .

# Configure environment
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY
```

**📖 For detailed setup instructions, see [Getting Started Guide](docs/guides/GETTING_STARTED.md)**

### Usage

#### Streamlit UI Mode (Recommended)

Launch the beautiful web interface with real-time progress tracking:

```bash
make run-streamlit
# or
streamlit run streamlit_app.py
```

Then open your browser to http://localhost:8501

**Features:**
- 🎨 Beautiful, modern interface
- 📊 Real-time progress tracking for each phase
- 📄 View output in HTML or Markdown
- 💾 Download blog posts in multiple formats
- 💡 Example topics for quick testing
- ⚙️ Configurable cache settings

#### CLI Mode

Generate a blog post from the command line:

```bash
make run-cli
# or
python -m src.agno_blog.cli
```

#### API Mode

Start the FastAPI server with comprehensive Swagger documentation:

```bash
uvicorn src.agno_blog.infrastructure.api.main:app --reload
```

**Access Documentation:**
- 📚 **Swagger UI**: http://localhost:8000/docs
- 📖 **ReDoc**: http://localhost:8000/redoc
- 🏥 **Health Check**: http://localhost:8000/health

**Example API request:**

```bash
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "The Future of AI in Healthcare",
    "use_search_cache": true
  }'
```

**📖 For complete API documentation, see [API Reference](docs/api/API_REFERENCE.md)**

#### Docker Mode

```bash
# Build and run with Docker Compose
make docker-build
make docker-run

# Or manually
docker-compose up
```

## 🛠️ Development

### Install development dependencies

```bash
make dev-install
```

### Run tests

```bash
make test
```

### Code formatting and linting

```bash
make format  # Format code
make lint    # Run linters
```

### Clean temporary files

```bash
make clean
```

## 📁 Project Structure

```
agno-blog-post-generator/
├── src/agno_blog/            # Source code
│   ├── domain/               # Core business logic
│   ├── application/          # Use cases & services
│   ├── infrastructure/       # External integrations
│   ├── config.py            # Configuration
│   └── cli.py               # CLI entry point
├── docs/                     # 📚 Documentation
│   ├── api/                 # API documentation
│   ├── guides/              # User & developer guides
│   └── architecture/        # Architecture docs
├── tests/                    # Test suite
├── data/                     # Data storage & cache
├── notebooks/                # Jupyter notebooks
├── .env.example             # Environment template
├── Dockerfile               # Docker configuration
├── docker-compose.yaml      # Docker Compose config
├── Makefile                 # Development commands
├── pyproject.toml           # Project metadata
└── README.md                # This file
```

## 🔧 Configuration

Configuration is managed through environment variables in `.env`:

```bash
# Google Gemini API Configuration
GOOGLE_API_KEY=your_api_key_here

# Comet ML Configuration (Optional - for experiment tracking)
COMET_API_KEY=your_comet_api_key
COMET_PROJECT_NAME=agno-blog-post-generator
COMET_WORKSPACE=your_workspace

# Opik Configuration (Optional - for LLM tracing)
OPIK_API_KEY=your_opik_api_key
OPIK_PROJECT_NAME=agno-blog-llm-tracing
OPIK_WORKSPACE=your_workspace
```

Additional settings can be configured in `src/agno_blog/config.py`.

## 📊 Observability

The project includes comprehensive observability with two complementary systems:

### Comet ML - Experiment Tracking
Track performance metrics, cache hit rates, and success rates across all phases.

### Opik - LLM Tracing
Trace every LLM call with complete prompt/response logging and token usage tracking.

**Setup:**
```bash
# Add to .env
COMET_API_KEY=your_api_key
COMET_PROJECT_NAME=agno-blog-post-generator
COMET_WORKSPACE=your_workspace

OPIK_API_KEY=your_api_key
OPIK_PROJECT_NAME=agno-blog-llm-tracing
OPIK_WORKSPACE=your_workspace
```

**📖 For complete observability guide, see [Observability Documentation](docs/guides/OBSERVABILITY.md)**

## 📚 How It Works

1. **Research Phase**: The research agent searches for relevant articles on the given topic
2. **Extraction Phase**: The scraper agent extracts full content from found articles
3. **Writing Phase**: The writer agent synthesizes information into a professional blog post
4. **Caching**: Results are cached at each stage for efficiency

## 📚 Documentation

Comprehensive documentation is available in the `/docs` directory:

- **[Getting Started Guide](docs/guides/GETTING_STARTED.md)** - Installation and first steps
- **[API Reference](docs/api/API_REFERENCE.md)** - Complete REST API documentation
- **[Architecture Overview](docs/architecture/ARCHITECTURE.md)** - System design and patterns
- **[Development Guide](docs/guides/DEVELOPMENT.md)** - Contributing and development workflow
- **[Observability Guide](docs/guides/OBSERVABILITY.md)** - Monitoring and tracking
- **[Groq Quick Start](GROQ_QUICK_START.md)** - Get started with Groq in 5 minutes
- **[Smart Model Factory](SMART_MODEL_FACTORY.md)** - How the hybrid provider system works

**Interactive API Documentation:**
- Swagger UI: http://localhost:8000/docs (when API is running)
- ReDoc: http://localhost:8000/redoc

## 🤝 Contributing

Contributions are welcome! Please see the [Development Guide](docs/guides/DEVELOPMENT.md) for:
- Development setup
- Coding standards
- Testing guidelines
- Pull request process

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Agno](https://github.com/agno-ai/agno) framework
- Powered by Google's Gemini API and Groq
- Observability by Comet ML and Opik
- Architecture inspired by Domain-Driven Design principles

## 📬 Support

- **Documentation**: [docs/](docs/)
- **Issues**: [GitHub Issues](https://github.com/CristianoLNPinto/agno-blog-post-generator/issues)
- **Discussions**: [GitHub Discussions](https://github.com/CristianoLNPinto/agno-blog-post-generator/discussions)

---

Made with ❤️ by Cristiano Lacerda Nunes Pinto
