.PHONY: check reset
check:
	python3 -I tests/test_openapi.py
	node --test tests/api.test.mjs
reset:
	python3 -I tools/reset.py
