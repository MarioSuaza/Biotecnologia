# Guía de uso del curso

Web: <https://www.mariosuaza.com/Biotecnologia/>.

## 1. Preparar el proyecto

Necesitas **Git, Quarto 1.8.25 o posterior y Python 3.12 o posterior**. Abre la carpeta del proyecto en VS Code e instala las extensiones **Quarto**, **Python** y **Jupyter**.

Desde la raíz del proyecto, en macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.lock
```

La instalación solo se hace una vez. Cada vez que abras una terminal nueva, activa el entorno con `source .venv/bin/activate`. En VS Code, selecciona `.venv/bin/python` como intérprete o kernel.

## 2. Editar el contenido

| Contenido | Archivo que debes editar |
|---|---|
| Portada | `index.qmd` |
| Teoría | `src/01_teoria/teoria-NN.qmd` |
| Prácticas | `src/03_practicas/practica-NN.qmd` |
| Tareas | `src/04_tareas/tarea-NN.qmd` |

Edita siempre los **`.qmd` originales**. No edites los HTML ni los notebooks de `downloads/`, `build/` o `_output/`: se generan automáticamente y tus cambios se sobrescribirían.

Para probar Python en un `.qmd`, utiliza bloques con **`{python}` entre llaves**:

````markdown
```{python}
print(2 + 3)
```
````

Coloca el cursor dentro del bloque y pulsa **Run Cell**. En macOS, **Cmd+Shift+Enter** ejecuta el bloque y **Option+Enter** ejecuta las líneas seleccionadas. Ejecuta las definiciones antes de sus tests.

Los ejercicios de las prácticas no se ejecutan al compilar la web; puedes ejecutarlos manualmente desde el editor o el notebook generado.

## 3. Ver los cambios en local

```bash
source .venv/bin/activate
quarto preview --host localhost --port 7777
```

Abre <http://localhost:7777/>. Guarda el `.qmd` para actualizar la previsualización. Las prácticas también actualizan sus notebooks de descarga y JupyterLite.

En teoría, pulsa **Ver diapositivas**, abajo a la derecha. Usa las flechas para avanzar, **F** para pantalla completa y **Esc** para la vista general.

**Detén la previsualización con Ctrl+C antes de compilar, limpiar o publicar.**

## 4. Comprobar la web y los notebooks

Con el entorno activado y la previsualización detenida:

```bash
quarto render
python scripts/check.py
python -m http.server 8000 --directory _output --bind 127.0.0.1
```

Abre <http://127.0.0.1:8000/> y comprueba la práctica:

- **Descargar Notebook:** descarga el notebook generado desde el `.qmd`. También puedes abrir `downloads/practica-01.ipynb` en VS Code.
- **Abrir en el navegador:** abre la práctica elegida en JupyterLite, en modo documento único y con el explorador cerrado. Ejecuta las celdas con **Shift+Enter** o **Run → Run All Cells**. Las otras prácticas siguen disponibles en el entorno; esta vista simplifica el trabajo y conserva los archivos guardados.
- Para conservar una respuesta del alumno, guarda y usa **File → Download**. Guardar en el navegador no envía el trabajo al profesor.

Si encuentras un error, corrígelo en el **`.qmd`** y vuelve a compilar. Los cambios hechos en el notebook de prueba no se trasladan al `.qmd`. Detén el servidor con **Ctrl+C** cuando termines.

## 5. Guardar y publicar los cambios

Guarda tus cambios en GitHub:

```bash
git add .
git commit -m "Actualizar contenidos del curso"
git push origin main
```

Con el entorno activado y la previsualización detenida, publica la web:

```bash
git fetch origin gh-pages
quarto render
python scripts/check.py
quarto publish gh-pages --no-prompt --no-browser --no-render
```

**Si una comprobación falla, no publiques:** corrige el error y repite la compilación y las comprobaciones. El código se guarda en `main`; la web se publica en `gh-pages`. GitHub Pages puede tardar unos minutos en mostrar la actualización.

Si tienes `just` instalado, **`just publish`** ejecuta los cuatro pasos de publicación.

## 6. Evitar fallos y resolver problemas

- Ejecuta **un solo proceso de Quarto a la vez**: detén preview antes de usar render o limpiar.
- Publica siempre el sitio completo con las comprobaciones anteriores. El `git fetch` permite conservar recursos que todavía utilizan páginas en caché.
- Conserva los scripts, filtros, estilos y la configuración del proyecto. No edites directamente los archivos generados.
- Si ves una versión anterior, recarga la página sin caché. En Safari puedes usar **Option+Cmd+R** o probar una ventana privada.
- Si JupyterLite muestra una copia antigua, descarga primero tu trabajo e importa el notebook actualizado con otro nombre. Necesita conexión para cargar Python y sus paquetes.
- Si añades bibliotecas, comprueba el notebook también en JupyterLite: instalar un paquete en `.venv` no lo instala en el navegador.

Si has retirado o renombrado páginas, reconstruye desde cero, siempre con la previsualización detenida:

```bash
python scripts/clean.py
quarto render
python scripts/check.py
```

Para consultar el respaldo anterior a la migración, guarda tus cambios, detén los servidores y ejecuta `git switch -c recuperar-version-anterior antes-practicas-qmd`. Regresa con `git switch main`. Cambiar de rama no cambia la web publicada hasta volver a compilar y publicar.

Autoría y recursos reutilizados: [ATTRIBUTION.md](ATTRIBUTION.md).
