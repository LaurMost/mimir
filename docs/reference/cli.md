---
title: CLI reference
---

# CLI reference

Every Mimir command, argument, and option below is generated directly from the
[Typer](https://typer.tiangolo.com/) application source, so it never drifts out
of date.

!!! tip "Help on demand"
    Every command also accepts `--help`:

    ```bash
    uv run mimir --help
    uv run mimir query --help
    ```

::: mkdocs-typer
    :module: mimir.cli
    :command: app
    :prog_name: mimir
    :depth: 1
