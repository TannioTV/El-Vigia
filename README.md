# El Vigía

Resumen automático de noticias seleccionadas, con mapa, datos clave, cronología y fuentes.

Las notas las escribe una IA a partir de medios publicados y se actualizan solas varias veces al día.
Pueden contener errores; consulta siempre las fuentes enlazadas en cada nota.

## Cómo funciona

- `index.html` es la página. Lee las notas de `data/noticias.json` y `data/ediciones.json`.
- `scripts/publicar.py` agrega una edición nueva a esos archivos (ver instrucciones en `CLAUDE.md`).
- La página se sirve con GitHub Pages desde la rama `main`, carpeta raíz.
