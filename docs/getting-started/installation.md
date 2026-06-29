---
title: Installation
---

# Installation

Mimir has three moving parts: the **Mimir CLI** itself, a **Qdrant** container for
vector storage, and (optionally) **Ollama** for RAG chat.

## 1. Prerequisites

=== "macOS (Homebrew)"

    ```bash
    # Container runtime — OrbStack is lighter than Docker Desktop on M-series
    brew install --cask orbstack

    # Python package manager + optional local LLM
    brew install uv ollama
    ```

=== "Linux"

    ```bash
    # Docker (see docs.docker.com for your distro)
    curl -fsSL https://get.docker.com | sh

    # uv
    curl -LsSf https://astral.sh/uv/install.sh | sh

    # Ollama (optional, only for `mimir chat`)
    curl -fsSL https://ollama.com/install.sh | sh
    ```

## 2. Install Mimir

Mimir is currently installed from source.

=== "uv (recommended)"

    ```bash
    git clone https://github.com/LaurMost/mimir.git
    cd mimir
    uv sync
    ```

    Run commands with `uv run mimir <command>`.

=== "pip"

    ```bash
    git clone https://github.com/LaurMost/mimir.git
    cd mimir
    python -m venv .venv && source .venv/bin/activate
    pip install -e .
    ```

    Run commands with `mimir <command>`.

!!! note "Why from source?"
    Mimir is alpha software (v0.1.0). Installing from source keeps you on the
    latest changes. A PyPI release will follow once the API stabilizes.

## 3. Start Qdrant

Mimir ships a `docker-compose.yml` that runs Qdrant with REST on `6333` and gRPC
on `6334`:

```bash
docker compose up -d
```

Verify it's healthy:

```bash
curl -sf http://localhost:6333/healthz && echo "Qdrant is up"
```

## 4. (Optional) Pull an Ollama model

Only needed for the `chat` command:

```bash
ollama pull qwen2.5:7b-instruct
```

## Verify the install

```bash
uv run mimir version
uv run mimir status
```

`status` prints your configuration and reports that the collection doesn't exist
yet &mdash; which is expected before your first ingest.

<div class="grid cards" markdown>

-   :material-rocket-launch: __[Continue to the Quickstart →](quickstart.md)__

    Ingest your first notes and run a query.

</div>
