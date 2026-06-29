---
title: Local RAG chat
tags:
  - guide
  - rag
  - ollama
---

# Local RAG chat

`mimir query` returns raw matching chunks. `mimir chat` goes a step further: it
retrieves the relevant chunks, feeds them to a local LLM as context, and streams
back a written answer with citations. All on your machine.

## 1. Install and start Ollama

```bash
brew install ollama   # macOS; see ollama.com for Linux
ollama pull qwen2.5:7b-instruct
```

Ollama runs as a background service on `http://localhost:11434`. If it isn't
running, start it with:

```bash
ollama serve
```

## 2. Ask a question

```bash
uv run mimir chat "summarise my notes on tailoring fabric sourcing"
```

The answer streams token by token, followed by the sources it drew from:

```title="Example output"
Asking qwen2.5:7b-instruct via http://localhost:11434...

Your notes identify three preferred mills for suiting cloth, with a
strong preference for high-twist worsteds for travel...

Sources:
  [1] fabric-sourcing.md   notes/work/tailoring/fabric-sourcing.md
  [2] mills-shortlist.md    notes/work/tailoring/mills-shortlist.md
```

## How it works

```mermaid
flowchart LR
    q["Your question"] --> embed["Embed query"]
    embed --> retrieve["Retrieve top-k chunks<br/>from Qdrant"]
    retrieve --> prompt["Build grounded prompt"]
    prompt --> llm["Ollama (local LLM)"]
    llm --> answer["Streamed answer<br/>+ citations"]
```

The system prompt instructs the model to **answer using only the provided
context** and not to invent facts &mdash; so answers stay grounded in your notes.

## Useful flags

```bash
# Retrieve more context chunks (default 6)
uv run mimir chat "..." --k 10

# Hide the sources list
uv run mimir chat "..." --no-sources
```

See the [CLI reference](../reference/cli.md#chat) for the full list.

## Choosing a model

Any chat model available to Ollama works. Set it with `MIMIR_OLLAMA_MODEL`:

```env
MIMIR_OLLAMA_MODEL=llama3.1:8b-instruct-q8_0
```

Larger models give better synthesis at the cost of speed and memory. The default
`qwen2.5:7b-instruct` is a good balance on a 16&nbsp;GB+ Mac.

!!! warning "Ollama not running?"
    If `chat` errors out, make sure the daemon is up (`ollama serve`) and the
    model is pulled (`ollama pull <model>`). `query` works without Ollama &mdash;
    only `chat` needs it.
