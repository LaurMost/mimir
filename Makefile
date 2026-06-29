.PHONY: up down logs ingest query chat status reset install fmt lint

install:
	uv sync

up:
	docker compose up -d
	@echo "Qdrant dashboard: http://localhost:6333/dashboard"

down:
	docker compose down

logs:
	docker compose logs -f qdrant

status:
	uv run mimir status

ingest:
	uv run mimir ingest

reset:
	uv run mimir reset

fmt:
	uv run ruff format src

lint:
	uv run ruff check src
