"""QMD editable -> notebook descargable y copia JupyterLite. Nunca ejecuta celdas."""
from copy import deepcopy
from pathlib import Path
import hashlib
import os
import re
import subprocess
import sys
import tempfile

import nbformat
import yaml

ROOT = Path(__file__).resolve().parents[1]
FRONT_MATTER = re.compile(r"\A---\s*\n(.*?)\n---\s*(?:\n|$)", re.DOTALL)


def write_notebook(path, notebook):
    text = nbformat.writes(notebook) + "\n"
    if not path.exists() or path.read_text() != text:
        path.write_text(text)


def generate():
    sources = sorted((ROOT / "src/03_practicas").glob("practica-*.qmd"))
    if not sources:
        raise ValueError("No se han encontrado prácticas QMD")
    stems = {source.stem for source in sources}
    downloads = ROOT / "downloads"
    lite = ROOT / "build/lite-content"
    for folder in (downloads, lite):
        folder.mkdir(parents=True, exist_ok=True)
        for path in folder.glob("practica-*.ipynb"):
            if path.stem not in stems:
                path.unlink()
    env = dict(os.environ, QUARTO_PYTHON=sys.executable)
    with tempfile.TemporaryDirectory(prefix="convert-", dir=ROOT / "build") as temp:
        for source in sources:
            front_matter = FRONT_MATTER.match(source.read_text())
            if not front_matter:
                raise ValueError(f"Falta el título YAML de {source.name}")
            title = yaml.safe_load(front_matter.group(1)).get("title")
            if not isinstance(title, str) or not title.strip():
                raise ValueError(f"Título inválido en {source.name}")
            converted = Path(temp) / source.with_suffix(".ipynb").name
            subprocess.run(
                ["quarto", "convert", str(source), "--output", str(converted), "--quiet"],
                check=True, cwd=ROOT, env=env,
            )
            notebook = nbformat.read(converted, as_version=4)
            # El YAML de Quarto se sustituye por un título legible para el estudiante.
            if notebook.cells and notebook.cells[0].cell_type == "markdown":
                notebook.cells[0].source = FRONT_MATTER.sub("", notebook.cells[0].source).lstrip()
                if not notebook.cells[0].source:
                    notebook.cells.pop(0)
            notebook.cells.insert(0, nbformat.v4.new_markdown_cell(f"# {title}"))
            notebook.nbformat_minor = 5
            notebook.metadata["kernelspec"] = {
                "name": "python3", "display_name": "Python 3", "language": "python",
            }
            notebook.metadata["language_info"] = {"name": "python"}
            notebook.metadata["quarto_source"] = {
                "path": source.relative_to(ROOT).as_posix(),
                "sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
            }
            for index, cell in enumerate(notebook.cells):
                cell["id"] = f"{source.stem}-cell-{index:02d}"
                if cell.cell_type == "code":
                    cell.execution_count = None
                    cell.outputs = []
            nbformat.validate(notebook)
            write_notebook(downloads / converted.name, notebook)
            browser_notebook = deepcopy(notebook)
            browser_notebook.metadata["kernelspec"] = {
                "name": "python", "display_name": "Python (Pyodide)", "language": "python",
            }
            write_notebook(lite / converted.name, browser_notebook)
    print(f"Notebooks generados desde QMD, sin ejecución: {len(sources)}.")


if __name__ == "__main__":
    generate()
