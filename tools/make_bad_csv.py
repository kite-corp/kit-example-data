#!/usr/bin/env python3
"""Write oversized bad CSV fixtures to a directory (not committed)."""

from __future__ import annotations

import argparse
from pathlib import Path

FIVE_MB = 5 * 1024 * 1024
TEN_MB = 10 * 1024 * 1024 + 1


def write_long_line(path: Path) -> None:
    # One CSV row, file size at least 5 MiB, single newline at EOF.
    body = "a," + ("x" * (FIVE_MB - 3))
    path.write_text(body + "\n", encoding="utf-8", newline="\n")


def write_over_limit(path: Path) -> None:
    chunk = "row,data\n" * 200_000
    data = chunk
    while len(data.encode("utf-8")) <= TEN_MB:
        data += chunk
    path.write_text(data, encoding="utf-8", newline="\n")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("out_dir", type=Path, help="Directory for long-line.csv and over-10mb.csv")
    args = parser.parse_args()
    out_dir = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    write_long_line(out_dir / "long-line.csv")
    write_over_limit(out_dir / "over-10mb.csv")


if __name__ == "__main__":
    main()
