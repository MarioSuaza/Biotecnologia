-- Los controles de la web no forman parte de los notebooks convertidos.
function Pandoc(doc)
  if not quarto.doc.is_format("html") then
    return doc
  end
  local stem = pandoc.path.filename(quarto.doc.input_file):gsub("%.qmd$", "")
  local notebook = stem .. ".ipynb"
  local controls = string.format([[
<div class="practice-actions">
<a class="btn btn-primary" href="../../downloads/%s" download="%s">Descargar Notebook</a>
<a class="btn btn-primary" href="../../lite/lab/index.html?workspace=curso-%s&amp;mode=single-document" target="_blank" rel="noopener">Abrir en el navegador</a>
</div>
<div class="callout callout-style-simple callout-note callout-titled">
<div class="callout-header"><div class="callout-title-container">Dónde ejecutar el código</div></div>
<div class="callout-body-container callout-body">
<p>Esta página muestra las instrucciones y el código, pero no ejecuta Python.
Pulsa <strong>Abrir en el navegador</strong> para trabajar en JupyterLite, o descarga
el notebook y ábrelo en Jupyter o VS Code.</p>
<p>Espera a que el kernel <strong>Python (Pyodide)</strong> esté listo. Después de cambiar
tu respuesta, usa <strong>Run → Run All Cells</strong>. Los resultados aparecen debajo
de los tests. Descarga tu copia de trabajo para conservarla fuera del navegador.</p>
</div>
</div>
]], notebook, notebook, stem)
  doc.blocks:insert(1, pandoc.RawBlock("html", controls))
  return doc
end
