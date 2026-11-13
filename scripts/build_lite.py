"""Post-render: construir Lite en el mismo árbol estático que Quarto."""
from pathlib import Path
import os
import shutil
import subprocess
import sys

root = Path(__file__).resolve().parents[1]
out = root / "_output/lite"
# En preview reutilizar Lite solo cuando sus notebooks siguen siendo los actuales.
if os.environ.get("QUARTO_PROJECT_OUTPUT_DIR") and not os.environ.get("QUARTO_PROJECT_RENDER_ALL") and (out / "lab/index.html").exists():
    sources = {path.name: path.read_bytes() for path in (root / "build/lite-content").glob("*.ipynb")}
    published = {path.name: path.read_bytes() for path in (out / "files").glob("*.ipynb")}
    config = root / "lite/jupyter-lite.json"
    if sources == published and config.stat().st_mtime <= (out / "jupyter-lite.json").stat().st_mtime:
        print("JupyterLite ya contiene los notebooks actuales.")
        sys.exit(0)
if out.exists():
    shutil.rmtree(out)
# La base doit conserva tareas de salidas borradas; no reutilizarla.
for cache in root.glob(".jupyterlite.doit.db*"):
    cache.unlink()
subprocess.run([sys.executable, "-m", "jupyter", "lite", "build", "--force",
                "--lite-dir", str(root / "lite"),
                "--contents", str(root / "build/lite-content"),
                "--output-dir", str(out)], check=True, cwd=root)
(root / "_output/.nojekyll").touch()
