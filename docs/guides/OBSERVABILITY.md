# Observability Guide

## Overview

The Agno Blog Generator includes comprehensive observability through two complementary systems:

1. **Comet ML**: High-level experiment tracking and metrics
2. **Opik**: Detailed LLM call tracing and debugging

## Why Observability?

Observability helps you:
- 📊 Track performance metrics
- 🐛 Debug issues quickly
- 📈 Optimize generation quality
- 💰 Monitor API costs
- 🔍 Understand agent behavior

## Comet ML - Experiment Tracking

### What It Tracks

- **Performance Metrics**:
  - Search phase duration
  - Scraping phase duration
  - Writing phase duration
  - Total generation time

- **Cache Metrics**:
  - Search cache hit rate
  - Scrape cache hit rate
  - Blog cache hit rate

- **Quality Metrics**:
  - Number of sources found
  - Number of articles scraped
  - Success/failure rates

- **Metadata**:
  - Topic
  - Timestamp
  - Configuration settings

### Setup

1. **Install Comet ML** (already included):
   ```bash
   pip install comet-ml
   ```

2. **Get API Key**:
   - Sign up at [Comet ML](https://www.comet.com/)
   - Get your API key from Settings

3. **Configure Environment**:
   ```bash
   # Add to .env
   COMET_API_KEY=your_comet_api_key
   COMET_PROJECT_NAME=agno-blog-post-generator
   COMET_WORKSPACE=your_workspace
   ```

4. **Run Application**:
   ```bash
   # Comet tracking is automatic!
   streamlit run streamlit_app.py
   ```

### Viewing Results

1. Go to [Comet ML Dashboard](https://www.comet.com/)
2. Navigate to your workspace
3. Select your project
4. View experiments and metrics

### Key Metrics to Monitor

| Metric | Description | Good Value |
|--------|-------------|------------|
| `total_duration` | Total generation time | < 60s |
| `search_duration` | Research phase time | < 20s |
| `scrape_duration` | Extraction phase time | < 20s |
| `write_duration` | Writing phase time | < 20s |
| `search_cache_hit` | Search cache hit rate | > 50% |
| `scrape_cache_hit` | Scrape cache hit rate | > 50% |
| `blog_cache_hit` | Blog cache hit rate | > 30% |
| `sources_found` | Number of sources | 5-10 |
| `articles_scraped` | Number of articles | 3-5 |

## Opik - LLM Tracing

### What It Tracks

- **LLM Calls**:
  - Complete prompt and response
  - Token usage (input/output)
  - Latency per call
  - Model used

- **Agent Interactions**:
  - Agent reasoning steps
  - Tool usage
  - Decision making process

- **Errors and Warnings**:
  - Failed LLM calls
  - Timeout issues
  - Rate limiting

### Setup

1. **Install Opik** (already included):
   ```bash
   pip install opik opentelemetry-sdk opentelemetry-exporter-otlp openinference-instrumentation-agno
   ```

2. **Configure Environment**:
   ```bash
   # Add to .env (uses same Comet credentials)
   OPIK_API_KEY=your_comet_api_key
   OPIK_PROJECT_NAME=agno-blog-llm-tracing
   OPIK_WORKSPACE=your_workspace
   ```

3. **Run Application**:
   ```bash
   # Opik tracing is automatic!
   streamlit run streamlit_app.py
   ```

### Viewing Traces

1. Go to [Comet ML Dashboard](https://www.comet.com/)
2. Navigate to your workspace
3. Go to "LLM Tracing" or "Opik" section
4. View detailed traces

### Understanding Traces

Each trace shows:
- **Span**: Individual operation (LLM call, agent step)
- **Duration**: Time taken
- **Input**: Prompt sent to LLM
- **Output**: Response from LLM
- **Metadata**: Model, tokens, cost

### Debugging with Traces

**Problem**: Slow generation

**Solution**:
1. View traces in Opik
2. Identify slowest spans
3. Check if specific agent is slow
4. Optimize prompts or caching

**Problem**: Poor quality output

**Solution**:
1. View the writer agent trace
2. Check the prompt sent
3. Review the response
4. Adjust prompts if needed

## Integration in Code

### Comet ML Integration

```python
from src.agno_blog.infrastructure.observability import CometTracker

# Initialize tracker
tracker = CometTracker()

# Start experiment
tracker.start_experiment(topic="Your Topic")

# Log metrics
tracker.log_metric("search_duration", 15.2)
tracker.log_metric("sources_found", 8)

# Log parameters
tracker.log_parameter("use_cache", True)

# End experiment
tracker.end_experiment()
```

### Opik Integration

Opik tracing is automatic when configured. The `OpikTracer` class handles:
- Automatic instrumentation of Agno agents
- Trace collection and export
- Error handling

```python
from src.agno_blog.infrastructure.observability import OpikTracer

# Initialize tracer (done automatically in service)
tracer = OpikTracer()

# Tracing happens automatically for all agent calls!
```

## Best Practices

### 1. Always Enable in Development

Enable observability during development to:
- Catch issues early
- Understand performance
- Optimize before production

### 2. Monitor Key Metrics

Focus on:
- **Performance**: Response times
- **Quality**: Success rates
- **Cost**: Token usage
- **Cache**: Hit rates

### 3. Set Up Alerts

In Comet ML, set up alerts for:
- High error rates
- Slow response times
- Low cache hit rates

### 4. Regular Review

Review metrics weekly to:
- Identify trends
- Spot anomalies
- Plan optimizations

### 5. Use Tags

Tag experiments with:
- Environment (dev/staging/prod)
- Version
- Feature flags

## Troubleshooting

### Comet ML Not Tracking

**Problem**: No experiments showing up

**Solution**:
1. Verify API key in `.env`
2. Check internet connection
3. Verify workspace and project names
4. Check Comet ML status page

### Opik Not Tracing

**Problem**: No traces appearing

**Solution**:
1. Verify Opik configuration in `.env`
2. Check that OpenTelemetry packages are installed
3. Verify instrumentation is enabled
4. Check for error messages in logs

### High Token Usage

**Problem**: Unexpectedly high token costs

**Solution**:
1. View Opik traces
2. Check prompt sizes
3. Enable caching
4. Optimize prompts

### Slow Performance

**Problem**: Generation is slow

**Solution**:
1. Check Comet ML metrics
2. Identify slow phase
3. View Opik traces for that phase
4. Optimize specific agent or enable caching

## Privacy and Security

### Data Sent to Comet ML

- Metrics and parameters
- Topic (not full blog post by default)
- Performance data
- Configuration settings

### Data Sent to Opik

- Complete prompts and responses
- Token usage
- Agent interactions
- Error messages

### Recommendations

1. **Sensitive Data**: Don't include sensitive data in topics
2. **API Keys**: Never log API keys
3. **PII**: Avoid personally identifiable information
4. **Compliance**: Review Comet ML's privacy policy

## Cost Considerations

### Comet ML

- **Free Tier**: 5,000 experiments/month
- **Team Tier**: Unlimited experiments
- **Enterprise**: Custom pricing

### Opik

- **Free Tier**: 100,000 traces/month
- **Team Tier**: Unlimited traces
- **Enterprise**: Custom pricing

### Optimization Tips

1. **Sampling**: In production, sample traces (e.g., 10%)
2. **Retention**: Set appropriate data retention periods
3. **Filtering**: Filter out health check calls
4. **Batching**: Batch metric uploads

## Advanced Features

### Custom Metrics

```python
# Log custom metrics
tracker.log_metric("custom_metric", value)
tracker.log_metric("quality_score", 0.95)
```

### Experiment Comparison

In Comet ML:
1. Select multiple experiments
2. Click "Compare"
3. View side-by-side metrics
4. Identify best configurations

### Trace Analysis

In Opik:
1. Filter traces by agent
2. Analyze token usage patterns
3. Identify bottlenecks
4. Export traces for analysis

## Disabling Observability

To disable observability:

```bash
# Remove from .env
# COMET_API_KEY=...
# OPIK_API_KEY=...
```

The application will work normally without observability.

## Resources

- **Comet ML Docs**: https://www.comet.com/docs
- **Opik Docs**: https://www.comet.com/docs/opik
- **OpenTelemetry**: https://opentelemetry.io/

## Summary

Observability is crucial for:
- 🎯 **Performance**: Monitor and optimize
- 🐛 **Debugging**: Quickly identify issues
- 💰 **Cost**: Track and reduce API costs
- 📈 **Quality**: Improve generation quality

Enable both Comet ML and Opik for comprehensive observability!
