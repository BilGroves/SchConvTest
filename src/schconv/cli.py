from __future__ import annotations

import argparse
import json
from pathlib import Path

from .parser import parse_pdf


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="schconv",
        description="Convert a schematic PDF into a structured JSON summary.",
    )
    parser.add_argument("pdf", type=Path, help="Path to source PDF.")
    parser.add_argument("-o", "--output", type=Path, help="Write output JSON to file.")
    parser.add_argument(
        "--pretty", action="store_true", help="Pretty-print JSON output with indentation."
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = parse_pdf(args.pdf)
    payload = json.dumps(result, indent=2 if args.pretty else None)
    if args.output:
        args.output.write_text(f"{payload}\n", encoding="utf-8")
    else:
        print(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
