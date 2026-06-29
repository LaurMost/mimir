Run the full local quality gate for Mimir and report results concisely:

```bash
uv run ruff check src tests
uv run black --check src tests
uv run mypy src
uv run pytest -q --cov=mimir --cov-report=term-missing
```

If anything fails, summarize the failures by tool and propose the smallest fix.
Do not change unrelated code.
