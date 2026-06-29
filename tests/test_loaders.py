"""Tests for mimir.loaders."""

from __future__ import annotations

from mimir.loaders import SUPPORTED_EXTENSIONS, discover_files, load_text


def test_supported_extensions():
    assert ".md" in SUPPORTED_EXTENSIONS
    assert ".txt" in SUPPORTED_EXTENSIONS
    assert ".pdf" in SUPPORTED_EXTENSIONS
    assert ".docx" not in SUPPORTED_EXTENSIONS


def test_discover_finds_supported(notes_dir):
    (notes_dir / "a.md").write_text("# A")
    (notes_dir / "b.txt").write_text("b")
    (notes_dir / "c.png").write_bytes(b"\x89PNG")
    sub = notes_dir / "sub"
    sub.mkdir()
    (sub / "d.markdown").write_text("# D")

    files = discover_files(notes_dir)
    names = {p.name for p in files}
    assert names == {"a.md", "b.txt", "d.markdown"}


def test_discover_empty_dir(notes_dir):
    assert discover_files(notes_dir) == []


def test_load_text_markdown(notes_dir):
    path = notes_dir / "note.md"
    path.write_text("# Hello\n\nWorld", encoding="utf-8")
    assert load_text(path) == "# Hello\n\nWorld"


def test_load_text_handles_bad_encoding(notes_dir):
    path = notes_dir / "weird.txt"
    path.write_bytes(b"hello \xff\xfe world")
    # Should not raise; invalid bytes are replaced
    result = load_text(path)
    assert "hello" in result
    assert "world" in result
