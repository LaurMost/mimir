---
title: Mimir
template: home.html
hide:
  - navigation
  - toc
---

> *"And there sat Odin, before the well, and asked counsel of the head of Mimir."*

Mimir points at a folder of notes &mdash; an Obsidian vault, loose Markdown, PDFs &mdash; chunks and embeds them into a local [Qdrant](https://qdrant.tech/) vector store, and lets you ask questions about them. Either as fast semantic search, or as a full retrieval-augmented answer from a local [Ollama](https://ollama.ai/) model. Nothing leaves your machine.

<div class="mimir-grid" markdown>

<div class="mimir-card" markdown>
### :material-shield-lock: Local-first &amp; private
Runs entirely on your machine. No API keys, no cloud, no tokens leaving your Mac.
</div>

<div class="mimir-card" markdown>
### :material-magnify: Semantic search
Top-k search across `.md`, `.pdf`, `.txt`, and more &mdash; with rich previews and filters.
</div>

<div class="mimir-card" markdown>
### :material-message-text: RAG chat
Ask questions and get answers grounded in your own notes, with citations back to the source.
</div>

<div class="mimir-card" markdown>
### :material-flash: Native Apple Silicon
Embeddings via fastembed (`BAAI/bge-small-en-v1.5`, ONNX) &mdash; fast, no GPU required.
</div>

<div class="mimir-card" markdown>
### :material-sync: Incremental ingest
Re-ingesting skips unchanged files automatically via per-file SHA-256 hashing.
</div>

<div class="mimir-card" markdown>
### :material-tune: Swappable models
Change the embedding model or LLM with a single `.env` value.
</div>

</div>

## Where to next

<div class="grid cards" markdown>

-   :material-rocket-launch: __[Quickstart](getting-started/quickstart.md)__

    Docker, first ingest, and your first query in five commands.

-   :material-console: __[CLI reference](reference/cli.md)__

    Every command and flag, auto-generated from the source.

-   :material-sitemap: __[Architecture](reference/architecture.md)__

    How ingest, Qdrant, query, and chat fit together.

-   :material-frequently-asked-questions: __[FAQ](faq.md)__

    Troubleshooting and common questions.

</div>
