"""Integrar CSS y sus archivos locales en la teoría sin descargar fuentes remotas."""
import base64
from html import unescape
from html.parser import HTMLParser
import json
import mimetypes
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "_output"
FONT_IMPORT = re.compile(
    r'''@import\s*(?:url\(\s*)?(["'])(https://fonts\.googleapis\.com/[^"']+)\1\s*\)?\s*;'''
)


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
        self.fonts = set()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag != "link" or attrs.get("rel") != "stylesheet":
            return
        href = attrs.get("href", "")
        path = local_path(self.page.parent, href)
        if path is None:
            return
        css = path.read_text()

        def defer_font(match):
            self.fonts.add(match.group(2))
            return ""

        css = FONT_IMPORT.sub(defer_font, css)

        def embed_asset(match):
            url = match.group(1).strip().strip("\"'")
            asset = local_path(path.parent, url)
            if asset is None:
                return match.group(0)
            fragment = urlsplit(url).fragment
            return 'url("' + data_uri(asset) + ("#" + fragment if fragment else "") + '")'

        css = re.sub(r"url\(([^)]+)\)", embed_asset, css)
        original = self.get_starttag_text()
        # Quarto usa estos <link> como controles del tema. El CSS real es un <style>
        # independiente: no depende de permitir hojas de estilo con direcciones data:.
        control = re.sub(
            r'\bhref\s*=\s*([\"\']).*?\1', 'href="data:text/css,"', original, count=1,
        )
        classes = attrs.get("class", "").split()
        if "quarto-color-scheme-extra" in classes:
            self.replacements[original] = control
            return
        alternate = "quarto-color-alternate" in classes
        mode = "alternate" if alternate else "primary"
        media = "not all" if alternate else "all"
        self.replacements[original] = (
            f'<style data-course-style="{mode}" media="{media}">\n{css}\n</style>\n' + control
        )


def theme_and_fonts(fonts):
    return """<script id="course-inline-style-controller">
(() => {
  const syncTheme = () => {
    const dark = document.body?.classList.contains('quarto-dark') ?? false;
    document.querySelectorAll('style[data-course-style="alternate"]').forEach(style => {
      style.media = dark ? 'all' : 'not all';
    });
  };
  new MutationObserver(syncTheme).observe(document.documentElement, {
    subtree: true, childList: true, attributes: true, attributeFilter: ['class']
  });
  syncTheme();
  window.addEventListener('load', () => {
    const fonts = FONT_URLS;
    fonts.forEach(url => {
      const link = document.createElement('link');
      link.rel = 'stylesheet';
      link.href = url;
      link.media = 'print';
      link.onload = () => { link.media = 'all'; };
      document.head.append(link);
    });
  }, { once: true });
})();
</script>
""".replace("FONT_URLS", json.dumps(sorted(fonts)))


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
            text = text.replace("</head>", theme_and_fonts(parser.fonts) + "</head>", 1)
            page.write_text(text)
            count += 1
    print(f"Páginas de teoría con estilos integrados: {count}.")


if __name__ == "__main__":
    inline_styles()
