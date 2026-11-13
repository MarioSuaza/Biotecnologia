run:
	python3 scripts/generate.py
	quarto preview --host localhost --port 7777

build:
	quarto render

check:
	python3 scripts/check.py

clean:
	python3 scripts/clean.py
