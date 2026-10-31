# -*- coding: utf-8 -*-
"""Genera la web de grabación a partir de datos.py y audio_timing.json.

Salida:
    presentacion.html      deck con selector de alumno y sincronización
    audio/audio_data.js    audio embebido en base64 (permite ajustar tono)
    capturas/              solo las imágenes que usa la presentación
"""

import base64
import json
import shutil
from pathlib import Path

import datos

BASE = Path(__file__).resolve().parent
TIMING = BASE / "audio_timing.json"
PLANTILLA = BASE / "plantilla.html"
SALIDA = BASE / "presentacion.html"
AUDIO_JS = BASE / "audio" / "audio_data.js"
CAPS_ORIGEN = BASE.parent / "capturas" / "png"
CAPS_DESTINO = BASE / "capturas"


def cargar_timing():
    if not TIMING.exists():
        raise SystemExit("Falta audio_timing.json. Ejecutá primero generar_audio.py")
    return json.loads(TIMING.read_text(encoding="utf-8"))


def armar_datos(timing):
    alumnos = {}
    for clave, info in timing["alumnos"].items():
        escenas = []
        for e in info["escenas"]:
            fuente = next((x for x in datos.ESCENAS if x["id"] == e["id"]), None)
            if fuente is None:
                raise SystemExit(f"No hay datos para la escena {e['id']}")
            escenas.append({
                "id": e["id"],
                "start": e["start"],
                "end": e["end"],
                "kicker": fuente["kicker"],
                "titulo": fuente["titulo"],
                "subtitulo": fuente["subtitulo"],
                "partes": e["partes"],
                "capturas": fuente["capturas"],
            })
        alumnos[clave] = {
            "nombre": info["nombre"],
            "bloque": info["bloque"],
            "comision": info["comision"],
            "codigo": info["codigo"],
            "total": info["total"],
            "intro": info["intro"],
            "escenas": escenas,
        }
    return {"alumnos": alumnos}


def copiar_capturas(datos_web):
    CAPS_DESTINO.mkdir(exist_ok=True)
    usadas = set()
    for alumno in datos_web["alumnos"].values():
        for escena in alumno["escenas"]:
            for cap in escena["capturas"]:
                usadas.add(cap["archivo"])
    for nombre in sorted(usadas):
        origen = CAPS_ORIGEN / nombre
        if not origen.exists():
            raise SystemExit(f"Falta la captura {origen}")
        destino = CAPS_DESTINO / nombre
        if not destino.exists() or destino.stat().st_size != origen.stat().st_size:
            shutil.copy2(origen, destino)
    # Limpiar capturas que ya no se usan.
    for archivo in CAPS_DESTINO.glob("*"):
        if archivo.is_file() and archivo.name not in usadas:
            archivo.unlink()
    return len(usadas)


def generar_audio_js():
    partes = []
    for clave in ("alejandro", "gabriel", "josue"):
        mp3 = BASE / "audio" / f"{clave}.mp3"
        if not mp3.exists():
            raise SystemExit(f"Falta {mp3}")
        partes.append(
            f'  "{clave}": "{base64.b64encode(mp3.read_bytes()).decode("ascii")}"'
        )
    AUDIO_JS.write_text(
        "// Generado por generar_web.py: audio de cada bloque en base64.\n"
        "window.AUDIO_B64 = {\n" + ",\n".join(partes) + "\n};\n",
        encoding="utf-8",
    )
    return AUDIO_JS.stat().st_size


def generar_html(datos_web):
    html = PLANTILLA.read_text(encoding="utf-8")
    marcador = "/*__DATOS__*/ null"
    if marcador not in html:
        raise SystemExit("La plantilla no tiene el marcador /*__DATOS__*/")
    html = html.replace(
        marcador, json.dumps(datos_web, ensure_ascii=False, separators=(",", ":"))
    )
    SALIDA.write_text(html, encoding="utf-8")


def main():
    timing = cargar_timing()
    datos_web = armar_datos(timing)
    n_caps = copiar_capturas(datos_web)
    tam_audio = generar_audio_js()
    generar_html(datos_web)

    print(f"Web generada: {SALIDA.name}")
    print(f"Capturas: {n_caps}")
    print(f"Audio embebido: {tam_audio / 1024 / 1024:.1f} MB")
    for clave, a in datos_web["alumnos"].items():
        m, s = divmod(int(round(a["total"])), 60)
        print(f"  {a['nombre']:22s} {a['codigo']:6s} {m}:{s:02d} · "
              f"{len(a['escenas'])} escenas")


if __name__ == "__main__":
    main()
