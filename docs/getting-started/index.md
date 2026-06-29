---
title: Getting started
---

# Getting started

Three short pages take you from nothing to querying your own notes:

<div class="grid cards" markdown>

-   :material-download: __[Installation](installation.md)__

    Install Mimir and its prerequisites (Docker, uv, optionally Ollama).

-   :material-rocket-launch: __[Quickstart](quickstart.md)__

    The five-command path from a fresh clone to your first answer.

-   :material-cog: __[Configuration](configuration.md)__

    Every `MIMIR_*` setting, what it does, and sensible defaults.

</div>

## What you'll need

| Requirement | Why | Required? |
|---|---|---|
| **macOS / Linux** | Mimir is tested on Apple Silicon and Linux | Yes |
| **Python 3.11+** | Runtime | Yes |
| **Docker** (or OrbStack) | Runs the Qdrant vector store | Yes |
| **[uv](https://github.com/astral-sh/uv)** | Fast Python package manager | Recommended |
| **[Ollama](https://ollama.ai/)** | Local LLM for the `chat` command | Only for `chat` |

!!! tip "On Apple Silicon, OrbStack is lighter than Docker Desktop"
    `brew install --cask orbstack` gives you a Docker-compatible runtime that
    idles at a fraction of the memory.
