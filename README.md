# 🎨 Agno - AI Blog Post Generator

An advanced AI-powered blog post generator that combines web research, content extraction, and professional writing using Google's Gemini API.

## ✨ Features

- **Intelligent Web Research**: Automatically finds and evaluates high-quality sources
- **Content Extraction**: Scrapes and processes articles with smart formatting
- **Professional Writing**: Generates engaging, SEO-optimized blog posts
- **Caching System**: Efficient content caching for faster generation
- **REST API**: FastAPI-based API for easy integration
- **CLI Interface**: Command-line tool for quick blog generation
- **Docker Support**: Containerized deployment ready

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
│   └── llm_providers/ # LLM configurations
└── config.py          # Configuration management
```

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

### Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd treinamento_agno
```

2. **Create virtual environment**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**
```bash
make install
# or
pip install -e .
```

4. **Configure environment**
```bash
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY
```

### Usage

#### CLI Mode

Generate a blog post from the command line:

```bash
make run-cli
# or
python -m src.agno_blog.cli
```

#### API Mode

Start the FastAPI server:

```bash
make run-api
# or
uvicorn src.agno_blog.infrastructure.api.main:app --reload
```

Then access:
- API docs: http://localhost:8000/docs
- Health check: http://localhost:8000/health

**Example API request:**

```bash
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "The Future of AI in Healthcare",
    "use_search_cache": true,
    "use_scrape_cache": true,
    "use_blog_cache": true
  }'
```

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
treinamento_agno/
├── src/agno_blog/            # Source code
│   ├── domain/               # Business logic
│   ├── application/          # Use cases
│   ├── infrastructure/       # External interfaces
│   ├── config.py            # Configuration
│   └── cli.py               # CLI entry point
├── tests/                    # Test suite
├── data/                     # Data storage
├── notebooks/                # Jupyter notebooks
├── static/                   # Static assets
├── tmp/                      # Temporary files
├── .env                      # Environment variables (gitignored)
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
```

Additional settings can be configured in `src/agno_blog/config.py`.

## 📚 How It Works

1. **Research Phase**: The research agent searches for relevant articles on the given topic
2. **Extraction Phase**: The scraper agent extracts full content from found articles
3. **Writing Phase**: The writer agent synthesizes information into a professional blog post
4. **Caching**: Results are cached at each stage for efficiency

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Agno](https://github.com/agno-ai/agno) framework
- Powered by Google's Gemini API
- Architecture inspired by [agent-api-cookiecutter](https://github.com/neural-maze/agent-api-cookiecutter)

## 📬 Contact

For questions or feedback, please open an issue on GitHub.

---

Made with ❤️ by Cristiano Lacerda Nunes Pinto
