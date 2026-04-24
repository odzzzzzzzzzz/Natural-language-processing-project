from __future__ import annotations

from pathlib import Path
from typing import Iterator
import re


def _normalize_text(text: str) -> str:
    """Clean opinion text while preserving paragraph boundaries."""
    # remove form-feed characters
    text = text.replace("\f", "")

    # normalize unicode dashes/quotes/spaces to simpler forms
    text = text.replace("\u00a0", " ")   # non-breaking space
    text = text.replace("\u2013", "-")   # en dash
    text = text.replace("\u2014", "-")   # em dash
    text = text.replace("\u2018", "'")
    text = text.replace("\u2019", "'")
    text = text.replace("\u201c", '"')
    text = text.replace("\u201d", '"')

    # remove isolated page markers like "*783" or "* 783"
    text = re.sub(r"\*(\s*)\d+\b", "", text)

    # remove bracketed footnote markers like [*], [1], [12]
    text = re.sub(r"\[(\*|\d+)\]", "", text)

    # clean trailing spaces on each line
    lines = [line.rstrip() for line in text.splitlines()]

    # collapse excessive internal spaces/tabs but preserve line breaks
    cleaned_lines = []
    for line in lines:
        line = re.sub(r"[ \t]+", " ", line).strip()
        cleaned_lines.append(line)

    text = "\n".join(cleaned_lines)

    # collapse 3+ blank lines to 2 blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def list_opinions(raw_dir: str) -> list[str]:
    """
    Return a sorted list of base names (without extension) for all opinions in raw_dir.

    Current strategy:
    - Prefer .txt files, since they appear to be the cleanest raw-text source in our inspection.
    - Search recursively because the corpus may contain nested directories like 1K_scotus/1K_scotus/.
    """
    root = Path(raw_dir)
    if not root.exists():
        raise FileNotFoundError(f"raw_dir does not exist: {raw_dir}")

    basenames = {p.stem for p in root.rglob("*.txt")}
    return sorted(basenames)


def load_opinion_text(base_name: str, raw_dir: str) -> str:
    """
    Read the preferred text file for the given opinion and return cleaned plain text.

    Current priority:
    1. .txt
    2. .case
    3. .case8  (only as a fallback; may contain markup in some files)
    """
    root = Path(raw_dir)
    if not root.exists():
        raise FileNotFoundError(f"raw_dir does not exist: {raw_dir}")

    candidates = []
    for ext in [".txt", ".case", ".case8"]:
        candidates.extend(root.rglob(f"{base_name}{ext}"))

    if not candidates:
        raise FileNotFoundError(
            f"Could not find any text file for base name '{base_name}' under {raw_dir}"
        )

    # Prefer the first match according to extension priority
    candidates = sorted(
        candidates,
        key=lambda p: {".txt": 0, ".case": 1, ".case8": 2}.get(p.suffix, 99)
    )
    path = candidates[0]

    text = path.read_text(encoding="utf-8", errors="ignore")
    return _normalize_text(text)


def iter_paragraphs(text: str) -> Iterator[str]:
    """Yield non-empty paragraphs split on blank lines."""
    for para in re.split(r"\n\s*\n", text):
        para = para.strip()
        if para:
            yield para
