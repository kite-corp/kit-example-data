#!/usr/bin/env python3
"""Drop and recreate kitexample cafe/clinic schemas; print table row hashes."""
from __future__ import annotations

import hashlib
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCHEMA = ROOT / "db" / "schema.sql"
SEED = ROOT / "db" / "seed.sql"
DB_NAME = "kitexample"

TABLES: list[tuple[str, str]] = [
    ("cafe", "menu_items", "id"),
    ("cafe", "stock", "item_id, day"),
    ("cafe", "loyalty_cards", "member_id"),
    ("cafe", "orders", "id"),
    ("cafe", "order_items", "order_id, line"),
    ("clinic", "dentists", "id"),
    ("clinic", "treatments", "id"),
    ("clinic", "patients", "id"),
    ("clinic", "slots", "id"),
    ("clinic", "appointments", "id"),
]


def _env(name: str, default: str | None = None) -> str:
    value = os.environ.get(name, default)
    if value is None:
        raise SystemExit(f"missing required env var {name}")
    return value


def _allowed_host(host: str) -> bool:
    if host.startswith("/"):
        return True
    return host in {"127.0.0.1", "localhost"}


def _psql_base_env() -> dict[str, str]:
    env = os.environ.copy()
    env.pop("PGDATABASE", None)
    return env


def _psql_cmd(database: str, *args: str) -> list[str]:
    host = _env("PGHOST")
    port = _env("PGPORT")
    user = _env("PGUSER")
    return [
        "psql",
        "-h",
        host,
        "-p",
        port,
        "-U",
        user,
        "-d",
        database,
        "-v",
        "ON_ERROR_STOP=1",
        *args,
    ]


def _run(cmd: list[str], env: dict[str, str] | None = None) -> None:
    subprocess.run(
        ["nice", "-n", "19", *cmd],
        check=True,
        env=env or os.environ.copy(),
    )


def _ensure_database() -> None:
    env = _psql_base_env()
    check = subprocess.run(
        ["nice", "-n", "19", *_psql_cmd("postgres", "-tAc", f"SELECT 1 FROM pg_database WHERE datname = '{DB_NAME}'")],
        capture_output=True,
        text=True,
        env=env,
    )
    if check.returncode != 0:
        raise SystemExit(check.stderr.strip() or "psql failed checking database")
    if check.stdout.strip() != "1":
        _run(_psql_cmd("postgres", "-c", f"CREATE DATABASE {DB_NAME}"), env=env)


def _reset_schemas() -> None:
    sql = (
        f"DROP SCHEMA IF EXISTS cafe CASCADE;\n"
        f"DROP SCHEMA IF EXISTS clinic CASCADE;\n"
    )
    _run(_psql_cmd(DB_NAME, "-c", sql), env=_psql_base_env())
    _run(_psql_cmd(DB_NAME, "-f", str(SCHEMA)), env=_psql_base_env())
    _run(_psql_cmd(DB_NAME, "-f", str(SEED)), env=_psql_base_env())


def _table_sha256(schema: str, table: str, order_cols: str) -> str:
    query = f"""
SELECT coalesce(string_agg(md5(t::text), E'\\n' ORDER BY {order_cols}), '')
FROM {schema}.{table} t;
"""
    proc = subprocess.run(
        ["nice", "-n", "19", *_psql_cmd(DB_NAME, "-tAc", query)],
        capture_output=True,
        text=True,
        check=True,
        env=_psql_base_env(),
    )
    payload = proc.stdout.rstrip("\n")
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def main() -> None:
    pgdatabase = os.environ.get("PGDATABASE")
    if pgdatabase is not None and pgdatabase != DB_NAME:
        raise SystemExit(
            f"refusing to run: PGDATABASE={pgdatabase!r} (must be unset or {DB_NAME!r})"
        )

    host = _env("PGHOST")
    if not _allowed_host(host):
        raise SystemExit(f"refusing to run: PGHOST={host!r} is not local")

    if not SCHEMA.is_file() or not SEED.is_file():
        raise SystemExit("missing db/schema.sql or db/seed.sql")

    _ensure_database()
    _reset_schemas()

    for schema, table, order_cols in TABLES:
        digest = _table_sha256(schema, table, order_cols)
        print(f"{schema}.{table}: {digest}")


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as exc:
        sys.stderr.write(exc.stderr or str(exc))
        raise SystemExit(exc.returncode) from exc
