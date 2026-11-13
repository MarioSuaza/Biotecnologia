"""Conservar recursos publicados para páginas que sigan en caché tras actualizar."""
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def preserve_assets():
    # No requiere red. En copias sin historial o sin gh-pages no hay recursos previos.
    try:
        previous = subprocess.run(
            ["git", "ls-tree", "-r", "--name-only", "origin/gh-pages", "--", "site_libs"],
            cwd=ROOT, capture_output=True, check=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("Sin publicación anterior local: no hay recursos que conservar.")
        return
    output = (ROOT / "_output").resolve()
    restored = 0
    for name in previous.stdout.decode().splitlines():
        destination = (output / name).resolve()
        if not destination.is_relative_to(output) or destination.exists():
            continue
        content = subprocess.run(
            ["git", "show", f"origin/gh-pages:{name}"],
            cwd=ROOT, capture_output=True, check=True,
        ).stdout
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(content)
        restored += 1
    print(f"Recursos de publicaciones anteriores conservados: {restored}.")


if __name__ == "__main__":
    preserve_assets()
