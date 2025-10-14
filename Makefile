.PHONY: help install dev-install sync test lint format clean run-cli run-api run-streamlit stop-api check-api docker-build docker-run

help:
	@echo "Available commands:"
	@echo "  make install       - Install production dependencies with uv"
	@echo "  make dev-install   - Install development dependencies with uv"
	@echo "  make sync          - Sync all dependencies (install agno framework + local package)"
	@echo "  make test          - Run tests"
	@echo "  make lint          - Run linting"
	@echo "  make format        - Format code"
	@echo "  make clean         - Clean temporary files"
	@echo "  make run-streamlit - Run Streamlit web interface (recommended)"
	@echo "  make run-cli       - Run CLI blog generator"
	@echo "  make run-api       - Run FastAPI server"
	@echo "  make stop-api      - Stop the API server"
	@echo "  make check-api     - Check if API is running"
	@echo "  make docker-build  - Build Docker image"
	@echo "  make docker-run    - Run Docker container"

install:
	uv pip install -e .

dev-install:
	uv pip install -e ".[dev]"

sync:
	@echo "Installing agno framework..."
	uv pip install agno==2.1.0
	@echo "Installing local package..."
	uv pip install -e ".[dev]"
	@echo "✅ All dependencies synced!"

test:
	pytest tests/ -v

lint:
	ruff check src/ tests/
	mypy src/

format:
	ruff format src/ tests/
	ruff check --fix src/ tests/

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf .ruff_cache
	rm -rf dist/
	rm -rf build/

run-streamlit:
	streamlit run streamlit_app.py

run-cli:
	python -m src.agno_blog.cli

run-api:
	uvicorn src.agno_blog.infrastructure.api.main:app --reload --host 0.0.0.0 --port 8000

stop-api:
	@echo "Stopping API server on port 8000..."
	@-pkill -f "uvicorn src.agno_blog.infrastructure.api.main:app" || echo "No API server running"
	@echo "✅ API server stopped"

check-api:
	@echo "Checking API server status..."
	@curl -s http://localhost:8000/health && echo "\n✅ API is running" || echo "❌ API is not running"

docker-build:
	docker build -t agno-blog-generator .

docker-run:
	docker-compose up
