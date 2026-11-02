"""CSV, SVG, access entries, and CSV generator tests (milestone D1)."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GOOD = ROOT / "csv" / "good"
BAD = ROOT / "csv" / "bad"
ASSETS = ROOT / "assets"
ACCESS = ROOT / "access"
TOOLS = ROOT / "tools"


class _LfMixin:
    def assert_lf_only(self, text: str) -> None:
        self.assertNotIn("\r", text, msg="expected LF line endings only")


class GoodCsvTests(_LfMixin, unittest.TestCase):
    def test_menu_items_headers_and_parse(self) -> None:
        path = GOOD / "menu_items.csv"
        self.assertTrue(path.is_file())
        text = path.read_text(encoding="utf-8")
        self.assert_lf_only(text)
        with path.open(encoding="utf-8", newline="") as fh:
            rows = list(csv.reader(fh))
        self.assertEqual(rows[0], ["name", "category", "price", "vegan", "gluten_free"])
        self.assertGreater(len(rows), 1)

    def test_treatments_headers_and_parse(self) -> None:
        path = GOOD / "treatments.csv"
        with path.open(encoding="utf-8", newline="") as fh:
            rows = list(csv.reader(fh))
        self.assertEqual(rows[0], ["name", "price", "from_price", "minutes"])
        self.assertGreater(len(rows), 1)

    def test_stock_today_headers_and_parse(self) -> None:
        path = GOOD / "stock_today.csv"
        with path.open(encoding="utf-8", newline="") as fh:
            rows = list(csv.reader(fh))
        self.assertEqual(rows[0], ["category", "item", "left", "price"])
        self.assertGreater(len(rows), 1)

    def test_slots_week_headers_and_parse(self) -> None:
        path = GOOD / "slots_week.csv"
        with path.open(encoding="utf-8", newline="") as fh:
            rows = list(csv.reader(fh))
        self.assertEqual(rows[0], ["day", "time", "minutes", "chair"])
        self.assertGreater(len(rows), 1)


class BadCsvTests(unittest.TestCase):
    def test_bad_utf8(self) -> None:
        path = BAD / "bad-utf8.csv"
        raw = path.read_bytes()
        with self.assertRaises(UnicodeDecodeError):
            raw.decode("utf-8")

    def test_wrong_types(self) -> None:
        path = BAD / "wrong-types.csv"
        with path.open(encoding="utf-8", newline="") as fh:
            rows = list(csv.reader(fh))
        self.assertGreater(len(rows), 1)
        price_idx = rows[0].index("price")
        bad = False
        for row in rows[1:]:
            if len(row) > price_idx and row[price_idx] and not row[price_idx].replace(".", "", 1).isdigit():
                bad = True
                break
        self.assertTrue(bad, msg="expected non-numeric text in a price column")

    def test_formula_cells(self) -> None:
        path = BAD / "formula-cells.csv"
        with path.open(encoding="utf-8", newline="") as fh:
            rows = list(csv.reader(fh))
        risky = "=+@-"
        found = any(cell and cell[0] in risky for row in rows for cell in row)
        self.assertTrue(found, msg="expected formula-like cell starters")

    def test_ragged_rows(self) -> None:
        path = BAD / "ragged-rows.csv"
        with path.open(encoding="utf-8", newline="") as fh:
            rows = list(csv.reader(fh))
        widths = {len(r) for r in rows if r}
        self.assertGreater(len(widths), 1, msg="expected inconsistent column counts")

    def test_bom(self) -> None:
        path = BAD / "bom.csv"
        self.assertTrue(path.read_bytes().startswith(b"\xef\xbb\xbf"))

    def test_empty(self) -> None:
        path = BAD / "empty.csv"
        self.assertEqual(path.stat().st_size, 0)

    def test_make_bad_csv_writes_large_files(self) -> None:
        script = TOOLS / "make_bad_csv.py"
        self.assertTrue(script.is_file())
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            subprocess.run(
                [sys.executable, str(script), str(out)],
                check=True,
                cwd=ROOT,
            )
            long_line = out / "long-line.csv"
            over = out / "over-10mb.csv"
            self.assertTrue(long_line.is_file())
            self.assertTrue(over.is_file())
            self.assertGreaterEqual(long_line.stat().st_size, 5 * 1024 * 1024)
            self.assertLessEqual(long_line.read_bytes().count(b"\n"), 1)
            self.assertGreater(over.stat().st_size, 10 * 1024 * 1024)


class SvgTests(unittest.TestCase):
    SVG_PATHS = [
        ASSETS / "cafe" / "flat-white.svg",
        ASSETS / "cafe" / "croissant.svg",
        ASSETS / "cafe" / "banana-bread.svg",
        ASSETS / "cafe" / "storefront.svg",
        ASSETS / "clinic" / "chair.svg",
        ASSETS / "clinic" / "tooth.svg",
        ASSETS / "clinic" / "room.svg",
        ASSETS / "clinic" / "storefront.svg",
    ]

    def test_svgs_exist_safe_and_small(self) -> None:
        on_attr = re.compile(r"\son[a-z]+\s*=", re.IGNORECASE)
        for path in self.SVG_PATHS:
            with self.subTest(path=path.relative_to(ROOT)):
                self.assertTrue(path.is_file())
                raw = path.read_text(encoding="utf-8")
                self.assertLess(path.stat().st_size, 4 * 1024)
                self.assertNotIn("<script", raw.lower())
                self.assertIsNone(
                    re.search(r"href\s*=\s*[\"']?http", raw, re.IGNORECASE),
                    msg="external href not allowed",
                )
                self.assertIsNone(on_attr.search(raw))
                self.assertIn('viewBox="0 0 96 96"', raw)
                self.assertRegex(raw, r"<title>[^<]+</title>")


class MakeBigCsvTests(unittest.TestCase):
    def test_make_big_csv_deterministic_100k_rows(self) -> None:
        script = TOOLS / "make_big_csv.py"
        self.assertTrue(script.is_file())
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "orders.csv"
            for _ in range(2):
                subprocess.run(
                    [sys.executable, str(script), str(out), "--rows", "100000"],
                    check=True,
                    cwd=ROOT,
                )
                digest = hashlib.sha256(out.read_bytes()).hexdigest()
                if _ == 0:
                    first = digest
                    with out.open(encoding="utf-8", newline="") as fh:
                        rows = list(csv.reader(fh))
                    self.assertEqual(len(rows) - 1, 100_000)
                else:
                    self.assertEqual(digest, first)


class AccessEntryTests(unittest.TestCase):
    REQUIRED_KEYS = {"name", "interface", "op", "call", "params", "doc", "examples"}

    def test_every_access_json(self) -> None:
        paths = sorted(ACCESS.glob("*.json"))
        self.assertGreaterEqual(len(paths), 8)
        for path in paths:
            with self.subTest(path=path.name):
                data = json.loads(path.read_text(encoding="utf-8"))
                self.assertEqual(set(data.keys()), self.REQUIRED_KEYS)
                self.assertGreaterEqual(len(data["examples"]), 6)
                for key in self.REQUIRED_KEYS:
                    self.assertIn(key, data)


if __name__ == "__main__":
    unittest.main()
