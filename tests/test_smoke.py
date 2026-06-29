"""Smoke test: every module imports cleanly without a running Qdrant."""

from __future__ import annotations


def test_imports():
    import mimir
    import mimir.chat
    import mimir.chunking
    import mimir.cli
    import mimir.config
    import mimir.db
    import mimir.embeddings
    import mimir.ingest
    import mimir.loaders
    import mimir.query  # noqa: F401


def test_cli_has_all_commands():
    import mimir.cli

    # Typer's app stores registered commands here
    names = {
        cmd.name or cmd.callback.__name__ for cmd in mimir.cli.app.registered_commands
    }
    expected = {"version", "status", "ingest", "query", "chat", "reset", "watch"}
    assert expected.issubset(names), f"missing commands: {expected - names}"
