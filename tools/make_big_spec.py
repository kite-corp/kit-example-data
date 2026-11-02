#!/usr/bin/env python3
"""Write a large OpenAPI document to the path given on the command line (not committed)."""

from __future__ import annotations

import sys

TARGET_BYTES = 50 * 1024 * 1024
CHUNK = (
    "  /v1/generated/{id}:\n"
    "    get:\n"
    "      operationId: gen_{id}\n"
    "      responses:\n"
    '        "200":\n'
    "          description: filler\n"
)


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: make_big_spec.py OUTPUT_PATH", file=sys.stderr)
        return 2
    out = sys.argv[1]
    header = "openapi: 3.1.0\ninfo:\n  title: big\n  version: 1.0.0\npaths:\n"
    footer = "\n"
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(header)
        written = len(header.encode("utf-8"))
        i = 0
        while written < TARGET_BYTES - len(footer.encode("utf-8")):
            block = CHUNK.format(id=i)
            fh.write(block)
            written += len(block.encode("utf-8"))
            i += 1
        fh.write(footer)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
