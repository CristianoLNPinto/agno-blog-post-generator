# Documentation Index

Welcome to the Agno Blog Generator documentation!

## 📚 Documentation Structure

### Getting Started
- **[Getting Started Guide](guides/GETTING_STARTED.md)** - Installation, setup, and your first blog post
- **[Quick Start](../QUICK_START.md)** - Fast track to generating blog posts

### API Documentation
- **[API Reference](api/API_REFERENCE.md)** - Complete REST API documentation
- **[Swagger/OpenAPI](http://localhost:8000/docs)** - Interactive API documentation (when server is running)

### Architecture & Design
- **[Architecture Overview](architecture/ARCHITECTURE.md)** - System design and patterns
- **[Domain-Driven Design](architecture/ARCHITECTURE.md#layer-responsibilities)** - DDD implementation details

### Guides
- **[Development Guide](guides/DEVELOPMENT.md)** - Contributing and development workflow
- **[Observability Guide](guides/OBSERVABILITY.md)** - Monitoring and tracking with Comet ML & Opik

### Project Information
- **[Main README](../README.md)** - Project overview and quick reference
- **[Changelog](../CHANGELOG.md)** - Version history and changes
- **[License](../LICENSE)** - MIT License

## 🚀 Quick Links

### For Users
1. [Install and Setup](guides/GETTING_STARTED.md#installation)
2. [Generate Your First Blog Post](guides/GETTING_STARTED.md#your-first-blog-post)
3. [Use the API](api/API_REFERENCE.md#endpoints)
4. [Enable Observability](guides/OBSERVABILITY.md#setup)

### For Developers
1. [Development Setup](guides/DEVELOPMENT.md#development-setup)
2. [Project Structure](guides/DEVELOPMENT.md#project-structure)
3. [Coding Standards](guides/DEVELOPMENT.md#coding-standards)
4. [Testing Guide](guides/DEVELOPMENT.md#testing)

### For Architects
1. [Architecture Overview](architecture/ARCHITECTURE.md#overview)
2. [Design Patterns](architecture/ARCHITECTURE.md#design-patterns)
3. [Data Flow](architecture/ARCHITECTURE.md#data-flow)
4. [Scalability](architecture/ARCHITECTURE.md#scalability-considerations)

## 📖 Documentation by Topic

### Installation & Setup
- [Prerequisites](guides/GETTING_STARTED.md#prerequisites)
- [Installation Steps](guides/GETTING_STARTED.md#installation)
- [Environment Configuration](guides/GETTING_STARTED.md#configure-environment)
- [Troubleshooting](guides/GETTING_STARTED.md#troubleshooting)

### Usage
- [Streamlit UI](guides/GETTING_STARTED.md#option-1-streamlit-ui-recommended)
- [REST API](guides/GETTING_STARTED.md#option-2-api-mode)
- [CLI Interface](guides/GETTING_STARTED.md#option-3-cli-mode)
- [Docker Deployment](guides/GETTING_STARTED.md#docker-mode)

### Features
- [Multi-Agent System](architecture/ARCHITECTURE.md#3-domain-layer)
- [Caching System](guides/GETTING_STARTED.md#caching-system)
- [Observability](guides/OBSERVABILITY.md)
- [API Documentation](api/API_REFERENCE.md)

### Development
- [Project Structure](guides/DEVELOPMENT.md#project-structure)
- [Development Workflow](guides/DEVELOPMENT.md#development-workflow)
- [Testing](guides/DEVELOPMENT.md#testing)
- [Code Quality](guides/DEVELOPMENT.md#coding-standards)

### API
- [Endpoints](api/API_REFERENCE.md#endpoints)
- [Request/Response Models](api/API_REFERENCE.md#blog-generation)
- [Error Handling](api/API_REFERENCE.md#error-codes)
- [Examples](api/API_REFERENCE.md#example-usage)

### Observability
- [Comet ML Setup](guides/OBSERVABILITY.md#comet-ml---experiment-tracking)
- [Opik Setup](guides/OBSERVABILITY.md#opik---llm-tracing)
- [Metrics](guides/OBSERVABILITY.md#key-metrics-to-monitor)
- [Debugging](guides/OBSERVABILITY.md#debugging-with-traces)

## 🎯 Common Tasks

### I want to...

**Generate a blog post**
→ [Getting Started Guide](guides/GETTING_STARTED.md#your-first-blog-post)

**Integrate the API**
→ [API Reference](api/API_REFERENCE.md)

**Understand the architecture**
→ [Architecture Overview](architecture/ARCHITECTURE.md)

**Contribute to the project**
→ [Development Guide](guides/DEVELOPMENT.md)

**Monitor performance**
→ [Observability Guide](guides/OBSERVABILITY.md)

**Deploy to production**
→ [Docker Guide](guides/GETTING_STARTED.md#docker-mode)

**Customize agents**
→ [Development Guide](guides/DEVELOPMENT.md#adding-a-new-agent)

**Debug issues**
→ [Troubleshooting](guides/GETTING_STARTED.md#troubleshooting)

## 🔧 Configuration

### Environment Variables

```bash
# Required
GOOGLE_API_KEY=your_gemini_api_key

# Optional - Observability
COMET_API_KEY=your_comet_api_key
COMET_PROJECT_NAME=agno-blog-post-generator
COMET_WORKSPACE=your_workspace

OPIK_API_KEY=your_opik_api_key
OPIK_PROJECT_NAME=agno-blog-llm-tracing
OPIK_WORKSPACE=your_workspace
```

See [Getting Started](guides/GETTING_STARTED.md#configure-environment) for details.

## 📊 Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     Presentation Layer                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Streamlit UI │  │  FastAPI     │  │     CLI      │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                             │
┌─────────────────────────────────────────────────────────────┐
│                     Application Layer                         │
│                  ┌──────────────────────┐                    │
│                  │BlogGenerationService │                    │
│                  └──────────────────────┘                    │
└─────────────────────────────────────────────────────────────┘
                             │
┌─────────────────────────────────────────────────────────────┐
│                       Domain Layer                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │Research Agent│  │Scraper Agent │  │ Writer Agent │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                             │
┌─────────────────────────────────────────────────────────────┐
│                   Infrastructure Layer                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  LLM Provider│  │   Database   │  │Observability │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

See [Architecture Documentation](architecture/ARCHITECTURE.md) for details.

## 🤝 Contributing

We welcome contributions! Please see:
- [Development Guide](guides/DEVELOPMENT.md)
- [Coding Standards](guides/DEVELOPMENT.md#coding-standards)
- [Testing Guide](guides/DEVELOPMENT.md#testing)

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Agno](https://github.com/agno-ai/agno) framework
- Powered by Google's Gemini API
- Observability by Comet ML and Opik

## 📬 Support

- **Documentation**: You're reading it!
- **Issues**: [GitHub Issues](https://github.com/CristianoLNPinto/agno-blog-post-generator/issues)
- **Discussions**: [GitHub Discussions](https://github.com/CristianoLNPinto/agno-blog-post-generator/discussions)

---

**Need help?** Start with the [Getting Started Guide](guides/GETTING_STARTED.md)!
