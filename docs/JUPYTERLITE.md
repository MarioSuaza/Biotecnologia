# Evaluación de JupyterLite

Consulta oficial realizada el 13 de noviembre de 2026. Versiones construidas: JupyterLite Core 0.8.7 y kernel Pyodide 0.8.7. Los resultados empíricos están en `VALIDACION.md`; no deben confundirse con las posibilidades documentadas.

| Uso | Aporte y alcance |
|---|---|
| Resolver prácticas | Editor de notebooks y Python en el navegador; no requiere instalación del estudiante. Se distribuyen las 13 prácticas y se prueba la 01. |
| Autocomprobación | `unittest` de biblioteca estándar; salida de cada test y resumen comprensible dentro del notebook. No hay envío ni protección de tests. |
| Experimentación | La copia modificada se guarda en el navegador y no modifica los originales del servidor. |
| Archivos pequeños | La documentación describe carga y sincronización del sistema de archivos. No se añaden datos porque sumar no los necesita; esta actividad no verifica carga/lectura. |
| Guardar y exportar | Guardado en almacenamiento del navegador y descarga de notebook; se comprueban la recarga y la conservación del código exportado. |

## Fuentes oficiales y alcance documental

- [Contenido y copias locales](https://jupyterlite.readthedocs.io/en/stable/howto/content/files.html): distinción entre archivos publicados y archivos modificados en almacenamiento del navegador. Una copia puede ocultar actualizaciones del servidor.
- [Almacenamiento](https://jupyterlite.readthedocs.io/en/stable/howto/configure/storage.html): controladores persistentes disponibles; normalmente IndexedDB y separación por ruta base. No es una copia de seguridad.
- [GitHub Pages](https://jupyterlite.readthedocs.io/en/stable/howto/deployment/github-pages.html): alojamiento estático de JupyterLite y reconstrucción de cambios. En esta plantilla se usa la publicación Quarto heredada, no el workflow de la demo.
- [Kernel Pyodide y matriz de compatibilidad](https://jupyterlite-pyodide-kernel.readthedocs.io/en/stable/): la familia 0.8 del kernel se corresponde con Core 0.8.
- [Restricciones de Python en WebAssembly](https://pyodide.org/en/stable/usage/wasm-constraints.html): límites de procesos, red, sistema de archivos y módulos nativos frente a CPython local.
- [Acceso a archivos desde el kernel](https://jupyterlite.readthedocs.io/en/stable/howto/content/python.html): sincronización de archivos y alternativas de acceso.

La configuración funciona con recursos estáticos y no exige encabezados COOP/COEP adicionales para el ejemplo probado. HTTPS o localhost son apropiados para el service worker; no se valida abrir desde file://. No se presupone interrupción fiable de código que bloquee ni soporte de bibliotecas nativas arbitrarias. La actividad usa únicamente Python básico y `unittest`.

Los ficheros originales se sirven desde `lite/files/`. Al guardar, el estudiante crea una copia en el almacén de contenidos local. Recargar no reinicia sus archivos guardados, aunque sí pierde las variables del kernel. Las actualizaciones con el mismo nombre pueden quedar ocultas por esa copia: exportar/renombrar el trabajo y retirar solo la copia afectada permite recuperar el original. Este comportamiento de actualización está documentado; no se ha simulado una actualización remota de GitHub Pages en esta entrega.

La prueba de recarga no demuestra persistencia ilimitada, resistencia a borrado de datos ni recuperación tras expulsión de IndexedDB. Tampoco se prometen sincronización entre dispositivos, trabajo sin conexión o entrega centralizada. Los tiempos dependen de red, caché y equipo; las mediciones registradas no son un compromiso de rendimiento.
