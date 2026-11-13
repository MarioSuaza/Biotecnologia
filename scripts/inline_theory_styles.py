"""Integrar CSS y sus archivos locales en la teoría sin descargar fuentes remotas."""
import base64
from html import unescape
from html.parser import HTMLParser
import mimetypes
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "_output"


def data_uri(path):
    mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode()


def local_path(base, url):
    parts = urlsplit(unescape(url))
    if parts.scheme or parts.netloc or not parts.path:
        return None
    path = (base / unquote(parts.path)).resolve()
    if not path.is_relative_to(OUTPUT.resolve()):
        raise ValueError(f"Recurso fuera del sitio: {url}")
    return path


class Styles(HTMLParser):
    def __init__(self, page):
        super().__init__(convert_charrefs=False)
        self.page = page
        self.replacements = {}

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag != "link" or attrs.get("rel") != "stylesheet":
            return
        href = attrs.get("href", "")
        path = local_path(self.page.parent, href)
        if path is None:
            return
        css = path.read_text()

        def embed_asset(match):
            url = match.group(1).strip().strip("\"'")
            asset = local_path(path.parent, url)
            if asset is None:
                return match.group(0)
            fragment = urlsplit(url).fragment
            return 'url("' + data_uri(asset) + ("#" + fragment if fragment else "") + '")'

        css = re.sub(r"url\(([^)]+)\)", embed_asset, css)
        uri = "data:text/css;base64," + base64.b64encode(css.encode()).decode()
        original = self.get_starttag_text()
        # Mantener <link>, sus identificadores y clases para el selector claro/oscuro de Quarto.
        self.replacements[original] = re.sub(
            r'\bhref\s*=\s*([\"\']).*?\1', lambda _: f'href="{uri}"', original, count=1,
        )


def inline_styles():
    count = 0
    for page in (OUTPUT / "src/01_teoria").glob("*.html"):
        if page.name.endswith(".reveal.html"):
            continue
        text = page.read_text()
        parser = Styles(page)
        parser.feed(text)
        for before, after in parser.replacements.items():
            text = text.replace(before, after)
        if parser.replacements:
            page.write_text(text)
            count += 1
    print(f"Páginas de teoría con estilos integrados: {count}.")


if __name__ == "__main__":
    inline_styles()
