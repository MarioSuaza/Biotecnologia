preview:
    make run

render:
    make build

check:
    make check

publish: render check
    quarto publish gh-pages --no-prompt --no-browser --no-render
