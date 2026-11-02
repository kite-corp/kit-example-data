# kit-example-data

Invented sample data for Kit examples and tests. Two businesses:

- **Kettle & Crumb**: a cafe and bakery (menu, stock, orders, loyalty).
- **Seabrook Family Dental**: a family dental clinic (dentists, treatments, slots, bookings).

No real people, places, orders or patients. No secrets. Test use only.

## Layout

| path | holds |
|---|---|
| `data/showcase.json` | view-shaped rows the showcase apps read (from kit-web `examples/try-full-flow-v3`) |
| `data/*.md` | the business facts the brains learn from |
| `db/schema.sql`, `db/seed.sql` | Postgres schema and seed, fixed ids and dates |
| `api/` | sample REST API (Node built-ins only) and `openapi.yaml`; `api/bad/` holds bad specs for tests |
| `csv/` | good and bad CSV files for import tests |
| `assets/` | small SVG images made for this repo |
| `access/` | one access entry per data call, for `kit iface feed` |
| `tools/` | seed builder, reset, big CSV generator |
| `tests/` | determinism, API and file tests |

## Ports

Loopback only, ports 18700-18709. The API listens on 18704 by default (`PORT`).

## Commands

- `make check`: all tests (`python3 -m unittest` and `node --test`).
- `npx @redocly/cli@1.34.0 lint api/openapi.yaml`: OpenAPI lint (recommended rules), clean.
- `make reset`: drop and reseed the `kitexample` database (`PGHOST`, `PGPORT`, `PGUSER` from the env).

Used by: the Kit data gateway tests, the shell data modules, `kit-example-web/-ios/-android`, the try-it showcase.
