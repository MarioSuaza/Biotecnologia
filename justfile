preview:
    make run

render:
    make build

check:
    make check

serve:
    make serve

publish:
    git fetch origin gh-pages
    quarto render
    python3 scripts/check.py
    quarto publish gh-pages --no-prompt --no-browser --no-render
