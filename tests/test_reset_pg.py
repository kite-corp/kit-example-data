"""Postgres reset determinism when KITEXAMPLE_PG=1."""
from __future__ import annotations

import os
import re
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RESET = ROOT / "tools" / "reset.py"

HASH_LINE = re.compile(r"^(?:cafe|clinic)\.\w+: ([0-9a-f]{64})$")


def _run_reset(env: dict[str, str]) -> dict[str, str]:
    proc = subprocess.run(
        ["nice", "-n", "19", "python3", "-I", str(RESET)],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        check=True,
    )
    hashes: dict[str, str] = {}
    for line in proc.stdout.splitlines():
        m = HASH_LINE.match(line.strip())
        if m:
            table = line.split(":")[0].strip()
            hashes[table] = m.group(1)
    return hashes


@unittest.skipUnless(os.environ.get("KITEXAMPLE_PG") == "1", "set KITEXAMPLE_PG=1")
class TestResetPostgres(unittest.TestCase):
    def test_reset_twice_same_table_hashes(self) -> None:
        env = os.environ.copy()
        env.setdefault("PGHOST", "/workspace/jobs/databuild/pg")
        env.setdefault("PGPORT", "18709")
        env.setdefault("PGUSER", "kitexample")
        env.pop("PGDATABASE", None)
        first = _run_reset(env)
        second = _run_reset(env)
        self.assertTrue(first, "reset produced no hash lines")
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()


class ResetRefuses(unittest.TestCase):
    def _run(self, **env):
        import subprocess
        import sys

        full = {k: v for k, v in os.environ.items() if not k.startswith("PG")}
        full.update(env)
        return subprocess.run(
            [sys.executable, "-I", str(ROOT / "tools" / "reset.py")],
            env=full, capture_output=True, text=True, timeout=30,
        )

    def test_a_remote_host_is_refused(self):
        out = self._run(PGHOST="203.0.113.1", PGPORT="5432", PGUSER="x")
        self.assertNotEqual(out.returncode, 0)
        self.assertIn("not local", out.stdout + out.stderr)

    def test_another_database_is_refused(self):
        out = self._run(PGHOST="127.0.0.1", PGPORT="5432", PGUSER="x", PGDATABASE="postgres")
        self.assertNotEqual(out.returncode, 0)
        self.assertIn("refusing", out.stdout + out.stderr)
