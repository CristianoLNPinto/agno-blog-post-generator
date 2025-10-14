# 📊 Observability with Comet ML

This document provides a comprehensive guide to the observability features implemented in the Agno Blog Post Generator using Comet ML.

## 🎯 Overview

The project now includes full observability through Comet ML, tracking:
- **Performance metrics** for each phase (search, scraping, writing)
- **Success rates** and failure reasons
- **Cache hit rates** for optimization insights
- **Complete experiment logs** with parameters and outputs
- **Duration tracking** for performance analysis

## 🚀 Quick Start

### 1. Install Dependencies

```bash
uv pip install comet_ml
```

### 2. Configure Credentials

Run the setup script:
```bash
./setup_comet_env.sh
```

Or manually create/update your `.env` file:
```bash
COMET_API_KEY=your_comet_api_key_here
COMET_PROJECT_NAME=your_project_name
COMET_WORKSPACE=your_workspace_name
```

### 3. Run the Application

```bash
# Streamlit app (with automatic tracking)
streamlit run streamlit_app.py

# CLI (tracking enabled by default)
python blog_post_generator.py "Your topic here"
```

## 📈 Tracked Metrics

### Search Phase Metrics
| Metric | Description | Type |
|--------|-------------|------|
| `search_cache_hit` | Cache hit (1) or miss (0) | Binary |
| `search_attempts` | Number of search attempts | Integer |
| `search_articles_found` | Articles found in search | Integer |
| `search_failed` | Search failure indicator | Binary |
| `phase_search_duration_seconds` | Search phase duration | Float |

### Scraping Phase Metrics
| Metric | Description | Type |
|--------|-------------|------|
| `scrape_cache_hit` | Cache hit (1) or miss (0) | Binary |
| `articles_scraped` | Successfully scraped articles | Integer |
| `articles_failed` | Failed scraping attempts | Integer |
| `scrape_success_rate` | Success rate (0.0-1.0) | Float |
| `phase_scraping_duration_seconds` | Scraping phase duration | Float |

### Writing Phase Metrics
| Metric | Description | Type |
|--------|-------------|------|
| `phase_writing_duration_seconds` | Writing phase duration | Float |

### Overall Metrics
| Metric | Description | Type |
|--------|-------------|------|
| `blog_cache_hit` | Blog cache hit (1) or miss (0) | Binary |
| `blog_length` | Blog post length in characters | Integer |
| `blog_word_count` | Blog post word count | Integer |
| `sources_used` | Number of sources used | Integer |
| `generation_success` | Success indicator | Binary |
| `generation_failed` | Failure indicator | Binary |

## 🏗️ Architecture

```
src/agno_blog/infrastructure/observability/
├── __init__.py                    # Module exports
└── comet_tracker.py              # CometTracker implementation
    ├── CometTracker              # Main tracking class
    └── get_comet_tracker()       # Factory function
```

### Integration Points

1. **BlogGenerationService** (`service.py`)
   - Tracks all three phases (search, scraping, writing)
   - Logs metrics at each step
   - Captures errors and failures

2. **Streamlit App** (`streamlit_app.py`)
   - Initializes tracker for each generation
   - Properly ends experiments
   - Handles exceptions with logging

## 💻 Usage Examples

### Basic Usage (Automatic)

The tracking is automatic when using the standard interfaces:

```python
from src.agno_blog.application.blog_generation_service import BlogGenerationService

# Tracker is automatically initialized
service = BlogGenerationService()

# All tracking happens automatically
blog_post = await service.generate_blog_post(
    session_state={},
    topic="The Future of AI"
)
```

### Custom Tracker Configuration

```python
from src.agno_blog.infrastructure.observability import CometTracker

# Create custom tracker
tracker = CometTracker(
    api_key="your_api_key",
    project_name="custom_project",
    workspace="your_workspace",
    enabled=True
)

# Use with service
service = BlogGenerationService(tracker=tracker)
```

### Manual Tracking

```python
from src.agno_blog.infrastructure.observability import get_comet_tracker

# Get tracker instance
tracker = get_comet_tracker()

# Set experiment details
tracker.set_name("custom_experiment")
tracker.add_tags(["custom", "test"])

# Log parameters
tracker.log_parameters({
    "temperature": 0.7,
    "max_tokens": 1000
})

# Track a phase
with tracker.track_phase("custom_phase"):
    # Your code here
    result = do_something()

# Log metrics
tracker.log_metrics({
    "accuracy": 0.95,
    "latency": 1.2
})

# Log text output
tracker.log_text(result, metadata={"type": "output"})

# End experiment
tracker.end()
```

### Context Manager Usage

```python
from src.agno_blog.infrastructure.observability import CometTracker

# Use as context manager (auto-ends experiment)
with CometTracker() as tracker:
    tracker.set_name("my_experiment")
    tracker.log_metric("score", 0.85)
    # Experiment automatically ends when exiting context
```

## 🔍 Viewing Experiments

### Comet ML Dashboard

1. Visit [https://www.comet.com/](https://www.comet.com/)
2. Navigate to your workspace
3. Select your project
4. View experiments with:
   - Metrics charts
   - Parameter comparisons
   - Text logs
   - Duration analysis

### Key Insights to Monitor

1. **Performance Trends**
   - Average duration per phase
   - Total generation time
   - Bottleneck identification

2. **Cache Effectiveness**
   - Cache hit rates
   - Time saved by caching
   - Cache optimization opportunities

3. **Quality Metrics**
   - Scraping success rates
   - Articles found per search
   - Blog post length distribution

4. **Failure Analysis**
   - Failure reasons
   - Error patterns
   - Retry success rates

## ⚙️ Configuration Options

### Environment Variables

```bash
# Required
COMET_API_KEY=your_api_key

# Optional (with defaults)
COMET_PROJECT_NAME=agno-blog-post-generator
COMET_WORKSPACE=your_workspace
```

### Programmatic Configuration

```python
from src.agno_blog.config import settings

# Disable tracking
settings.comet_enabled = False

# Change project name
settings.comet_project_name = "new_project"
```

## 🐛 Troubleshooting

### Tracking Not Working

**Problem**: Experiments not appearing in Comet ML

**Solutions**:
1. Verify API key is correct in `.env`
2. Check internet connectivity
3. Ensure `comet_enabled = True` in settings
4. Look for error messages in console

### Import Errors

**Problem**: `ModuleNotFoundError: No module named 'comet_ml'`

**Solution**:
```bash
uv pip install comet_ml
```

### Performance Impact

**Problem**: Tracking slows down generation

**Solutions**:
1. Disable tracking for development:
   ```python
   settings.comet_enabled = False
   ```
2. Use async logging (already implemented)
3. Reduce logged text size

### Experiment Not Ending

**Problem**: Experiments stay "running" in Comet ML

**Solution**: Always call `tracker.end()` or use context manager:
```python
with get_comet_tracker() as tracker:
    # Your code
    pass  # Automatically ends
```

## 📊 Best Practices

### 1. Naming Conventions

Use descriptive experiment names:
```python
tracker.set_name(f"blog_gen_{topic[:30]}_{timestamp}")
```

### 2. Tagging Strategy

Tag experiments for easy filtering:
```python
tracker.add_tags([
    "production",      # Environment
    "blog_generation", # Task type
    "v1.0",           # Version
    "cached"          # Special conditions
])
```

### 3. Error Logging

Always log errors with context:
```python
try:
    result = await process()
except Exception as e:
    tracker.log_other("error_details", {
        "error": str(e),
        "phase": "scraping",
        "url": url
    })
    raise
```

### 4. Metric Organization

Group related metrics:
```python
tracker.log_metrics({
    "search_articles": 10,
    "search_duration": 2.5,
    "search_success": 1
})
```

### 5. Resource Cleanup

Always end experiments:
```python
try:
    # Your code
    pass
finally:
    tracker.end()
```

## 🔐 Security Notes

1. **Never commit `.env` file** - It's in `.gitignore`
2. **Rotate API keys regularly** - Update in Comet ML dashboard
3. **Use environment-specific keys** - Different keys for dev/prod
4. **Limit key permissions** - Use read-only keys where possible

## 📚 Additional Resources

- [Comet ML Documentation](https://www.comet.com/docs/)
- [Comet ML Python SDK](https://www.comet.com/docs/v2/api-and-sdk/python-sdk/)
- [Best Practices Guide](https://www.comet.com/docs/v2/guides/getting-started/best-practices/)

## 🤝 Contributing

When adding new tracking:

1. Add metrics to this documentation
2. Use descriptive metric names
3. Include units in metric names (e.g., `_seconds`, `_count`)
4. Log both success and failure cases
5. Test with `comet_enabled = False`

## 📝 Changelog

### v1.0.0 - Initial Implementation
- ✅ Comet ML integration
- ✅ Phase duration tracking
- ✅ Success/failure metrics
- ✅ Cache hit rate tracking
- ✅ Complete parameter logging
- ✅ Text output logging
- ✅ Error tracking
