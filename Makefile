.PHONY: check reset big
check:
	python3 -m unittest discover -s tests -t . -v
	node --test tests/*.test.mjs
reset:
	python3 -I tools/reset.py
big:
	python3 -I tools/make_big_csv.py csv/big-orders.csv
