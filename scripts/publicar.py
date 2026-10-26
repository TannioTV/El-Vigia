#!/usr/bin/env python3
"""Agrega una edición y sus notas a los datos públicos de El Vigía.

Uso:
    python3 scripts/publicar.py ruta/a/edicion.json [más archivos...]

Cada archivo es un objeto JSON con esta forma:
    {
      "edicion": {"id": "e20261026-1500", "fecha": "...", "titular": "...", "tipo": "regular", "n_noticias": 3},
      "noticias": [ {"id": "n20261026-1500-sinaloa", "edicion_id": "e20261026-1500", ...}, ... ]
    }
"edicion" puede omitirse si solo se agregan o corrigen notas.

El script:
  - quita los campos privados (leida, guardada) antes de guardar,
  - reemplaza una nota o edición si ya existe una con el mismo id,
  - ordena todo por fecha (más reciente primero),
  - borra notas con más de DIAS_RETENCION días y ediciones sin notas.
Solo usa la biblioteca estándar de Python.
"""
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DATOS = RAIZ / "data"
DIAS_RETENCION = 90
CAMPOS_PRIVADOS = {"leida", "guardada"}
CAMPOS_NOTA = [
    "id", "edicion_id", "fecha", "tema", "tema_id", "hilo", "titular", "bajada", "cuerpo",
    "importancia", "estado", "lugar", "datos_clave", "cronologia", "grafico", "fuentes",
]
CAMPOS_EDICION = ["id", "fecha", "titular", "tipo", "n_noticias"]


def fecha(valor):
    try:
        d = datetime.fromisoformat(str(valor).replace("Z", "+00:00"))
        return d if d.tzinfo else d.replace(tzinfo=timezone.utc)
    except ValueError:
        return datetime(1970, 1, 1, tzinfo=timezone.utc)


def leer(nombre):
    ruta = DATOS / nombre
    if not ruta.exists():
        return []
    datos = json.loads(ruta.read_text(encoding="utf-8"))
    return datos if isinstance(datos, list) else []


def escribir(nombre, filas):
    DATOS.mkdir(exist_ok=True)
    (DATOS / nombre).write_text(json.dumps(filas, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def limpiar(fila, campos):
    if not isinstance(fila, dict) or not fila.get("id") or not fila.get("fecha"):
        raise ValueError(f"Falta id o fecha en: {str(fila)[:120]}")
    return {k: fila.get(k) for k in campos if k in fila and k not in CAMPOS_PRIVADOS}


def main(archivos):
    if not archivos:
        print(__doc__)
        return 2
    noticias = {n["id"]: n for n in leer("noticias.json") if isinstance(n, dict) and n.get("id")}
    ediciones = {e["id"]: e for e in leer("ediciones.json") if isinstance(e, dict) and e.get("id")}
    nuevas_n = nuevas_e = 0
    for archivo in archivos:
        paquete = json.loads(Path(archivo).read_text(encoding="utf-8"))
        if paquete.get("edicion"):
            e = limpiar(paquete["edicion"], CAMPOS_EDICION)
            ediciones[e["id"]] = e
            nuevas_e += 1
        for nota in paquete.get("noticias") or []:
            n = limpiar(nota, CAMPOS_NOTA)
            noticias[n["id"]] = n
            nuevas_n += 1

    limite = datetime.now(timezone.utc) - timedelta(days=DIAS_RETENCION)
    lista_n = [n for n in noticias.values() if fecha(n["fecha"]) >= limite]
    ids_ed = {n.get("edicion_id") for n in lista_n}
    lista_e = [e for e in ediciones.values() if e["id"] in ids_ed]
    lista_n.sort(key=lambda n: fecha(n["fecha"]), reverse=True)
    lista_e.sort(key=lambda e: fecha(e["fecha"]), reverse=True)

    escribir("noticias.json", lista_n)
    escribir("ediciones.json", lista_e)
    escribir("actualizado.json", [{"fecha": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}])
    print(f"Listo: {nuevas_e} edición(es) y {nuevas_n} nota(s) agregadas. "
          f"Total publicado: {len(lista_n)} notas en {len(lista_e)} ediciones.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
