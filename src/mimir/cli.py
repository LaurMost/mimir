"""Mimir CLI."""

from __future__ import annotations

import subprocess
from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from mimir import __version__
from mimir.chat import stream_answer
from mimir.config import settings
from mimir.db import collection_info, drop_collection, get_client
from mimir.ingest import ingest_path
from mimir.query import search

app = typer.Typer(
    name="mimir",
    help="Local second brain — Qdrant + fastembed + Ollama.",
    no_args_is_help=True,
    add_completion=False,
)
console = Console()


@app.command()
def version():
    """Show Mimir version."""
    console.print(f"Mimir v{__version__}")


@app.command()
def status():
    """Show collection stats and current configuration."""
    info = collection_info()

    t = Table(title="Mimir", show_header=False, box=None)
    t.add_column(style="cyan", no_wrap=True)
    t.add_column()
    t.add_row("Qdrant URL", settings.qdrant_url)
    t.add_row("Collection", settings.collection)
    t.add_row("Embed model", settings.embed_model)
    t.add_row("Vector size", str(settings.vector_size))
    t.add_row("Chunk size / overlap", f"{settings.chunk_size} / {settings.chunk_overlap}")
    t.add_row("Notes dir", str(settings.notes_dir))

    if info is None:
        t.add_row("Status", "[yellow]collection does not exist yet[/yellow]")
    else:
        count = get_client().count(settings.collection).count
        t.add_row("Points indexed", f"[green]{count:,}[/green]")
        t.add_row("Vectors config", str(info.config.params.vectors))

    console.print(t)


@app.command()
def ingest(
    path: Path | None = typer.Argument(None, help="Path to ingest. Defaults to MIMIR_NOTES_DIR."),
    force: bool = typer.Option(False, "--force", "-f", help="Re-embed even unchanged files."),
):
    """Walk PATH, chunk, embed, and upsert into Qdrant."""
    root = path or settings.notes_dir
    console.print(f"[bold]Ingesting[/bold] {root.resolve()}")
    stats = ingest_path(root, force=force)
    t = Table(show_header=False, box=None)
    t.add_column(style="cyan")
    t.add_column(justify="right")
    t.add_row("Files seen", str(stats["files_seen"]))
    t.add_row("Files indexed", f"[green]{stats['files_indexed']}[/green]")
    t.add_row("Files skipped (unchanged)", f"[dim]{stats['files_skipped']}[/dim]")
    t.add_row("Chunks upserted", f"[green]{stats['chunks_upserted']}[/green]")
    console.print(t)


@app.command()
def query(
    text: str = typer.Argument(..., help="Search query."),
    k: int = typer.Option(5, "--k", "-k", help="Number of results."),
    folder: str | None = typer.Option(None, "--folder", help="Filter by folder."),
    ext: str | None = typer.Option(None, "--ext", help="Filter by extension, e.g. .md"),
    title: str | None = typer.Option(None, "--title", help="Filter by exact file title."),
    full: bool = typer.Option(False, "--full", help="Show full chunk text (no truncation)."),
):
    """Semantic search across your notes."""
    hits = search(text, k=k, folder=folder, ext=ext, title=title)
    if not hits:
        console.print("[yellow]No results.[/yellow]")
        return
    for i, h in enumerate(hits, 1):
        body_text = h.text if full else (h.text[:900] + ("…" if len(h.text) > 900 else ""))
        body = Text(body_text)
        header = f"[{i}] {h.title}  ·  {h.folder}  ·  score={h.score:.3f}"
        console.print(Panel(body, title=header, subtitle=h.path, border_style="cyan"))


@app.command()
def chat(
    text: str = typer.Argument(..., help="Your question."),
    k: int = typer.Option(6, "--k", "-k", help="Number of context chunks to retrieve."),
    show_sources: bool = typer.Option(True, "--sources/--no-sources"),
):
    """Ask Mimir using retrieval-augmented generation (requires Ollama running)."""
    console.print(f"[dim]Asking {settings.ollama_model} via {settings.ollama_url}...[/dim]\n")
    sources = []
    try:
        for token, hits in stream_answer(text, k=k):
            sources = hits
            console.print(token, end="", soft_wrap=True, highlight=False)
    except Exception as e:
        console.print(f"\n[red]Ollama error:[/red] {e}")
        console.print(
            "[yellow]Is Ollama running? Try: [bold]ollama serve[/bold] "
            "and [bold]ollama pull "
            f"{settings.ollama_model}[/bold][/yellow]"
        )
        raise typer.Exit(1) from e
    console.print()

    if show_sources and sources:
        console.print("\n[bold]Sources:[/bold]")
        for i, h in enumerate(sources, 1):
            console.print(f"  [{i}] [cyan]{h.title}[/cyan]  [dim]{h.path}[/dim]")


@app.command()
def reset(
    yes: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation."),
):
    """Drop and recreate the collection. All embeddings are deleted."""
    if not yes:
        confirm = typer.confirm(
            f"This will delete the '{settings.collection}' collection. Continue?"
        )
        if not confirm:
            raise typer.Abort()
    drop_collection()
    console.print(f"[green]Collection '{settings.collection}' dropped.[/green]")
    console.print("Run [bold]mimir ingest[/bold] to rebuild.")


@app.command()
def watch(
    path: Path | None = typer.Argument(None, help="Path to watch. Defaults to MIMIR_NOTES_DIR."),
):
    """Re-ingest whenever files change (requires `fswatch`)."""
    root = path or settings.notes_dir
    if not _which("fswatch"):
        console.print(
            "[red]fswatch not found.[/red] Install with: [bold]brew install fswatch[/bold]"
        )
        raise typer.Exit(1)

    console.print(f"[bold]Watching[/bold] {root.resolve()}  (Ctrl-C to stop)")
    # Initial ingest
    ingest_path(root)
    try:
        proc = subprocess.Popen(
            ["fswatch", "-o", "--latency=2", str(root)],
            stdout=subprocess.PIPE,
        )
        assert proc.stdout is not None
        for _ in iter(proc.stdout.readline, b""):
            console.print("[dim]change detected — reingesting[/dim]")
            ingest_path(root)
    except KeyboardInterrupt:
        console.print("\n[dim]stopped[/dim]")


def _which(cmd: str) -> bool:
    from shutil import which

    return which(cmd) is not None


if __name__ == "__main__":
    app()
