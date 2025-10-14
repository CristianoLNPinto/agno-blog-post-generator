# 🚀 Opik Quick Reference

## ⚡ Quick Setup (30 seconds)

```bash
# 1. Install
uv pip install opik opentelemetry-sdk opentelemetry-exporter-otlp openinference-instrumentation-agno

# 2. Configure .env
# Add to .env:
OPIK_API_KEY=your_api_key
OPIK_PROJECT_NAME=agno-blog-llm-tracing
OPIK_WORKSPACE=your_workspace

# 3. Run (automatic tracing!)
streamlit run streamlit_app.py
```

## 🔑 Configuration

```bash
# Same as Comet ML credentials
OPIK_API_KEY=your_comet_api_key
OPIK_PROJECT_NAME=agno-blog-llm-tracing
OPIK_WORKSPACE=your_workspace
```

## 📊 View Traces

**URL:** https://www.comet.com/[your-workspace]/[your-project]

Navigate to the "LLM Tracing" or "Opik" section

## 🎯 What Gets Traced

| Item | Description |
|------|-------------|
| **Agent Calls** | Every agent invocation |
| **LLM Calls** | All calls to Gemini |
| **Prompts** | Complete prompts sent |
| **Responses** | Full LLM responses |
| **Token Usage** | Input/output tokens |
| **Latency** | Time per call |
| **Tool Usage** | Search, scraping tools |
| **Errors** | Stack traces |

## 💻 Usage

### Automatic (Streamlit)
```python
# Already configured in streamlit_app.py
# Just run the app - tracing happens automatically!
streamlit run streamlit_app.py
```

### Manual (Scripts)
```python
from src.agno_blog.infrastructure.observability import instrument_agno_globally

# Instrument once at startup
instrument_agno_globally()

# All agent calls are now traced!
service = BlogGenerationService()
blog_post = await service.generate_blog_post(...)
```

### Context Manager
```python
from src.agno_blog.infrastructure.observability import OpikTracer

with OpikTracer() as tracer:
    # Traced only in this block
    service = BlogGenerationService()
    blog_post = await service.generate_blog_post(...)
```

## 🔧 Disable Tracing

### Temporary
```python
from src.agno_blog.config import settings
settings.opik_enabled = False
```

### Permanent
```bash
# In .env, comment out:
# OPIK_API_KEY=...
```

## 🆚 Opik vs Comet ML

| Feature | Comet ML | Opik |
|---------|----------|------|
| **Purpose** | Experiment tracking | LLM tracing |
| **Tracks** | Metrics, parameters | Prompts, responses |
| **Use For** | A/B testing, metrics | Debug agents, optimize prompts |
| **Data** | Aggregated stats | Individual LLM calls |
| **View** | Charts, comparisons | Trace timeline, spans |

**Use Both Together** for complete observability!

## 🔍 Common Use Cases

### Debug Agent Behavior
```
1. Run blog generation
2. Go to Opik dashboard
3. View trace timeline
4. Inspect each agent decision
5. See exact prompts used
```

### Optimize Token Usage
```
1. Check token usage in dashboard
2. Identify expensive prompts
3. Optimize prompt length
4. Compare before/after
```

### Monitor Production
```
1. Enable tracing in production
2. Set up alerts for errors
3. Monitor latency trends
4. Track cost over time
```

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| No traces | Check OPIK_API_KEY in .env |
| Import error | Run: `uv pip install opik openinference-instrumentation-agno` |
| Slow performance | Disable: `settings.opik_enabled = False` |
| Wrong project | Check OPIK_PROJECT_NAME in .env |

## 📖 Key Concepts

### Traces
A complete record of a blog generation request, including all agent calls.

### Spans
Individual operations within a trace (e.g., one LLM call, one tool use).

### Instrumentation
Automatic wrapping of Agno agents to capture telemetry data.

### OTLP
OpenTelemetry Protocol - standard for sending trace data.

## 🎨 Dashboard Features

- **Timeline View**: See all operations in chronological order
- **Span Tree**: Hierarchical view of agent → LLM → tool calls
- **Prompt Inspector**: View exact prompts and responses
- **Token Counter**: Track usage and costs
- **Error Viewer**: Debug failures with stack traces
- **Search & Filter**: Find specific traces quickly

## 📚 Documentation

- **Setup Guide:** [OPIK_SETUP.md](OPIK_SETUP.md)
- **Opik Docs:** https://www.comet.com/docs/opik/
- **GitHub:** https://github.com/comet-ml/opik

## ✅ Checklist

- [ ] Installed Opik packages
- [ ] Configured .env with API key
- [ ] Ran Streamlit app
- [ ] Generated a blog post
- [ ] Viewed trace in Opik dashboard
- [ ] Inspected LLM calls and prompts

---

**Need help?** See [OPIK_SETUP.md](OPIK_SETUP.md) for detailed instructions.
