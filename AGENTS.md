# AGENTS.md: kit-example-data

Owns: invented sample data for Kit examples and tests. Product type data. Allowed kit-* dependencies: none.

## Rules
- Invented data only. No real people, no secrets, no tokens.
- No dependencies: Python 3.12 stdlib and Node 22 built-ins only.
- Loopback ports 18700-18709 only. The API binds 127.0.0.1.
- Fixed ids and dates: `make reset` twice gives the same row hashes.
- Test first. No file over 800 lines (generated big files are made by a script, not committed).
- Use `nice -n 19` for every command. Never read `.env`. Never print secrets.
- Push only feature branches. Only Kit Builder fast-forwards dev.
