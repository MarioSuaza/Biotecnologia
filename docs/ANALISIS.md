# Análisis del proyecto de referencia

Inspección: 13 de noviembre de 2026. Raíz Git comprobada: `/Users/mesuaza/proyectos/clasesPythonUnizar`. Su directorio padre `/Users/mesuaza/proyectos` no pertenece a otro repositorio. Se observaron estado Git limpio y archivos generados locales que no se copiaron.

## Tecnologías y ejecución reales

Es un sitio Quarto (`project.type: website`) con portada `index.qmd`, índice EJS y render `src/**/*.qmd`. La salida es `_output`, con `.nojekyll` para Pages. Quarto instalado: 1.8.25. No es una aplicación Python con backend ni un frontend npm. `pyproject.toml` declara Python >=3.12 y opciones Ruff/Pyright, sin dependencias de ejecución. `flake.nix` ofrece Git, just, rsync, Quarto, Typst y ripgrep para Linux x86_64. No hay GitHub Actions en la referencia.

Los comandos existentes son `quarto preview`, `quarto render` y `quarto publish gh-pages --no-prompt --no-browser --no-render`. El README y justfile indican publicar desde la máquina local a `gh-pages`. Makefile añade un clean con búsquedas amplias de HTML: se sustituye en la plantilla por limpieza limitada a directorios generados.

## Materiales y navegación

`src/01_teoria` contiene temas con archivos numerados, imágenes y metadata para HTML/Reveal.js (`.reveal.html`). `02_problemas` contiene ejercicios; `03_practicas` está dividido en p0–p6 con páginas, scripts y ZIP de tests; `04_examenes` agrupa exámenes y recursos; `00_otros` contiene guías docentes. Todo ese contenido académico se excluye del proyecto nuevo.

La barra lateral de `_quarto.yml` usa patrones por carpeta, secciones plegables y buscador overlay. La portada usa `index.ejs` para mostrar un índice de títulos/subtítulos ordenado por ruta. Los estilos, las marcas, el índice y `_metadata.yml` son componentes compartidos. Reveal.js usa el complemento local `tldraw`, menú, progreso y logotipos. No se encontró una biblioteca de componentes React/Vue.

## Identidad visual

`_brand_light.yml` y `_brand_dark.yml` definen las marcas y tipografías Google: Nunito para cuerpo, Source Sans 3 para encabezados, Roboto Mono para código, y Sanchez disponible como familia adicional. Azul Unizar `#223d71`, verde `#78A540`, azul `#003660`, naranja `#DF8073` y rojo `#900C3F`. En oscuro, fondo negro y azul principal `#C8D6EF`. El formato activo usa `src/_style/fix.scss`; existen además `custom.scss` y `dark.scss`, que se conservan como recursos de diseño. Logotipos: `logo_uz.svg`, `unizar-black.svg`, `unizar-diis-white.svg`.

Se conservan estos recursos de identidad, sin imágenes de lecciones. Se adapta el título y se retira el antiguo `meta.link.home`. Los reconocimientos del README original se trasladan a `ATTRIBUTION.md`; no se encontró LICENSE general y no se presume una nueva licencia.

## Decisiones de la nueva plantilla

Quarto puede renderizar notebooks, pero el formato web de las prácticas necesita botones y una copia con el kernel correcto para Lite. Un generador pequeño de biblioteca estándar convierte el notebook fuente en Markdown Quarto sin ejecutar sus celdas; copia literalmente la descarga y adapta solo la metadata de la copia Lite. Evita tres versiones manuales del material, no requiere nbconvert para la conversión y preserva el enfoque Markdown del original. `nbformat` valida el esquema en las comprobaciones.

Se conservan HTML, Reveal.js, SCSS, marcas, índice EJS y publicación por `quarto publish`. La estructura nueva es 13 teorías, 13 prácticas y 4 tareas. Las antiguas secciones de problemas y exámenes no se copian. Los notebooks pendientes no desarrollan contenidos. El ejercicio mínimo de sumar es nuevo y queda sin solución.

JupyterLite se construye en `_output/lite` después de Quarto, con copias propias de los archivos del curso; no depende de una demo externa. El kernel descarga el runtime Pyodide desde su CDN predeterminado. El sitio puede hospedarse bajo una ruta de repositorio sin configurar un servidor de ejecución. Los notebooks siguen siendo descargables si el navegador o la conexión no permiten usar Lite.
