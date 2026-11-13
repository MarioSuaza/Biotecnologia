# Curso con Quarto y JupyterLite

Curso con 13 clases de teoría, 13 prácticas y 4 tareas. **Todos los contenidos se editan en archivos `.qmd`.** Las prácticas generan automáticamente su página web y los notebooks para descarga y JupyterLite. La práctica 01 incluye un ejercicio de suma y autocomprobación; el resto está preparado para desarrollar el contenido.

La autoría y los recursos reutilizados se detallan en `ATTRIBUTION.md`.

## Instalar y abrir el proyecto

Necesitas Git, Quarto 1.8.25 o posterior y Python 3.12 o posterior. El entorno comprobado es macOS ARM64 con Python 3.14. Los comandos siguientes se ejecutan desde la raíz del proyecto:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.lock
quarto --version
```

`requirements.txt` declara las dependencias directas; `requirements.lock` fija las versiones del entorno probado. Incluyen `ipykernel`, necesario para la conversión nativa de Quarto y para probar Python en VS Code. Las herramientas de compilación no son las bibliotecas del kernel del alumno: JupyterLite utiliza Python/Pyodide en el navegador.

Abre la carpeta en VS Code e instala las extensiones **Quarto**, **Python** y **Jupyter**. Selecciona el intérprete o kernel `.venv/bin/python`. En Windows, la activación es `.venv\Scripts\Activate.ps1`; adapta `python3` a `python` en los hooks y comandos si es necesario. Esa plataforma no está validada.

## Dónde editar

| Contenido | Fuente editable |
|---|---|
| Portada | `index.qmd` |
| Teoría | `src/01_teoria/teoria-NN.qmd` |
| Prácticas | `src/03_practicas/practica-NN.qmd` |
| Tareas | `src/04_tareas/tarea-NN.qmd` |

Los `.qmd` de prácticas **son originales y se guardan en Git**. Las descargas y las copias de JupyterLite se generan desde ellos; no se editan ni se mantienen notebooks originales en otra carpeta.

```text
src/03_practicas/practica-01.qmd       ← editar aquí
  ├── _output/src/03_practicas/practica-01.html
  ├── downloads/practica-01.ipynb      → _output/downloads/
  └── build/lite-content/practica-01.ipynb → _output/lite/files/
```

`lite/` contiene la configuración del entorno web. `src/_filters/practice-actions.lua` añade a la página los dos botones azules y el aviso sobre ejecución; esos elementos no se incluyen en el notebook. Los estilos y logos están en `src/_style/`; las marcas, en `_brand_light.yml` y `_brand_dark.yml`.

## Escribir y probar una práctica

El título se define en el YAML inicial. Redacta las instrucciones en Markdown y usa bloques **`{python}`** para las celdas ejecutables:

````markdown
---
title: "Práctica 01"
---

## Ejercicio

Implementa la función siguiente.

```{python}
def sumar(a, b):
    raise NotImplementedError("Implementa sumar")
```

## Autocomprobación

```{python}
assert sumar(2, 3) == 5
```
````

Los bloques ` ```python ` sin llaves son ejemplos de texto, no celdas ejecutables. Para el contenido compartido con el notebook utiliza Markdown sencillo: títulos, listas, tablas y bloques Python. Los diseños específicos de Quarto, enlaces a datos e imágenes deben comprobarse también en JupyterLite; no se copian automáticamente archivos auxiliares de cada práctica.

En VS Code, coloca el cursor dentro de un bloque y pulsa **Run Cell**. En la extensión comprobada, **Cmd+Shift+Enter** ejecuta el bloque en macOS y **Option+Enter** ejecuta la selección. Ejecuta primero las definiciones y después sus tests. Si cambias una función, vuelve a ejecutar su definición. Las pruebas locales usan CPython; comprueba también el notebook en Pyodide antes de introducir bibliotecas nuevas.

`src/03_practicas/_metadata.yml` configura `execute.enabled: false`: los ejercicios se muestran y convierten, pero **no se ejecutan al construir la web**. Puedes probarlos manualmente en el editor. Los resultados de esas pruebas no se guardan en la fuente ni se publican como salidas.

## Generar y validar los notebooks

Con `.venv` activado:

```bash
quarto render
python scripts/check.py
python -m http.server 8000 --directory _output --bind 127.0.0.1
```

Abre <http://127.0.0.1:8000/> y entra en **Prácticas → Práctica 01**. Prueba ambos botones. También puedes abrir `downloads/practica-01.ipynb` en VS Code y ejecutar sus celdas con el kernel local. Para regenerar solo los notebooks, sin compilar la web:

```bash
python scripts/generate.py
```

El generador llama a **`quarto convert`**, prepara un título legible, asigna el kernel y publica notebooks sin salidas ni contadores. No modifica los `.qmd`. Los notebooks incluyen la huella de su fuente para detectar resultados desactualizados. Los tests visibles de la práctica 01 distinguen ejercicio pendiente, respuesta incorrecta y respuesta correcta.

Corrige siempre el **`.qmd` original** y vuelve a compilar. Los cambios que hagas en un notebook generado para probarlo no vuelven al `.qmd` y se reemplazan en la siguiente generación.

## Previsualización y limpieza

```bash
quarto preview --host localhost --port 7777
```

Abre <http://localhost:7777/>. Al guardar una práctica y renderizarla, el pre-render actualiza sus notebooks; el post-render reconstruye JupyterLite cuando cambia su contenido. Una copia ya guardada por el navegador puede ocultar el nuevo notebook: utiliza un contexto privado nuevo o importa la descarga actual con otro nombre.

Detén el servidor con **Ctrl+C antes de ejecutar otra compilación o limpieza en la misma carpeta**. Ejecutar simultáneamente preview y render puede dejar archivos incompletos o recursos ausentes.

```bash
python scripts/clean.py
quarto render
python scripts/check.py
```

La limpieza elimina salidas, cachés y restos HTML generados; conserva los `.qmd`, la configuración, los filtros y los estilos originales. Úsala al retirar o renombrar páginas para que no queden HTML obsoletos.

Atajos opcionales: `make run`, `make build`, `make check`, `make serve`, `make clean`; con `just`: `just preview`, `just render`, `just check`, `just serve` y `just publish`.

## Qué se genera y qué se guarda en Git

Se guardan los `.qmd`, configuración, estilos, filtros y scripts necesarios. Se ignoran `.venv/`, `.quarto/`, `build/`, `downloads/`, `_output/`, evidencias y archivos locales. No borres los scripts incluidos: los hooks los utilizan.

Al compilar:

1. `scripts/generate.py` convierte las prácticas QMD en notebooks.
2. Quarto genera las páginas web y las presentaciones.
3. `scripts/build_lite.py` construye JupyterLite con sus notebooks.
4. `scripts/preserve_assets.py` conserva recursos de la publicación anterior para páginas en caché.
5. `scripts/inline_theory_styles.py` integra el CSS en los HTML de teoría para conservar el diseño aunque falle una descarga externa de estilos.

La teoría conserva el botón **Ver diapositivas** abajo a la derecha y el enlace **Otros formatos → RevealJS**. En la presentación usa flechas para avanzar, **F** para pantalla completa y **Esc** para la vista general.

## Publicar en GitHub Pages

El código fuente está en `main`; la web compilada se publica en `gh-pages`. Después de editar, registra y sube tus cambios de fuente con Git. Para actualizar la web, detén la previsualización y ejecuta:

```bash
source .venv/bin/activate
git fetch origin gh-pages
quarto render
python scripts/check.py
quarto publish gh-pages --no-prompt --no-browser --no-render
```

El fetch permite conservar los recursos de la publicación anterior. No publiques una compilación parcial. En un repositorio nuevo sin rama `gh-pages`, omite el fetch inicial y ejecuta la primera publicación sin `--no-prompt` para inicializarla; configura **Settings → Pages → Deploy from a branch → gh-pages → / (root)**.

Este curso está en <https://www.mariosuaza.com/Biotecnologia/>. Los enlaces propios son relativos y funcionan bajo el prefijo de otro repositorio. No cambies los enlaces de los botones a `/downloads/…` o `/lite/…`, pues perderían ese prefijo. La configuración `lite/jupyter-lite.json` controla el nombre del entorno; `_quarto.yml` y las marcas controlan títulos y apariencia del sitio.

## JupyterLite y el trabajo del estudiante

Python se ejecuta con Pyodide en el navegador de cada alumno; GitHub Pages sirve archivos estáticos. El runtime y paquetes pueden descargarse desde CDN, por lo que se necesita conexión. No se instala un servidor Python ni se reciben entregas o calificaciones automáticamente.

El alumno ejecuta las celdas de arriba abajo con **Shift+Enter** o **Run → Run All Cells**. Guarda con **Ctrl+S/Cmd+S** y descarga su respuesta mediante **File → Download**. Sus cambios no modifican el QMD ni el notebook publicado.

El almacenamiento del navegador no sincroniza equipos ni es una copia de seguridad. Tras recargar se pierden las variables del kernel; vuelve a ejecutar las celdas. Una copia guardada puede ocultar actualizaciones con el mismo nombre: descárgala o renómbrala antes de recuperar el original. No borres todo el almacenamiento del sitio para actualizar una práctica.

Las bibliotecas de Python deben ser compatibles con Pyodide. Instalarlas en `.venv` o añadirlas a `requirements.txt` no las instala en el navegador. Para probar paquetes compatibles en Lite puedes utilizar `await piplite.install("nombre")`; verifica sus operaciones reales y las rutas de datos antes de preparar una actividad.

## Volver a la metodología anterior

La etiqueta Git **`antes-practicas-qmd`** conserva la versión previa a la migración, con los notebooks como fuente. Para probarla sin borrar el trabajo actual:

```bash
git switch -c recuperar-version-anterior antes-practicas-qmd
```

Con los cambios guardados y el servidor detenido, compila esa rama y compruébala. Para volver a esta metodología, ejecuta `git switch main`. Cambiar de rama no modifica la web publicada hasta que vuelvas a compilar y publicar.
