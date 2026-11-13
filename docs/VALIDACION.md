# Validación de la entrega

Fecha: 13 de noviembre de 2026. Sistema: macOS ARM64. Carpeta y raíz Git independientes: `/Users/mesuaza/proyectos/plantilla-curso-quarto`. El directorio padre no es un repositorio. Rama inicial `main`, sin historial heredado ni remotos. No se crea ni publica un repositorio remoto.

## Revisión de descarga y acceso a diapositivas

En la revisión se detectó que el enlace Markdown de descarga dejaba los atributos `{.btn .btn-primary download}` como texto literal en el HTML. Se sustituyó por un enlace HTML con `download="practica-NN.ipynb"` en el generador de las 13 prácticas. La comprobación estructural ahora exige ese atributo, además de la existencia del destino.

Se añadió el botón **Ver diapositivas** abajo a la derecha en las páginas de teoría, reutilizando el destino Reveal.js de «Otros formatos». Las páginas de prácticas explican que su código es estático y que las pruebas se ejecutan en JupyterLite con **Run → Run All Cells**.

Tras los cambios se recompiló el sitio completo y se verificaron los 2.318 enlaces y recursos. Se repitió `scripts/browser_check.py` en Chromium y Firefox bajo `/curso-demo/`: descarga original, clic en el botón de diapositivas y carga de Reveal.js, detección de respuesta incorrecta, aceptación de respuesta correcta, exportación y persistencia tras recarga. Sin excepciones JavaScript. Los tiempos de carga del kernel en esta repetición fueron 9,29 s y 9,75 s. Resultados y capturas de esta revisión: `build/browser-results.json` y `build/*-diapositivas.png`. La publicación remota sigue sin realizarse.

## Integridad y compilación

- Comparación SHA-256 de **590 archivos** del proyecto original (incluidos sus archivos locales ignorados y excluidos los internos de `.git`): sin diferencias. Estado Git original limpio al terminar. No se ejecutan operaciones de escritura de remotos o configuración sobre ese repositorio.
- Proyecto generado desde recursos seleccionados, sin copiar `.git`, cachés, entornos, contenidos académicos, ZIP de ejercicios, datos, exámenes o imágenes de lecciones. Se conservan exclusivamente los recursos de diseño, herramientas reutilizables y reconocimientos documentados.
- Instalación limpia de `requirements.lock` en la `.venv` de esta carpeta, con Python 3.14.7.
- `quarto render` con Quarto 1.8.25: salida completa HTML, Reveal.js y JupyterLite. Se han realizado renders sucesivos; el hook elimina el registro de tareas Lite para no perder la configuración al reconstruir una salida borrada. La previsualización incremental conserva Lite; los cambios de notebook requieren render completo.
- `quarto preview --host localhost --port 7777`: inicio comprobado y HTTP 200 para portada, descarga de práctica 01 y aplicación Lite. El servidor temporal se detuvo al acabar.
- `python scripts/check.py`: **13 teorías, 13 prácticas, 4 tareas y 2.318 enlaces/recursos relativos existentes**, incluidos los de las presentaciones. Se corrigió en la plantilla la ruta del logo Reveal.js heredada.
- Los 13 notebooks pasan la validación de esquema de nbformat. Las descargas publicadas son idénticas a sus fuentes. Las fuentes no contienen salidas ni contadores de ejecución. Las 12 prácticas pendientes y todas las tareas siguen sin desarrollar.
- Tests en CPython: el ejercicio pendiente produce errores, una resta incorrecta produce fallos, y una suma correcta pasa los cuatro métodos de unittest. No se guarda ninguna solución en el material distribuido.

## Prueba real de JupyterLite

`scripts/browser_check.py` monta `_output` bajo **`/curso-demo/`** en un servidor HTTP temporal, equivalente al prefijo de un repositorio Pages. Usa los archivos construidos en esta carpeta, no una demo externa. Se ejecuta código en el kernel real Pyodide, no una simulación JavaScript de los tests.

| Navegador | Versión | Carga inicial hasta kernel listo | Detecta implementación incorrecta | Acepta correcta | Exporta cambios | Conserva código tras recarga |
|---|---|---|---|---|---|---|
| chromium | 158.0.8127.18 | 9.54 s | Sí | Sí | Sí | Sí |
| firefox | 159.0 | 10.53 s | Sí | Sí | Sí | Sí |

Tiempos observados en contextos nuevos y con la conexión de esta máquina; no son una garantía, ni una medición de dispositivos móviles o de todas las cachés de red. El runtime predeterminado de la extensión fijada usa Pyodide **314.0.6** desde jsDelivr. No se hospeda una instancia pública de demostración, pero sí existe esa dependencia de red del runtime.

En ambos navegadores se comprueban:

1. Página web de la primera práctica y descarga original sin resolver.
2. Apertura explícita de `practica-01.ipynb` mediante el parámetro `path`.
3. Ejecución del ejercicio pendiente, una implementación incorrecta y una correcta; resultados de unittest dentro del kernel.
4. Guardado y descarga desde JupyterLite: el JSON exportado contiene la solución escrita en la prueba.
5. Recarga: el archivo guardado conserva el código del estudiante. Esto no implica que se conserven las variables del kernel.
6. El archivo servido por `lite/files/practica-01.ipynb` sigue sin resolver después de guardar y exportar la copia.
7. Ninguna excepción `pageerror` de JavaScript observada.

Los tests usan stdout para que el resumen correcto no adopte el fondo rojo que Jupyter aplica normalmente a stderr. La práctica explica `OK`, `FAIL` y `ERROR`. Capturas revisadas de portada de escritorio, portada a 390 px, práctica y resultados del kernel: [evidencias](evidencias/). La captura estrecha solo verifica la presentación web; no demuestra usabilidad del editor Lite en un teléfono. Resultados estructurados: [browser-results.json](evidencias/browser-results.json).

## Límites y comprobaciones pendientes

- **No se ha publicado en GitHub Pages**, conforme al alcance solicitado. Se ha validado la ruta base local; autenticación Git, permisos y activación efectiva de Pages quedan para el usuario.
- Safari, móviles reales, modo sin conexión y políticas institucionales de almacenamiento/red no se han ensayado.
- La persistencia está comprobada al guardar y recargar en el mismo contexto. No se garantizan duración ilimitada, sincronización entre navegadores ni recuperación tras borrar datos o superar cuotas. La descarga es la copia de seguridad del estudiante.
- El comportamiento de copias locales ante una actualización del original está respaldado por la documentación oficial; no se ha simulado un despliegue remoto actualizado. El README explica exportar/renombrar y retirar solo la copia afectada.
- No se introducen datos ni bibliotecas adicionales en el ejercicio. La carga y lectura de archivos pequeños y la compatibilidad de paquetes nuevos quedan por comprobar cuando una actividad los necesite. La documentación describe esas posibilidades, pero no se presentan como verificadas aquí.
- Las interfaces locales de JupyterLab, Jupyter Notebook y VS Code, Windows y la alternativa Nix no se han ensayado. El esquema del notebook y sus tests sí se han validado con CPython.
- Quarto puede advertir que aún no conoce `lite/lab/index.html` durante el render: la aplicación se genera en el post-render. La comprobación posterior y las pruebas HTTP confirman esos destinos. Las advertencias opcionales de `libarchive-c`/traducciones de Lite no impiden construir ni ejecutar el ejemplo; no se añaden esas dependencias porque no son necesarias.

Conclusión: JupyterLite aporta un primer entorno práctico de Python sin instalación para resolver y autocomprobar esta actividad. Se integra como complemento con descarga siempre disponible, sin servidor de ejecución, cuentas, entregas ni calificación centralizada. Las capacidades confirmadas se limitan al flujo y navegadores descritos.
