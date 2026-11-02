#!/usr/bin/env python3
"""Write a deterministic large orders CSV for import stress tests."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

HEADER = ["order_id", "line_no", "sku", "qty", "unit_price", "line_total", "status"]


def row_values(n: int) -> list[str]:
    """Derive one data row from 1-based row index n (no randomness)."""
    order_num = 2000 + (n % 9000)
    order_id = f"K-{order_num}"
    line_no = str((n % 5) + 1)
    sku = f"SKU-{(n % 24):02d}"
    qty = str((n % 3) + 1)
    unit_cents = 320 + (n % 17) * 10
    unit_price = f"{unit_cents / 100:.2f}"
    line_total = f"{int(qty) * unit_cents / 100:.2f}"
    statuses = ["Received", "Being made", "Ready on the shelf", "Cancelled"]
    status = statuses[n % len(statuses)]
    return [order_id, line_no, sku, qty, unit_price, line_total, status]


def write_csv(path: Path, rows: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh, lineterminator="\n")
        writer.writerow(HEADER)
        for i in range(1, rows + 1):
            writer.writerow(row_values(i))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("out", type=Path, help="Output CSV path")
    parser.add_argument("--rows", type=int, default=100_000, help="Number of data rows")
    args = parser.parse_args()
    if args.rows < 1:
        raise SystemExit("--rows must be at least 1")
    write_csv(args.out, args.rows)


if __name__ == "__main__":
    main()
