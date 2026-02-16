.PHONY: help install test test-verbose test-cov test-watch lint format type-check clean

help:
	@echo "AgenteSocial Backend - Make Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make install          Install all dependencies including test deps"
	@echo ""
	@echo "Testing:"
	@echo "  make test             Run all tests"
	@echo "  make test-verbose     Run tests with verbose output"
	@echo "  make test-cov         Run tests with coverage report"
	@echo "  make test-watch       Run tests in watch mode"
	@echo "  make test-health      Run only health tests"
	@echo "  make test-auth        Run only auth tests"
	@echo "  make test-chat        Run only chat tests"
	@echo "  make test-content     Run only content tests"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint             Run all linters (ruff)"
	@echo "  make format           Format code with black and isort"
	@echo "  make type-check       Run type checking with mypy"
	@echo "  make check            Run all checks (format + lint + type-check)"
	@echo ""
	@echo "Development:"
	@echo "  make dev              Start development server"
	@echo "  make clean            Clean up cache and temp files"

install:
	pip install --upgrade pip
	pip install -r requirements.txt
	pip install pytest pytest-asyncio pytest-env pytest-cov pytest-watch
	pip install python-jose[cryptography]
	pip install ruff black isort mypy

test:
	pytest

test-verbose:
	pytest -v

test-cov:
	pytest --cov=app --cov-report=html --cov-report=term

test-watch:
	ptw --runner "pytest -v"

test-health:
	pytest tests/test_health.py -v

test-auth:
	pytest tests/test_auth.py -v

test-chat:
	pytest tests/test_chat.py -v

test-content:
	pytest tests/test_content.py -v

lint:
	ruff check app tests

format:
	black app tests
	isort app tests

type-check:
	mypy app --ignore-missing-imports

check: format lint type-check
	@echo "All checks passed!"

dev:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name ".coverage" -delete 2>/dev/null || true
	find . -type f -name "coverage.xml" -delete 2>/dev/null || true
	@echo "Clean complete!"
