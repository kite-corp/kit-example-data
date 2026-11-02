"""OpenAPI coverage checks (stdlib only)."""

from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OPENAPI = ROOT / "api" / "openapi.yaml"

# Paths served by api/server.mjs (OpenAPI path templates).
EXPECTED_PATHS = [
    "/v1/orders/{order_id}",
    "/v1/stock/{category}",
    "/v1/slots/{day}",
    "/v1/bookings/{booking_id}",
    "/v1/loyalty/{member_id}",
    "/v1/orders/{order_id}/eta",
    "/v1/orders/{order_id}/track",
    "/v1/orders/{order_id}/pass",
    "/v1/members/{member_id}/notifications",
    "/v1/sales/{date}/{part}",
    "/v1/calendar/{month}",
    "/v1/times/{date}",
    "/v1/bookings/{booking_id}/status",
    "/v1/bookings/{booking_id}/pass",
    "/v1/clinic/{week}/{part}",
    "/v1/invoices/{invoice_id}",
    "/v1/invoices/{invoice_id}/claim",
    "/v1/menu",
    "/v1/menu/{category}",
    "/v1/orders",
    "/v1/bookings",
    "/reset",
]


class TestOpenApi(unittest.TestCase):
    def test_paths_in_openapi(self) -> None:
        spec = OPENAPI.read_text(encoding="utf-8")
        missing = [p for p in EXPECTED_PATHS if p not in spec]
        self.assertEqual(missing, [], f"missing paths: {missing}")

    def test_operation_ids_unique(self) -> None:
        spec = OPENAPI.read_text(encoding="utf-8")
        ids = re.findall(r"^\s+operationId:\s+(\S+)\s*$", spec, re.MULTILINE)
        self.assertEqual(len(ids), len(set(ids)), f"duplicate operationIds: {ids}")


if __name__ == "__main__":
    unittest.main()
