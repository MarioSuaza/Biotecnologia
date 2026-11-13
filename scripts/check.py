"""Validación estructural, notebooks, tests locales y enlaces del sitio compilado."""
from pathlib import Path
import contextlib
import io
import json
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import nbformat

root = Path(__file__).resolve().parents[1]
assert len(list((root/'src/01_teoria').glob('teoria-*.qmd'))) == 13
assert len(list((root/'src/04_tareas').glob('tarea-*.qmd'))) == 4
notebooks = sorted((root/'notebooks').glob('*.ipynb'))
assert len(notebooks) == 13
for path in notebooks:
    nb = nbformat.read(path, as_version=4)
    nbformat.validate(nb)
    assert all(c.execution_count is None and not c.outputs for c in nb.cells if c.cell_type == 'code')
    assert path.read_bytes() == (root/'_output/downloads'/path.name).read_bytes()
    page = (root/'_output/src/03_practicas'/(path.stem+'.html')).read_text()
    assert 'Descargar Notebook' in page and 'Abrir en el navegador' in page
    assert (root/'_output/lite/files'/path.name).is_file()
nb = nbformat.read(notebooks[0], as_version=4)
code_cells = [c.source for c in nb.cells if c.cell_type == 'code']
for solution, expected in [(code_cells[0],False), ('def sumar(a,b): return a-b',False), ('def sumar(a,b): return a+b',True)]:
    ns = {}
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        exec(solution,ns)
        exec(code_cells[1],ns)
    assert ns['resultado'].wasSuccessful() is expected
class Links(HTMLParser):
    def __init__(self):
        super().__init__(); self.links=[]; self.anchors=[]
    def handle_starttag(self,tag,attrs):
        if tag == 'a': self.anchors.append(dict(attrs))
        for k,v in attrs:
            if k in ('href','src') and v: self.links.append(v)
output = root/'_output'
checked=0
for page in [output/'index.html', *output.glob('src/**/*.html')]:
    parser=Links(); parser.feed(page.read_text())
    if page.parent.name == '03_practicas':
        notebook = page.stem + '.ipynb'
        assert any(a.get('download') == notebook and
                   a.get('href') == '../../downloads/' + notebook
                   for a in parser.anchors), f'Falta descarga real: {page}'
    for href in parser.links:
        u=urlsplit(href)
        if u.scheme or u.netloc or not u.path: continue
        # Todos los enlaces deben permanecer relativos al repositorio.
        assert not u.path.startswith('/'), (page,href)
        target=(page.parent/unquote(u.path)).resolve()
        assert target.is_relative_to(output.resolve()), (page,href)
        assert target.exists(), (page,href,target)
        checked+=1
print(f'OK: 13 teorías, 13 notebooks válidos, 4 tareas; tests pendiente/incorrecto/correcto; {checked} enlaces y recursos relativos existentes.')
