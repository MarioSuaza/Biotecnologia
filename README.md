# Plantilla de curso con Quarto y notebooks

Proyecto independiente para escribir un curso nuevo con 13 clases de teoría, 13 prácticas y 4 tareas. Conserva la estructura técnica y el diseño general de la referencia, sin su contenido académico. Solo la práctica 01 tiene un ejercicio mínimo de validación. Consulta `ATTRIBUTION.md` para la autoría y los recursos reutilizados.

## Requisitos e instalación

- Git y Quarto **1.8.25** (versión comprobada; la configuración de marca requiere Quarto 1.7 o posterior).
- Python **3.12 o posterior** con `venv` y `pip` (comprobado con 3.14.7).
- Acceso a Internet para instalar dependencias, cargar las fuentes Google y descargar el runtime Pyodide en el navegador.
- `make` y `just` son opcionales; todos los pasos tienen comandos directos.

Abre esta carpeta con **Archivo → Abrir carpeta** en VS Code. No necesitas añadirla al workspace anterior. Opcionalmente instala las extensiones Quarto, Python y Jupyter.

Desde la raíz del nuevo proyecto, en macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.lock
quarto --version
python scripts/generate.py
quarto preview --host localhost --port 7777
```

Abre <http://localhost:7777/>. Detén el servidor con Ctrl+C. En Windows usa `py -m venv .venv`, `.venv\Scripts\Activate.ps1` y `python` en lugar de `python3`; en los hooks de `_quarto.yml` sustituye también `python3` por `python` si tu instalación no ofrece ese alias. La adaptación a Windows no está comprobada.

`requirements.txt` declara las dependencias directas; `requirements.lock` fija también sus dependencias transitivas. Para actualizar, hazlo en un entorno virtual limpio, valida de nuevo y regenera el lock con `python -m pip freeze > requirements.lock`.

JupyterLite necesita el extra de construcción `jupyterlite-core[contents]`, que instala `jupyter-server` para indexar los archivos. No se inicia ese servidor ni se publica Python del servidor: el resultado es HTML/JS/Wasm estático.

## Compilar, comprobar y previsualizar el resultado exacto

Con el entorno virtual activado:

```bash
quarto render
python scripts/check.py
python -m http.server 7777 --directory _output --bind 127.0.0.1
```

`quarto render` ejecuta automáticamente `scripts/generate.py` antes del render y `scripts/build_lite.py` después. El resultado completo está en `_output/`, incluido `_output/lite/`. No abras el HTML con `file://`: los módulos, el kernel y los recursos necesitan HTTP local o HTTPS publicado.

Equivalentes opcionales: `make run`, `make build`, `make check`, `just preview`, `just render`. `python scripts/clean.py` elimina exclusivamente los directorios generados. Tras borrar o renombrar páginas haz una limpieza y un render completo para retirar HTML obsoleto. La primera previsualización renderiza el sitio; si cambias notebooks, vuelve a ejecutar `quarto render` para actualizar también Lite y las descargas.

La teoría conserva además salida Reveal.js. En cada página de teoría, pulsa **Ver diapositivas**, abajo a la derecha; también está el enlace **Otros formatos → RevealJS**. Dentro de la presentación, usa las flechas para avanzar, `F` para pantalla completa y `Esc` para la vista general. Para compilar solo una presentación: `quarto render src/01_teoria/teoria-01.qmd --to revealjs`. Usa el render completo para preparar una publicación.

## Organización

```text
.
├── _quarto.yml                  # sitio, navegación, formatos y hooks
├── _brand_light.yml             # identidad clara
├── _brand_dark.yml              # identidad oscura
├── index.qmd / index.ejs         # portada e índice compartido
├── src/
│   ├── 01_teoria/teoria-01.qmd … teoria-13.qmd
│   ├── 03_practicas/             # páginas generadas; no editar
│   ├── 04_tareas/tarea-01.qmd … tarea-04.qmd
│   └── _style/                  # SCSS y logotipos heredados
├── notebooks/practica-01.ipynb … practica-13.ipynb  # fuente de prácticas
├── lite/jupyter-lite.json       # configuración de JupyterLite
├── scripts/                     # generación, construcción y comprobación
├── _extensions/tldraw/          # complemento de las diapositivas
├── downloads/                   # generado: copias literales para descargar
├── build/lite-content/          # generado: notebooks con metadata del kernel web
└── _output/                     # generado: sitio publicable completo
```

No se versionan entornos, cachés, salidas, credenciales, documentación interna (`docs/`) ni herramientas locales de prueba del navegador. Los cuatro scripts publicados son necesarios para generar, compilar, comprobar y limpiar el curso; `_quarto.yml`, Makefile y justfile los utilizan. `.gitignore` excluye los demás archivos de `scripts/`.

El código fuente se mantiene en `main`; el sitio generado, incluidos sus recursos y descargas, se publica en `gh-pages`. `flake.nix` y su lock se conservan como alternativa opcional del original (Nix, Linux x86_64; no comprobada en esta entrega). Esa alternativa proporciona Quarto y utilidades; también necesitas Python y las dependencias anteriores. No es requisito usar Nix.

## Escribir y reorganizar el curso

- **Teoría:** edita `src/01_teoria/teoria-NN.qmd`; título y subtítulo están en YAML, contenido en Markdown. `_metadata.yml` habilita HTML y Reveal.js.
- **Prácticas:** edita únicamente `notebooks/practica-NN.ipynb`. La primera celda Markdown contiene `# Práctica NN` (puedes ampliar el título); el resto contiene el material, ejercicios y tests. Usa celdas Markdown y código; no se admiten celdas raw. Mantén imágenes como archivos relativos y amplía el generador para distribuirlas a los tres destinos si las necesitas: esta plantilla valida prácticas autocontenidas sin adjuntos ni archivos auxiliares.
- **Tareas:** edita `src/04_tareas/tarea-NN.qmd`; añade objetivos, contenido y recursos cuando estén definidos.

Para añadir o retirar sesiones usa las mismas convenciones y dos dígitos. La navegación lateral usa patrones en `_quarto.yml`; el índice de inicio usa `src/**/*.qmd` en `index.qmd`. Cambia esos patrones o enumera rutas explícitas si deseas otro orden o agrupaciones. Renombra enlaces internos al reorganizar. `scripts/check.py` espera 13/13/4: actualiza sus conteos deliberadamente si cambia la estructura.

Modifica el título del sitio en `_quarto.yml` (incluido el pie de Reveal.js), la portada en `index.qmd` y el nombre del entorno en `lite/jupyter-lite.json`. Edita ambas marcas para títulos institucionales, colores y fuentes. Azul principal: `#223d71`; tema oscuro: `#C8D6EF`. Los logotipos están en `src/_style/logos/`; sus referencias viven en las marcas y en `_quarto.yml`. Conserva las atribuciones y comprueba los permisos institucionales de los recursos reutilizados. No quedan enlaces al repositorio original en la navegación.

## Una fuente para la práctica web, la descarga y Lite

El notebook de `notebooks/` es la **única fuente académica**. `generate.py`:

1. Valida que no haya salidas ni contadores de ejecución.
2. Copia el notebook sin cambios a `downloads/`.
3. Genera la página `.qmd` con el mismo Markdown y código (sin ejecutarlo), y ambos botones.
4. Genera la copia de Lite cambiando solo la identificación del kernel a `Python (Pyodide)`.

No edites `src/03_practicas/`, `downloads/` ni `build/`. Después de modificar la fuente, guarda el notebook, usa **Clear All Outputs**, reinicia el kernel si procede y compila. Las pruebas visibles forman parte del propio notebook, sin ZIP de tests ni versión web mantenida a mano. Los notebooks pendientes no contienen tests inventados; incluyen el espacio reservado.

## Probar la primera práctica

Abre **Prácticas → Práctica 01**. Comprueba que se ve el ejercicio y pulsa **Descargar Notebook** para obtener la versión original sin resolver. Con **Abrir en el navegador** se abre esa práctica en JupyterLite, en otra pestaña.

Ejecuta con Shift+Enter de arriba abajo, implementa `sumar(a, b)` y ejecuta sus tests. Inicialmente aparecen errores por `NotImplementedError`. `FAIL` muestra un resultado incorrecto; `ERROR` una excepción; `OK` confirma los cuatro métodos de prueba (positivos, negativos, cero y signos distintos). Tras editar la función ejecuta de nuevo su celda antes de los tests. Los tests son modificables, no exhaustivos, de autocomprobación y no envían nada al profesor.

La página Quarto es estática: copiar o cambiar texto en ella no ejecuta las pruebas. En JupyterLite espera a que el kernel esté listo, sustituye el `raise NotImplementedError(...)` por tu implementación y usa **Run → Run All Cells**. Así evitas probar una definición anterior que aún siga en la memoria del kernel. Los resultados se muestran debajo de la celda de autocomprobación.

Guarda con Ctrl+S/Cmd+S y usa **File → Download** (o clic derecho en el archivo → Download) para descargar el trabajo. El notebook descargado conserva el código y las salidas guardadas. Mantén el original publicado sin resolver.

Para trabajar localmente, abre el `.ipynb` en VS Code con extensiones Python/Jupyter y selecciona un kernel de Python, o instala un entorno opcional separado con `python -m pip install jupyterlab` y ejecuta `jupyter lab`; para la interfaz Notebook instala `notebook` y ejecuta `jupyter notebook`. Las pruebas de esta práctica solo usan `unittest` de la biblioteca estándar. Estas interfaces locales opcionales no se han ensayado; el notebook y sus tests sí se han comprobado con CPython. Estas instalaciones opcionales no forman parte de la compilación del sitio.

## Qué permite JupyterLite y cómo conservar el trabajo

El entorno distribuido por este proyecto ejecuta Python con Pyodide dentro del navegador. El servidor solo entrega archivos estáticos. No usa una instancia pública de demostración. La configuración predeterminada del kernel descarga Pyodide y sus paquetes desde CDN: **no se promete funcionamiento sin Internet**. La descarga inicial puede tardar; depende de la conexión y de la caché del navegador.

Puedes editar, ejecutar ejemplos y tests sin cambiar los originales publicados. JupyterLite guarda las copias modificadas en el almacenamiento de ese navegador (normalmente IndexedDB), asociado al origen y ruta base. La memoria del kernel y sus variables no persisten: tras recargar vuelve a ejecutar las celdas. El guardado no sincroniza dispositivos, perfiles ni navegadores; modo privado, borrado de datos, cuotas o políticas del navegador pueden perderlo. Descarga copias periódicas.

Una copia guardada puede ocultar una versión nueva publicada con el mismo nombre. Antes de actualizar una práctica, descarga o renombra tu copia, elimina **solo ese archivo** del explorador de Lite y recarga para recuperar el material distribuido. También puedes descargar el original desde la página Quarto e importarlo con otro nombre. No borres todo el almacenamiento del sitio para recuperar una práctica. Si el cambio es incompatible, el docente puede publicar con un nombre versionado y actualizar sus enlaces. Cambiar el dominio, protocolo, puerto local o ruta base puede dejar los trabajos anteriores en otro espacio de almacenamiento.

No hay acceso automático al disco local, servidores Python, procesos normales del sistema ni todas las bibliotecas de CPython. Para añadir bibliotecas, comprueba que existan en Pyodide o dispongan de wheels Python puros compatibles; puedes probar `await piplite.install("NOMBRE_DEL_PAQUETE")` en una celda y después el import y sus operaciones reales. Sustituye el valor de ejemplo. No basta con añadirlas a `requirements.txt`: ese archivo configura la compilación, no el kernel Wasm. Comprueba las versiones y repite las pruebas en los navegadores objetivo antes de introducir una dependencia. Extensiones nativas requieren una compilación compatible con Pyodide.

Los archivos pequeños pueden subirse al explorador de Lite y leerse desde el kernel cuando su sistema de archivos esté sincronizado. No se añade un dataset artificial al ejercicio de suma. La lectura de archivos subidos y la incorporación de bibliotecas adicionales quedan fuera de los casos probados en esta práctica; consulta la evaluación y la documentación oficial antes de diseñar una actividad que dependa de ello.

## Repositorio propio y publicación

Comprueba la independencia desde esta carpeta:

```bash
git rev-parse --show-toplevel
git status --short
git remote -v
```

La raíz debe ser esta carpeta, sin remotos hasta que los configures. Se inicializa una rama `main` sin historial heredado. Crea un repositorio **vacío** en GitHub (sin README, licencia ni gitignore automáticos). No se ha creado ni publicado ningún remoto en esta entrega.

```bash
git add .
git commit -m "Plantilla independiente del nuevo curso"
git remote add origin URL_DEL_NUEVO_REPOSITORIO
git push -u origin main
```

Sustituye `URL_DEL_NUEVO_REPOSITORIO` por la URL HTTPS o SSH real que muestre GitHub. Autentícate con tus credenciales habituales; no las guardes en el proyecto.

Para GitHub Pages, conserva el procedimiento de Quarto del original:

```bash
source .venv/bin/activate
quarto render
python scripts/check.py
quarto publish gh-pages --no-prompt --no-browser --no-render
```

Después configura en GitHub **Settings → Pages → Deploy from a branch → gh-pages → / (root)**. El repositorio debe permitir Pages. El comando requiere permisos de escritura y autenticación Git; crea/actualiza la rama publicable, sin editar el código fuente de `main`. No uses una compilación parcial para publicar. `just publish` encadena compilación y comprobación antes de publicar, si tienes `just`.

La URL real la proporciona GitHub Pages: para un repositorio de proyecto tiene la forma `https://USUARIO.github.io/REPOSITORIO/` (valores que debes sustituir). Todos los botones y recursos propios usan rutas relativas, por lo que el nombre del repositorio no está fijado en el código. Si configuras `website.site-url` para metadatos, usa tu URL real completa con el sufijo del repositorio. No conviertas los botones a `/lite/…` o `/downloads/…`: perderían ese prefijo. Se comprueba el alojamiento bajo `/curso-demo/` en las pruebas del navegador; el despliegue remoto queda para el usuario.

## Validación y problemas habituales

`python scripts/check.py` comprueba conteos, formato de notebooks, igualdad de descargas, originales limpios, tests con implementaciones pendiente/incorrecta/correcta, recursos y enlaces relativos del HTML.

Para comprobar el recorrido del alumno, abre la práctica 01, descarga el notebook, ejecútalo en JupyterLite, guarda y exporta tu respuesta. Comprueba también que la copia publicada sigue sin resolver.

- **`quarto` no encontrado:** instala Quarto y vuelve a abrir la terminal.
- **Falta `jupyter` o el kernel al compilar:** activa `.venv` antes de ejecutar Quarto e instala las dependencias completas, incluido `[contents]`.
- **Notebook con salidas:** usa Clear All Outputs y guarda; el generador rechaza las salidas para no distribuir validaciones del docente.
- **Cambios no visibles:** render completo; si es Lite, comprueba si tienes una copia del estudiante que oculta el original y descárgala antes de recuperarlo.
- **404 en Pages:** publica todo `_output`, conserva `.nojekyll`, revisa la rama `gh-pages` y las rutas relativas bajo el prefijo del repositorio.
- **Aviso de enlace Lite durante render:** Lite se genera en el post-render; confirma su existencia con `python scripts/check.py`. Los avisos de `libarchive-c` y traducciones son opcionales y no bloquean esta actividad.
- **Kernel cargando indefinidamente:** comprueba conexión, CDN, consola del navegador y bloqueadores; prueba un perfil moderno limpio. No se ofrece una alternativa de servidor.
- **Datos desaparecidos tras recargar:** vuelve a ejecutar las celdas para recuperar variables; si falta un archivo, comprueba perfil, origen/ruta y tus descargas de respaldo.

Las fuentes externas pueden fallar sin conexión; el navegador usa las familias alternativas del tema. Safari y dispositivos móviles no forman parte de la matriz comprobada de esta entrega.
