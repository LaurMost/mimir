Build the Mimir documentation site in strict mode and report the outcome:

```bash
uv sync --extra docs
uv run mkdocs build --strict
```

`--strict` fails on broken links or missing references. If the build fails,
summarize the errors and propose fixes. To preview locally instead, use
`uv run mkdocs serve`.
