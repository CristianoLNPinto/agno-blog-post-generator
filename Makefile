.PHONY: help install dev-install test lint format clean run-cli run-api docker-build docker-run

help:
	@echo "Available commands:"
	@echo "  make install       - Install production dependencies"
	@echo "  make dev-install   - Install development dependencies"
	@echo "  make test          - Run tests"
	@echo "  make lint          - Run linting"
	@echo "  make format        - Format code"
	@echo "  make clean         - Clean temporary files"
	@echo "  make run-cli       - Run CLI blog generator"
	@echo "  make run-api       - Run FastAPI server"
	@echo "  make docker-build  - Build Docker image"
	@echo "  make docker-run    - Run Docker container"

install:
	pip install -e .

dev-install:
	pip install -e ".[dev]"

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

run-cli:
	python -m src.agno.cli

run-api:
	uvicorn src.agno.infrastructure.api.main:app --reload --host 0.0.0.0 --port 8000

docker-build:
	docker build -t agno-blog-generator .

docker-run:
	docker-compose up
