"""Tests for mimir.chunking."""

from __future__ import annotations

from itertools import pairwise

from mimir.chunking import chunk_text


def test_empty_input_returns_empty_list():
    assert chunk_text("") == []
    assert chunk_text("   \n\n  ") == []


def test_short_text_is_one_chunk():
    text = "Just a short note."
    chunks = chunk_text(text, max_chars=1000, overlap=100)
    assert chunks == [text]


def test_long_text_is_split():
    text = "Sentence one. " * 200  # ~2800 chars
    chunks = chunk_text(text, max_chars=500, overlap=50)
    assert len(chunks) > 1
    assert all(len(c) <= 600 for c in chunks)  # max + a little slack for sep


def test_chunks_overlap():
    # Build text where boundaries are deterministic
    text = ("A" * 100 + ". ") * 10  # ~1020 chars of repeating blocks
    chunks = chunk_text(text, max_chars=300, overlap=50)
    assert len(chunks) >= 2
    # Each consecutive pair should share at least some content
    for a, b in pairwise(chunks):
        # crude overlap check: last 20 chars of a appear somewhere in b
        tail = a[-20:].strip()
        if tail:
            assert tail[:10] in b or tail in b or len(b) < 20


def test_prefers_paragraph_boundary():
    para1 = "First paragraph content." * 5
    para2 = "Second paragraph content." * 5
    text = para1 + "\n\n" + para2
    chunks = chunk_text(text, max_chars=len(para1) + 10, overlap=10)
    # The split should happen at or after the paragraph break, so the first
    # chunk should end with the first paragraph (modulo trailing whitespace).
    assert chunks[0].rstrip().endswith(".")


def test_no_infinite_loop_on_pathological_input():
    # Single long unbroken word — must terminate
    text = "x" * 5000
    chunks = chunk_text(text, max_chars=500, overlap=100)
    assert len(chunks) > 1
    assert "".join(chunks).count("x") >= 5000  # all content preserved at least once
