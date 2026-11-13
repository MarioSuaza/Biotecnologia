run:
	quarto preview --host localhost --port 7777

build:
	quarto render

check:
	python3 scripts/check.py

serve:
	python3 -m http.server 8000 --directory _output --bind 127.0.0.1

clean:
	python3 scripts/clean.py
