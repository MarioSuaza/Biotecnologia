from pathlib import Path
import shutil
root = Path(__file__).resolve().parents[1]
for name in ("_output", ".quarto", "build", "downloads"):
    shutil.rmtree(root / name, ignore_errors=True)
