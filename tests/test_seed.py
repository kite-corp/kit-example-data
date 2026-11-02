"""Deterministic seed.sql and showcase id coverage."""
from __future__ import annotations

import json
import re
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SEED_SQL = ROOT / "db" / "seed.sql"
BUILD = ROOT / "tools" / "build_seed.py"
SHOWCASE = ROOT / "data" / "showcase.json"

REAL_EMAIL = re.compile(
    r"[a-zA-Z0-9._%+-]+@(gmail|yahoo|hotmail|outlook|icloud|proton)\.",
    re.I,
)


class TestSeedSql(unittest.TestCase):
    def test_seed_matches_fresh_build(self) -> None:
        proc = subprocess.run(
            ["nice", "-n", "19", "python3", "-I", str(BUILD)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertEqual(proc.stderr, "")
        built = (ROOT / "db" / "seed.sql").read_text(encoding="utf-8")
        committed = SEED_SQL.read_text(encoding="utf-8")
        self.assertEqual(built, committed)

    def test_no_real_looking_emails_in_seed(self) -> None:
        text = SEED_SQL.read_text(encoding="utf-8")
        self.assertIsNone(REAL_EMAIL.search(text))

    def test_showcase_order_booking_loyalty_ids_in_seed(self) -> None:
        data = json.loads(SHOWCASE.read_text(encoding="utf-8"))
        seed = SEED_SQL.read_text(encoding="utf-8")
        for order_id in data["orders"]:
            self.assertIn(order_id, seed, msg=f"missing order {order_id}")
        for booking_id in data["bookings"]:
            self.assertIn(booking_id, seed, msg=f"missing booking {booking_id}")
        for member_id in data["loyalty"]:
            self.assertIn(member_id, seed, msg=f"missing loyalty {member_id}")


if __name__ == "__main__":
    unittest.main()


def _seed_data():
    import importlib.util

    spec = importlib.util.spec_from_file_location("seed_data", ROOT / "tools" / "seed_data.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class SeedMatchesFiles(unittest.TestCase):
    def test_the_menu_csv_matches_the_seed(self):
        import csv

        sd = _seed_data()
        seed = {m["name"]: m for m in sd.MENU_ITEMS}
        rows = list(csv.DictReader((ROOT / "csv/good/menu_items.csv").open(encoding="utf-8")))
        self.assertEqual(sorted(r["name"] for r in rows), sorted(seed))
        for r in rows:
            m = seed[r["name"]]
            self.assertEqual(round(float(r["price"]) * 100), m["price_cents"], r["name"])
            self.assertEqual(r["vegan"] == "true", m["vegan"], r["name"])
            self.assertEqual(r["gluten_free"] == "true", m["gluten_free"], r["name"])

    def test_order_totals_are_the_sum_of_their_lines_and_match_the_showcase(self):
        sd = _seed_data()
        showcase = json.loads((ROOT / "data/showcase.json").read_text(encoding="utf-8"))
        for o in sd.ORDERS:
            lines = sum(i["price_cents"] * i.get("qty", 1) for i in sd.ORDER_ITEMS if i["order_id"] == o["id"])
            self.assertEqual(lines, o["total_cents"], o["id"])
            if o["id"] in showcase["orders"]:
                self.assertEqual(showcase["orders"][o["id"]]["Total"], f"${o['total_cents'] / 100:.2f}")
