# Comet ML Observability Setup

This document explains how to set up Comet ML observability for the Agno Blog Post Generator.

## Installation

Comet ML has been installed using:
```bash
uv pip install comet_ml
```

## Configuration

### 1. Create .env file

Copy the `.env.example` file to `.env`:
```bash
cp .env.example .env
```

### 2. Add Comet ML Credentials

Edit the `.env` file and add your Comet ML credentials:

```bash
# Comet ML Configuration
COMET_API_KEY=your_comet_api_key_here
COMET_PROJECT_NAME=your_project_name
COMET_WORKSPACE=your_workspace_name
```

### 3. Optional: Disable Comet ML Tracking

If you want to disable Comet ML tracking temporarily, you can set in your code:
```python
from src.agno_blog.config import settings
settings.comet_enabled = False
```

## What Gets Tracked

The Comet ML integration tracks the following metrics and data:

### Parameters
- **topic**: The blog post topic
- **use_search_cache**: Whether search cache is enabled
- **use_scrape_cache**: Whether scrape cache is enabled
- **use_blog_cache**: Whether blog cache is enabled
- **model_id**: The AI model being used

### Metrics

#### Search Phase
- `search_cache_hit`: Whether search results were found in cache (1) or not (0)
- `search_attempts`: Number of attempts needed to find articles
- `search_articles_found`: Number of articles found
- `search_failed`: Whether search failed (1) or not (0)
- `phase_search_duration_seconds`: Time taken for search phase

#### Scraping Phase
- `scrape_cache_hit`: Whether scraped articles were found in cache (1) or not (0)
- `articles_scraped`: Number of articles successfully scraped
- `articles_failed`: Number of articles that failed to scrape
- `scrape_success_rate`: Percentage of successful scrapes
- `phase_scraping_duration_seconds`: Time taken for scraping phase

#### Writing Phase
- `phase_writing_duration_seconds`: Time taken for writing phase

#### Overall Metrics
- `blog_cache_hit`: Whether blog post was found in cache (1) or not (0)
- `blog_length`: Length of generated blog post in characters
- `blog_word_count`: Number of words in the blog post
- `sources_used`: Number of sources used to generate the blog
- `generation_success`: Whether generation succeeded (1) or not (0)
- `generation_failed`: Whether generation failed (1) or not (0)

### Text Logs
- The complete generated blog post with metadata

### Tags
- `blog_generation`: All experiments are tagged with this
- `automated`: Indicates automated generation

### Other Data
- `failure_reason`: Reason for failure if generation fails
- Error messages for each phase if errors occur

## Viewing Results

1. Go to [Comet ML](https://www.comet.com/)
2. Navigate to your workspace
3. Select your project
4. View your experiments with all tracked metrics, parameters, and logs

## Usage Examples

### Using in Streamlit App

The Streamlit app automatically initializes Comet ML tracking:

```python
# Tracking is automatically enabled when you run:
streamlit run streamlit_app.py
```

### Using in CLI or Scripts

```python
from src.agno_blog.application.blog_generation_service import BlogGenerationService
from src.agno_blog.infrastructure.observability import get_comet_tracker

# Create a tracker
tracker = get_comet_tracker()

# Initialize service with tracker
service = BlogGenerationService(tracker=tracker)

# Generate blog post (tracking happens automatically)
blog_post = await service.generate_blog_post(
    session_state={},
    topic="Your topic here"
)

# End the experiment
tracker.end()
```

### Manual Tracking

You can also use the tracker manually:

```python
from src.agno_blog.infrastructure.observability import CometTracker

# Initialize tracker
tracker = CometTracker(
    api_key="your_api_key",
    project_name="your_project_name",
    workspace="your_workspace"
)

# Set experiment name
tracker.set_name("my_experiment")

# Log parameters
tracker.log_parameters({
    "param1": "value1",
    "param2": 42
})

# Log metrics
tracker.log_metric("accuracy", 0.95)
tracker.log_metrics({
    "precision": 0.92,
    "recall": 0.88
})

# Track a phase
with tracker.track_phase("data_processing"):
    # Your code here
    pass

# Log text
tracker.log_text("Some important text", metadata={"type": "output"})

# End experiment
tracker.end()
```

## Troubleshooting

### Comet ML Not Tracking

1. Check that your `.env` file has the correct credentials
2. Verify that `COMET_API_KEY` is set correctly
3. Check that `comet_enabled` is `True` in settings
4. Look for error messages in the console logs

### Import Errors

If you see import errors, make sure comet_ml is installed:
```bash
uv pip install comet_ml
```

### Viewing Experiments

If experiments are not showing up in Comet ML:
1. Check that the API key is valid
2. Verify the workspace and project names are correct
3. Check your internet connection
4. Look for error messages in the logs

## Architecture

The observability system is structured as follows:

```
src/agno_blog/infrastructure/observability/
├── __init__.py              # Module exports
└── comet_tracker.py         # CometTracker class implementation

Integration points:
- BlogGenerationService: Tracks all phases of blog generation
- Streamlit App: Initializes tracker for each generation request
```

## Benefits

1. **Performance Monitoring**: Track how long each phase takes
2. **Quality Metrics**: Monitor success rates and article counts
3. **Debugging**: See exactly what parameters were used for each generation
4. **Comparison**: Compare different runs to optimize the system
5. **Reproducibility**: All parameters and results are logged for reproducibility
