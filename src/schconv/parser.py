from __future__ import annotations

from collections import Counter
from pathlib import Path
import re

from pypdf import PdfReader

_IGNORED_TITLE_LINES = {
    "engineer",
    "author",
    "date",
    "doc#",
    "circuit",
    "rev",
    "sheet#",
    "title",
    "this page intentionally left blank",
}

_STOP_WORDS = {
    "the",
    "and",
    "for",
    "with",
    "only",
    "this",
    "that",
    "from",
    "into",
    "are",
    "page",
    "available",
    "load",
    "note",
    "variant",
}


def _clean_line(line: str) -> str:
    return re.sub(r"\s+", " ", line).strip()


def _extract_sheet_title(lines: list[str]) -> str | None:
    candidates: list[str] = []
    for raw in lines:
        line = _clean_line(raw)
        if not line:
            continue
        lower = line.lower()
        if lower in _IGNORED_TITLE_LINES:
            continue
        if line.isupper() and len(line.split()) <= 2:
            continue
        alpha = sum(char.isalpha() for char in line)
        if alpha < 7:
            continue
        if re.search(r"[a-z]", line) and len(line) <= 60:
            candidates.append(line)
    if not candidates:
        return None
    return max(candidates, key=lambda item: ("," in item, len(item.split())))


def _top_terms(lines: list[str], limit: int = 8) -> list[str]:
    counts: Counter[str] = Counter()
    for line in lines:
        for token in re.findall(r"[A-Za-z][A-Za-z0-9_/-]{2,}", line):
            normalized = token.lower()
            if normalized in _STOP_WORDS:
                continue
            counts[normalized] += 1
    return [token for token, _ in counts.most_common(limit)]


def parse_pdf(pdf_path: str | Path) -> dict:
    source = Path(pdf_path)
    reader = PdfReader(str(source))
    pages: list[dict] = []
    global_counter: Counter[str] = Counter()

    for index, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        lines = [_clean_line(line) for line in text.splitlines() if _clean_line(line)]
        terms = _top_terms(lines)
        global_counter.update(terms)
        pages.append(
            {
                "page_number": index,
                "word_count": len(text.split()),
                "sheet_title": _extract_sheet_title(lines),
                "top_terms": terms,
            }
        )

    return {
        "source_file": str(source),
        "page_count": len(reader.pages),
        "pages": pages,
        "global_terms": [token for token, _ in global_counter.most_common(20)],
    }
