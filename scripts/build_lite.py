"""Post-render: construir Lite en el mismo árbol estático que Quarto."""
from pathlib import Path
import json
import os
import re
import shutil
import subprocess
import sys

root = Path(__file__).resolve().parents[1]
out = root / "_output/lite"
workspaces = {
    data["metadata"]["id"]: data
    for path in (root / "build/lite-workspaces").glob("*.jupyterlab-workspace")
    for data in [json.loads(path.read_text())]
}
# En preview reutilizar Lite solo cuando sus notebooks siguen siendo los actuales.
if os.environ.get("QUARTO_PROJECT_OUTPUT_DIR") and not os.environ.get("QUARTO_PROJECT_RENDER_ALL") and (out / "lab/index.html").exists():
    sources = {path.name: path.read_bytes() for path in (root / "build/lite-content").glob("*.ipynb")}
    published = {path.name: path.read_bytes() for path in (out / "files").glob("*.ipynb")}
    config = root / "lite/jupyter-lite.json"
    workspace_index = out / "api/workspaces/all.json"
    published_workspaces = json.loads(workspace_index.read_text()) if workspace_index.exists() else {}
    bootstrap_has_workspaces = '"workspacesAllJsonFile"' in (out / "lab/index.html").read_text()
    if sources == published and workspaces == published_workspaces and bootstrap_has_workspaces and config.stat().st_mtime <= (out / "jupyter-lite.json").stat().st_mtime:
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
                "--workspaces", str(root / "build/lite-workspaces"),
                "--output-dir", str(out)], check=True, cwd=root)
# La URL de cada workspace es nueva; su HTML debe anunciar el índice incluso si
# el navegador conserva un jupyter-lite.json anterior que aún no lo conocía.
lab = out / "lab/index.html"
text = lab.read_text()
config_script = re.search(r'(<script[^>]+id="jupyter-config-data"[^>]*>)(.*?)(</script>)', text, re.DOTALL)
if not config_script:
    raise RuntimeError("No se encuentra la configuración de inicio de JupyterLab")
page_config = json.loads(config_script.group(2))
page_config["workspacesAllJsonFile"] = "all.json"
lab.write_text(text[:config_script.start(2)] + json.dumps(page_config) + text[config_script.end(2):])
(root / "_output/.nojekyll").touch()
