"""Notebook canónico -> página Quarto, descarga y copia JupyterLite. Sin ejecución."""
from pathlib import Path
import json
import shutil

ROOT = Path(__file__).resolve().parents[1]

def generate():
    pages = ROOT / "src/03_practicas"
    pages.mkdir(parents=True, exist_ok=True)
    stems = {path.stem for path in (ROOT / "notebooks").glob("practica-*.ipynb")}
    for folder in (pages, ROOT / "downloads", ROOT / "build/lite-content"):
        folder.mkdir(parents=True, exist_ok=True)
        for path in folder.glob("practica-*." + ("qmd" if folder == pages else "ipynb")):
            if path.stem not in stems:
                path.unlink()
    for path in sorted((ROOT / "notebooks").glob("practica-*.ipynb")):
        nb = json.loads(path.read_text())
        for cell in nb["cells"]:
            if cell["cell_type"] == "code" and (cell["outputs"] or cell["execution_count"] is not None):
                raise ValueError(f"Limpia las salidas antes de distribuir {path.name}")
        title = "".join(nb["cells"][0]["source"]).strip().removeprefix("# ")
        lines = [f'---\ntitle: "{title}"\nformat: html\nexecute:\n  enabled: false\n---\n',
                 f'<a class="btn btn-primary" href="../../downloads/{path.name}" download="{path.name}">Descargar notebook de Jupyter</a>\n',
                 f'<a class="btn btn-outline-primary" href="../../lite/lab/index.html?path={path.name}" target="_blank" rel="noopener">Abrir en el navegador</a>\n',
                 '::: {.callout-note title="Dónde ejecutar el código"}\n'
                 'Esta página muestra las instrucciones y el código, pero no ejecuta Python. '
                 'Pulsa **Abrir en el navegador** para editar y ejecutar las celdas en JupyterLite, '
                 'o descarga el notebook y ábrelo en Jupyter o VS Code.\n\n'
                 'En JupyterLite espera a que el kernel **Python (Pyodide)** esté listo. '
                 'Después de cambiar tu respuesta, usa **Run → Run All Cells** para actualizar '
                 'la función y las pruebas en orden. Los resultados aparecen debajo de la celda de tests. '
                 'Descarga tu copia de trabajo para conservarla fuera del navegador.\n:::\n']
        for cell in nb["cells"][1:]:
            source = "".join(cell["source"])
            if cell["cell_type"] == "markdown":
                lines.append(source)
            elif cell["cell_type"] == "code":
                # Un bloque ordinario presenta el ejercicio sin ejecutarlo durante el render.
                fence = "`" * max(3, max((len(x) for x in source.split() if set(x) == {"`"}), default=0) + 1)
                lines.append(f"{fence}python\n{source}\n{fence}")
            else:
                raise ValueError("Solo se admiten celdas Markdown y código")
        page = pages / (path.stem + ".qmd")
        rendered = "\n\n".join(lines) + "\n"
        if not page.exists() or page.read_text() != rendered:
            page.write_text(rendered)
        shutil.copy2(path, ROOT / "downloads" / path.name)
        # Nombre real del kernelspec instalado por jupyterlite-pyodide-kernel.
        nb["metadata"]["kernelspec"] = {"name": "python", "display_name": "Python (Pyodide)", "language": "python"}
        (ROOT / "build/lite-content" / path.name).write_text(json.dumps(nb, ensure_ascii=False, indent=2) + "\n")

if __name__ == "__main__":
    generate()
