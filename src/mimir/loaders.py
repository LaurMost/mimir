"""File loaders. Add new formats here."""

from __future__ import annotations

from pathlib import Path

SUPPORTED_EXTENSIONS = {".md", ".markdown", ".txt", ".pdf", ".rst", ".org"}


def load_text(path: Path) -> str:
    """Read a file and return its text content. Raises on failure."""
    ext = path.suffix.lower()
    if ext == ".pdf":
        return _load_pdf(path)
    return path.read_text(encoding="utf-8", errors="ignore")


def _load_pdf(path: Path) -> str:
    # Lazy import — pypdf isn't needed unless you actually have PDFs.
    from pypdf import PdfReader

    reader = PdfReader(str(path))
    pages = []
    for page in reader.pages:
        try:
            pages.append(page.extract_text() or "")
        except Exception:
            continue
    return "\n\n".join(pages)


def discover_files(root: Path, pattern: str = "**/*") -> list[Path]:
    """Walk `root` and return all supported files."""
    return sorted(
        p
        for p in root.glob(pattern)
        if p.is_file() and p.suffix.lower() in SUPPORTED_EXTENSIONS
    )
