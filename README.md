# SchConvTest

`SchConvTest` provides a small CLI utility that reads a schematic PDF and emits a structured JSON summary.

## What is implemented

- Python package scaffold with `src/` and `tests/`.
- `schconv` CLI that accepts a PDF input path and emits JSON.
- PDF parsing using `pypdf`:
  - Page count
  - Per-page word counts
  - Best-effort page "sheet title" extraction
  - Per-page and global top terms
- Unit tests for parser heuristics and CLI behavior.

## Setup

```bash
python -m pip install -e .[dev]
```

## Usage

```bash
schconv path/to/schematic.pdf --pretty
```

Write to a file:

```bash
schconv path/to/schematic.pdf --pretty -o path/to/result.json
```

## Test

```bash
pytest
```

## Notes

The repository did not include an explicit functional specification beyond the schematic PDF, so this implementation establishes a practical MVP conversion target: PDF-to-structured-summary JSON.
