#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Adapta presentacion.html para soportar 3 versiones de audio."""

import json
import re
import shutil
from pathlib import Path

import datos

BASE = Path(__file__).resolve().parent
TIMING_FILE = BASE / "audio_timing.json"
PRESENTACION_HTML = BASE / "presentacion.html"
CAPTURAS_ORIGEN = BASE.parent / "capturas" / "png"
CAPTURAS_DESTINO = BASE / "capturas"

def cargar_timings():
    with open(TIMING_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def armar_datos_web(timing):
    """Construye la presentación con los tiempos y capturas de cada versión."""
    alumnos = {}
    escenas_datos = {escena["id"]: escena for escena in datos.ESCENAS}

    for clave, datos_alumno in datos.VOCES.items():
        info = timing["alumnos"].get(clave)
        if not info:
            raise SystemExit(f"Faltan tiempos para {clave}")

        versiones = {}
        for version in ("principal", "agudo", "grave"):
            tiempo_version = info.get(version)
            if not tiempo_version:
                raise SystemExit(f"Falta la versión {version} de {clave}")

            escenas = []
            for escena_timing in tiempo_version.get("escenas", []):
                escena = escenas_datos.get(escena_timing["id"])
                if escena is None:
                    raise SystemExit(f"No hay metadatos para {escena_timing['id']}")
                escenas.append({
                    **escena_timing,
                    "kicker": escena["kicker"],
                    "titulo": escena["titulo"],
                    "subtitulo": escena["subtitulo"],
                    "capturas": escena["capturas"],
                })
            versiones[version] = {
                "archivo": tiempo_version["archivo"],
                "total": tiempo_version["total"],
                "intro": tiempo_version["intro"],
                "escenas": escenas,
            }

        alumnos[clave] = {
            "nombre": datos_alumno["nombre"],
            "bloque": datos_alumno["bloque"],
            "comision": datos_alumno["comision"],
            "codigo": datos_alumno["codigo"],
            "total": versiones["principal"]["total"],
            "versiones": versiones,
        }
    return {"alumnos": alumnos}


def copiar_capturas(datos_web):
    CAPTURAS_DESTINO.mkdir(exist_ok=True)
    for alumno in datos_web["alumnos"].values():
        for version in alumno["versiones"].values():
            for escena in version["escenas"]:
                for captura in escena["capturas"]:
                    nombre = captura["archivo"]
                    origen = CAPTURAS_ORIGEN / nombre
                    destino = CAPTURAS_DESTINO / nombre
                    if not origen.exists():
                        raise SystemExit(f"Falta la captura requerida: {origen}")
                    if not destino.exists() or destino.stat().st_size != origen.stat().st_size:
                        shutil.copy2(origen, destino)


def main():
    timing = cargar_timings()
    html = PRESENTACION_HTML.read_text(encoding="utf-8")
    match = re.search(r'window\.PRESENTACION\s*=\s*(\{.*?\});', html, re.DOTALL)
    if not match:
        raise SystemExit("No se encontró window.PRESENTACION")

    nuevo_presentacion = armar_datos_web(timing)
    copiar_capturas(nuevo_presentacion)
    html = html.replace(
        match.group(1),
        json.dumps(nuevo_presentacion, ensure_ascii=False, separators=(",", ":")),
    )
    PRESENTACION_HTML.write_text(html, encoding="utf-8")
    print("presentacion.html actualizado con tres variantes sincronizadas")

if __name__ == "__main__":
    main()