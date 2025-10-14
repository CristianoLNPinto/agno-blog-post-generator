# 🚀 Comet ML Quick Reference

## ⚡ Quick Setup (30 seconds)

```bash
# 1. Install
uv pip install comet_ml

# 2. Configure
./setup_comet_env.sh

# 3. Test
python test_comet_integration.py

# 4. Run
streamlit run streamlit_app.py
```

## 🔑 Credentials

```bash
COMET_API_KEY=your_comet_api_key_here
COMET_PROJECT_NAME=your_project_name
COMET_WORKSPACE=your_workspace_name
```

## 📊 View Dashboard

**URL:** https://www.comet.com/[your-workspace]/[your-project]

## 🎯 Key Metrics at a Glance

| Metric | What it Tracks |
|--------|----------------|
| `phase_*_duration_seconds` | Time for each phase |
| `*_cache_hit` | Cache effectiveness |
| `articles_scraped` | Successful scrapes |
| `scrape_success_rate` | Scraping quality |
| `blog_word_count` | Output size |
| `generation_success` | Overall success |

## 💻 Common Code Patterns

### Get Tracker
```python
from src.agno_blog.infrastructure.observability import get_comet_tracker

tracker = get_comet_tracker()
```

### Log Metrics
```python
tracker.log_metric("my_metric", 42)
tracker.log_metrics({"metric1": 1, "metric2": 2})
```

### Track Phase
```python
with tracker.track_phase("my_phase"):
    # your code here
    pass
```

### Log Parameters
```python
tracker.log_parameters({
    "param1": "value",
    "param2": 123
})
```

### End Experiment
```python
tracker.end()
```

## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| Not tracking | Check `.env` has `COMET_API_KEY` |
| Import error | Run `uv pip install comet_ml` |
| No experiments | Verify API key and workspace |
| Slow performance | Set `comet_enabled = False` in config |

## 📖 Documentation

- **Setup Guide:** [COMET_ML_SETUP.md](COMET_ML_SETUP.md)
- **Full Docs:** [OBSERVABILITY.md](OBSERVABILITY.md)
- **Implementation:** [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)

## 🎨 Disable Tracking

### Temporary (in code)
```python
from src.agno_blog.config import settings
settings.comet_enabled = False
```

### Permanent (in .env)
```bash
# Comment out or remove COMET_API_KEY
# COMET_API_KEY=...
```

## 📞 Quick Help

```bash
# Test integration
python test_comet_integration.py

# Check config
python -c "from src.agno_blog.config import settings; print(f'Enabled: {settings.comet_enabled}, Key: {bool(settings.comet_api_key)}')"

# View logs
# Check console output when running app
```

## ✅ Checklist

- [ ] Installed comet_ml
- [ ] Configured .env with credentials
- [ ] Ran test_comet_integration.py
- [ ] Generated a blog post
- [ ] Viewed experiment in Comet ML dashboard
- [ ] Reviewed metrics and logs

---

**Need more help?** See [COMET_ML_SETUP.md](COMET_ML_SETUP.md) for detailed instructions.
