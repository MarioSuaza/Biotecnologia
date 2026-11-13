from pathlib import Path
import shutil
root = Path(__file__).resolve().parents[1]
for name in ("_output", ".quarto", "build", "downloads"):
    shutil.rmtree(root / name, ignore_errors=True)
# Restos que una previsualización interrumpida puede dejar junto a las fuentes.
shutil.rmtree(root / "site_libs", ignore_errors=True)
for name in ("index.html", "search.json", "listings.json"):
    (root / name).unlink(missing_ok=True)
for folder in ("01_teoria", "03_practicas", "04_tareas"):
    for page in (root / "src" / folder).glob("*.html"):
        page.unlink()
