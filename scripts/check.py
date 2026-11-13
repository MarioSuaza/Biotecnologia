"""Comprobar fuentes QMD, notebooks generados, tests y recursos de la web."""
from copy import deepcopy
from pathlib import Path
import contextlib
import hashlib
from html.parser import HTMLParser
import io
from urllib.parse import unquote, urlsplit

import nbformat
import yaml

from generate import FRONT_MATTER

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / '_output'
sources = sorted((ROOT / 'src/03_practicas').glob('practica-*.qmd'))
assert sources, 'No hay prácticas QMD'
assert not (ROOT / 'notebooks').exists(), 'Solo los QMD deben ser fuentes de prácticas'
metadata = yaml.safe_load((ROOT / 'src/03_practicas/_metadata.yml').read_text())
assert metadata['execute']['enabled'] is False, 'Los ejercicios no deben ejecutarse al publicar'
names = {source.stem + '.ipynb' for source in sources}
for folder in (ROOT / 'downloads', ROOT / 'build/lite-content', OUTPUT / 'downloads', OUTPUT / 'lite/files'):
    assert {path.name for path in folder.glob('practica-*.ipynb')} == names, folder
for source in sources:
    notebook_path = ROOT / 'downloads' / (source.stem + '.ipynb')
    notebook = nbformat.read(notebook_path, as_version=4)
    nbformat.validate(notebook)
    assert notebook.metadata.quarto_source.sha256 == hashlib.sha256(source.read_bytes()).hexdigest(), source
    title = yaml.safe_load(FRONT_MATTER.match(source.read_text()).group(1))['title']
    assert notebook.cells[0].source == '# ' + title, source
    assert 'path' not in notebook.metadata.kernelspec, 'No publicar rutas del equipo'
    assert all(c.execution_count is None and not c.outputs for c in notebook.cells if c.cell_type == 'code')
    assert not any('practice-actions' in c.source or 'Dónde ejecutar el código' in c.source for c in notebook.cells)
    assert notebook_path.read_bytes() == (OUTPUT / 'downloads' / notebook_path.name).read_bytes()
    expected = deepcopy(notebook)
    expected.metadata['kernelspec'] = {'name': 'python', 'display_name': 'Python (Pyodide)', 'language': 'python'}
    for folder in (ROOT / 'build/lite-content', OUTPUT / 'lite/files'):
        actual = nbformat.read(folder / notebook_path.name, as_version=4)
        nbformat.validate(actual)
        assert actual == expected, (source, folder)

notebook = nbformat.read(ROOT / 'downloads/practica-01.ipynb', as_version=4)
cells = [cell.source for cell in notebook.cells if cell.cell_type == 'code']
for solution, expected in [(cells[0], False), ('def sumar(a,b): return a-b', False), ('def sumar(a,b): return a+b', True)]:
    namespace = {}
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        exec(solution, namespace)
        exec(cells[1], namespace)
    assert namespace['resultado'].wasSuccessful() is expected


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.anchors = []
        self.inline_styles = 0
        self.style_contents = []
        self.in_inline_style = False

    def handle_starttag(self, tag, attrs):
        if tag == 'style' and 'data-course-style' in dict(attrs):
            self.inline_styles += 1
            self.in_inline_style = True
        if tag == 'a':
            self.anchors.append(dict(attrs))
        for key, value in attrs:
            if key in ('href', 'src') and value:
                self.links.append(value)

    def handle_endtag(self, tag):
        if tag == 'style':
            self.in_inline_style = False

    def handle_data(self, data):
        if self.in_inline_style:
            self.style_contents.append(data)


checked = 0
for page in [OUTPUT / 'index.html', *OUTPUT.glob('src/**/*.html')]:
    parser = Links()
    parser.feed(page.read_text())
    if page.parent.name == '01_teoria' and not page.name.endswith('.reveal.html'):
        assert not any(urlsplit(link).path.endswith('.css') for link in parser.links if not link.startswith('data:')), page
        assert parser.inline_styles >= 6, f'Faltan estilos directos en {page}'
        assert '@import' not in ''.join(parser.style_contents), f'CSS bloqueante en {page}'
    if page.parent.name == '03_practicas':
        notebook_name = page.stem + '.ipynb'
        assert any(a.get('download') == notebook_name and a.get('href') == '../../downloads/' + notebook_name
                   and 'btn-primary' in a.get('class', '') for a in parser.anchors), page
        assert any(a.get('href') == '../../lite/lab/index.html?path=' + notebook_name
                   and 'btn-primary' in a.get('class', '') for a in parser.anchors), page
        assert 'Descargar Notebook' in page.read_text(), page
    for href in parser.links:
        url = urlsplit(href)
        if url.scheme or url.netloc or not url.path:
            continue
        assert not url.path.startswith('/'), (page, href)
        target = (page.parent / unquote(url.path)).resolve()
        assert target.is_relative_to(OUTPUT.resolve()) and target.exists(), (page, href, target)
        checked += 1
print(f'OK: {len(sources)} prácticas QMD y notebooks coherentes; tests pendiente/incorrecto/correcto; {checked} enlaces y recursos existentes.')
