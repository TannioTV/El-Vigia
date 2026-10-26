# El Vigía (sitio público)

Este repositorio es la versión pública de El Vigía, publicada con GitHub Pages desde `main` (carpeta raíz).
No hay paso de compilación: `index.html` lee `data/noticias.json` y `data/ediciones.json` al cargar.

## Publicar una edición

1. Escribe un archivo JSON fuera del repositorio (por ejemplo `/tmp/edicion.json`) con esta forma:
   `{"edicion": {id, fecha, titular, tipo, n_noticias}, "noticias": [ {...nota...}, ... ]}`
   Cada nota usa los mismos campos que en el El Vigía privado: id, edicion_id, fecha, tema, tema_id, hilo,
   titular, bajada, cuerpo, importancia, estado, lugar, datos_clave, cronologia, grafico, fuentes.
2. Ejecuta `python3 scripts/publicar.py /tmp/edicion.json`. El script quita campos privados (leida, guardada),
   reemplaza ids repetidos, ordena por fecha y borra notas de más de 90 días.
3. `git add data && git commit -m "Edición <id>" && git push origin main`.

No edites `index.html` como parte de una publicación de noticias.
No publiques nada que no esté en El Vigía privado y no cambies el campo "estado" de una nota a "confirmado"
si las fuentes no lo confirman.
