.PHONY: up down logs install dev ingest query chat status reset fmt lint test test-fast precommit release-check help

help: ## Show available targets
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Install runtime deps
	uv sync

dev: ## Install with dev deps + pre-commit hooks
	uv sync --extra dev
	uv run pre-commit install

up: ## Start Qdrant
	docker compose up -d
	@echo "Qdrant dashboard: http://localhost:6333/dashboard"

down: ## Stop Qdrant
	docker compose down

logs: ## Tail Qdrant logs
	docker compose logs -f qdrant

status: ## Show collection stats
	uv run mimir status

ingest: ## Ingest the notes/ directory
	uv run mimir ingest

reset: ## Drop the collection
	uv run mimir reset

fmt: ## Format code with ruff
	uv run ruff format src tests

lint: ## Lint with ruff
	uv run ruff check src tests
	uv run ruff format --check src tests

test: ## Run all tests
	uv run pytest -v

test-fast: ## Run only tests that don't need heavy deps
	uv run pytest -v -k "not integration"

precommit: ## Run pre-commit on all files
	uv run pre-commit run --all-files

release-check: ## Verify pyproject version matches latest tag
	@TAG=$$(git describe --tags --abbrev=0 2>/dev/null || echo "v0.0.0"); \
	VERSION=v$$(uv run python -c "import tomllib; print(tomllib.load(open('pyproject.toml','rb'))['project']['version'])"); \
	echo "latest tag: $$TAG"; echo "pyproject:  $$VERSION"; \
	test "$$TAG" = "$$VERSION" && echo "✅ match" || echo "⚠️  mismatch"
