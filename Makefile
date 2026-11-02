.PHONY: check reset
check:
	python3 -I -m unittest discover -s tests -t . -v
	node --test tests/
reset:
	python3 -I tools/reset.py
