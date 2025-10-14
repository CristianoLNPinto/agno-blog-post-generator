# Getting Started Guide

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.12+**: [Download Python](https://www.python.org/downloads/)
- **Git**: [Download Git](https://git-scm.com/downloads)
- **Google Gemini API Key**: [Get API Key](https://makersuite.google.com/app/apikey)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/CristianoLNPinto/agno-blog-post-generator.git
cd agno-blog-post-generator
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Linux/Mac:
source .venv/bin/activate

# On Windows:
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
# Install the package and dependencies
pip install -e .

# Or use make (if available)
make install
```

### 4. Configure Environment

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your API keys
nano .env  # or use your preferred editor
```

**Required Configuration** (`.env`):

```bash
# Google Gemini API Key (Required)
GOOGLE_API_KEY=your_gemini_api_key_here
```

**Optional Configuration** (for observability):

```bash
# Comet ML (Optional - for experiment tracking)
COMET_API_KEY=your_comet_api_key
COMET_PROJECT_NAME=agno-blog-post-generator
COMET_WORKSPACE=your_workspace

# Opik (Optional - for LLM tracing)
OPIK_API_KEY=your_opik_api_key
OPIK_PROJECT_NAME=agno-blog-llm-tracing
OPIK_WORKSPACE=your_workspace
```

## Quick Start

### Option 1: Streamlit UI (Recommended)

The easiest way to get started is with the Streamlit web interface:

```bash
# Start the Streamlit app
streamlit run streamlit_app.py

# Or use make
make run-streamlit
```

Then open your browser to: http://localhost:8501

**Features**:
- 🎨 Beautiful, modern interface
- 📊 Real-time progress tracking
- 📄 View output in HTML or Markdown
- 💾 Download blog posts
- 💡 Example topics for testing

### Option 2: API Mode

Start the FastAPI server for programmatic access:

```bash
# Start the API server
uvicorn src.agno_blog.infrastructure.api.main:app --reload

# Or use make
make run-api
```

Then access:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

**Example API Request**:

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

### Option 3: CLI Mode

Use the command-line interface for quick generation:

```bash
# Run the CLI
python -m src.agno_blog.cli

# Or use make
make run-cli
```

Follow the prompts to enter your topic and generate a blog post.

## Your First Blog Post

Let's generate your first blog post using the Streamlit UI:

1. **Start the app**:
   ```bash
   streamlit run streamlit_app.py
   ```

2. **Enter a topic**:
   - Try: "The Future of AI in Healthcare"
   - Or use one of the example topics

3. **Configure caching** (optional):
   - Enable all caches for faster generation
   - Disable caches for fresh content

4. **Generate**:
   - Click "Generate Blog Post"
   - Watch real-time progress
   - See results in ~30-60 seconds (first time)
   - See results in ~1-5 seconds (cached)

5. **View and Download**:
   - Switch between Markdown and HTML views
   - Download in your preferred format

## Understanding the Process

The blog generation happens in three phases:

### 1. Research Phase 🔍
- Searches for relevant articles on your topic
- Evaluates source quality
- Selects the best sources
- **Time**: ~10-20 seconds

### 2. Extraction Phase 📄
- Scrapes content from selected articles
- Extracts main content
- Processes and cleans text
- **Time**: ~10-20 seconds

### 3. Writing Phase ✍️
- Analyzes extracted content
- Synthesizes information
- Generates professional blog post
- Applies SEO best practices
- **Time**: ~10-20 seconds

## Caching System

The system uses three levels of caching:

### Search Cache
- Stores search results for topics
- Improves performance for similar topics
- Location: `data/cache/search/`

### Scrape Cache
- Stores extracted article content
- Reduces external API calls
- Location: `data/cache/scrape/`

### Blog Cache
- Stores generated blog posts
- Returns existing posts instantly
- Location: `data/cache/blog/`

**Cache Benefits**:
- ⚡ Faster generation (1-5 seconds vs 30-60 seconds)
- 💰 Reduced API costs
- 🌐 Less external requests
- ♻️ Reuse of quality content

**When to Disable Caching**:
- Need fresh, up-to-date content
- Testing different generation approaches
- Want to see different results for same topic

## Troubleshooting

### API Key Issues

**Problem**: "Invalid API key" error

**Solution**:
1. Verify your API key in `.env`
2. Ensure no extra spaces or quotes
3. Get a new key from [Google AI Studio](https://makersuite.google.com/app/apikey)

### Installation Issues

**Problem**: Package installation fails

**Solution**:
```bash
# Upgrade pip
pip install --upgrade pip

# Install with verbose output
pip install -e . -v

# Try installing dependencies separately
pip install agno fastapi streamlit
```

### Port Already in Use

**Problem**: "Address already in use" error

**Solution**:
```bash
# For Streamlit (default port 8501)
streamlit run streamlit_app.py --server.port 8502

# For FastAPI (default port 8000)
uvicorn src.agno_blog.infrastructure.api.main:app --port 8001
```

### Slow Generation

**Problem**: Blog generation takes too long

**Solution**:
1. Enable all caching options
2. Check your internet connection
3. Verify API key is valid
4. Try a more specific topic

### Cache Issues

**Problem**: Want to clear cache

**Solution**:
```bash
# Clear all caches
make clean

# Or manually
rm -rf data/cache/*
```

## Next Steps

Now that you're up and running:

1. **Explore Features**: Try different topics and caching options
2. **Read Documentation**: Check out other guides in `/docs`
3. **API Integration**: Integrate the API into your applications
4. **Customize**: Modify agents and prompts for your needs
5. **Contribute**: Submit issues or pull requests

## Additional Resources

- **API Reference**: [docs/api/API_REFERENCE.md](../api/API_REFERENCE.md)
- **Architecture**: [docs/architecture/ARCHITECTURE.md](../architecture/ARCHITECTURE.md)
- **Observability**: [docs/guides/OBSERVABILITY.md](./OBSERVABILITY.md)
- **Development**: [docs/guides/DEVELOPMENT.md](./DEVELOPMENT.md)

## Getting Help

If you encounter issues:

1. Check the [Troubleshooting](#troubleshooting) section
2. Review the documentation in `/docs`
3. Search [GitHub Issues](https://github.com/CristianoLNPinto/agno-blog-post-generator/issues)
4. Open a new issue with:
   - Error message
   - Steps to reproduce
   - Environment details (OS, Python version)

## Quick Reference

### Common Commands

```bash
# Install dependencies
make install

# Run Streamlit UI
make run-streamlit

# Run API server
make run-api

# Run CLI
make run-cli

# Run tests
make test

# Clean cache and temp files
make clean

# Format code
make format

# Run linters
make lint
```

### Environment Variables

```bash
# Required
GOOGLE_API_KEY=your_key

# Optional - Observability
COMET_API_KEY=your_key
COMET_PROJECT_NAME=project_name
COMET_WORKSPACE=workspace_name

OPIK_API_KEY=your_key
OPIK_PROJECT_NAME=project_name
OPIK_WORKSPACE=workspace_name
```

### Default Ports

- **Streamlit**: 8501
- **FastAPI**: 8000

---

**Ready to generate amazing blog posts? Let's get started! 🚀**
