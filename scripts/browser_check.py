"""Prueba real en Chromium y Firefox. Ejecutar tras compilar.
Requiere: pip install -r requirements-browser.txt; python -m playwright install chromium firefox
"""
import asyncio
from functools import partial
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
import json
from pathlib import Path
import tempfile
import threading
import time
from playwright.async_api import async_playwright

ROOT=Path(__file__).resolve().parents[1]
class Quiet(SimpleHTTPRequestHandler):
    def log_message(self,*args): pass
async def main():
    # Montar bajo un prefijo, igual que un repositorio Pages.
    with tempfile.TemporaryDirectory() as td:
        (Path(td)/'curso-demo').symlink_to(ROOT/'_output',target_is_directory=True)
        server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=td))
        threading.Thread(target=server.serve_forever,daemon=True).start()
        base=f'http://127.0.0.1:{server.server_port}/curso-demo'
        results=[]
        async with async_playwright() as pw:
            for name in ('chromium','firefox'):
                browser=await getattr(pw,name).launch()
                context=await browser.new_context(accept_downloads=True)
                page=await context.new_page()
                print(name, 'inicio',flush=True)
                failures=[]
                page.on('pageerror', lambda e: failures.append(str(e)))
                await page.goto(base+'/src/01_teoria/teoria-01.html')
                slides=page.get_by_role('link',name='Ver diapositivas',exact=True)
                await slides.click()
                await page.wait_for_function('window.Reveal?.isReady()')
                assert page.url.endswith('teoria-01.reveal.html') or 'teoria-01.reveal.html#' in page.url
                await page.screenshot(path=str(ROOT/f'build/{name}-diapositivas.png'),full_page=True)
                await page.goto(base+'/src/03_practicas/practica-01.html')
                async with page.expect_download() as dl:
                    await page.get_by_text('Descargar notebook de Jupyter',exact=True).click()
                download=await dl.value
                original=json.loads(Path(await download.path()).read_text())
                assert 'NotImplementedError' in ''.join(original['cells'][2]['source'])
                await page.screenshot(path=str(ROOT/f'build/{name}-practica.png'),full_page=True)
                start=time.monotonic()
                await page.goto(base+'/lite/lab/index.html?path=practica-01.ipynb')
                await page.wait_for_function('window.jupyterapp?.shell.currentWidget?.content?.model?.cells?.get(4)',timeout=120000)
                print(name, 'notebook abierto',flush=True)
                await asyncio.wait_for(page.evaluate('async () => {await jupyterapp.shell.currentWidget.sessionContext.ready; await jupyterapp.shell.currentWidget.sessionContext.session.kernel.info;}'),120)
                print(name, 'kernel listo',flush=True)
                ready=round(time.monotonic()-start,2)
                async def run(source,expected):
                    await page.evaluate('(s) => {jupyterapp.shell.currentWidget.content.model.cells.get(2).sharedModel.setSource(s)}',source)
                    await asyncio.wait_for(page.evaluate('jupyterapp.commands.execute("notebook:run-all-cells")'),120)
                    await page.wait_for_function('(text) => JSON.stringify(jupyterapp.shell.currentWidget.content.model.cells.get(4).toJSON().outputs).includes(text)',arg=expected,timeout=120000)
                await run('def sumar(a,b): raise NotImplementedError("Implementa sumar")','Revisa tu función')
                await page.evaluate('jupyterapp.commands.execute("notebook:clear-all-cell-outputs")')
                await run('def sumar(a,b): return a-b','Revisa tu función')
                print(name, 'incorrecta detectada',flush=True)
                # Clear old output to ensure the next result is fresh.
                await page.evaluate('jupyterapp.commands.execute("notebook:clear-all-cell-outputs")')
                await run('def sumar(a,b): return a+b','Todas las pruebas superadas')
                print(name, 'correcta aceptada',flush=True)
                await page.evaluate('jupyterapp.commands.execute("docmanager:save")')
                async with page.expect_download(timeout=30000) as dl:
                    await page.evaluate('jupyterapp.commands.execute("docmanager:download")')
                download=await dl.value
                solved=json.loads(Path(await download.path()).read_text())
                assert 'return a+b' in ''.join(solved['cells'][2]['source'])
                await page.screenshot(path=str(ROOT/f'build/{name}-lite.png'),full_page=True)
                await page.reload()
                await page.wait_for_function('window.jupyterapp?.shell.currentWidget?.content?.model?.cells?.get(4)',timeout=120000)
                saved=await page.evaluate('jupyterapp.shell.currentWidget.content.model.cells.get(2).sharedModel.getSource()')
                assert 'return a+b' in saved
                # Published notebook remains unsolved, even after save/reload/export.
                published=await context.request.get(base+'/lite/files/practica-01.ipynb')
                assert 'NotImplementedError' in ''.join((await published.json())['cells'][2]['source'])
                results.append({'browser':name,'version':browser.version,'cold_ready_seconds':ready,'incorrect_fails':True,'correct_passes':True,'export_preserves_solution':True,'reload_preserves_solution':True,'published_unchanged':True,'pageerrors':failures})
                print(json.dumps(results[-1],ensure_ascii=False),flush=True)
                await page.goto(base+'/')
                await page.screenshot(path=str(ROOT/f'build/{name}-inicio.png'),full_page=True)
                await page.set_viewport_size({'width':390,'height':844})
                await page.screenshot(path=str(ROOT/f'build/{name}-movil.png'),full_page=True)
                await browser.close()
        server.shutdown()
        (ROOT/'build/browser-results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
if __name__=='__main__': asyncio.run(main())
