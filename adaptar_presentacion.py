#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Adapta presentacion.html para soportar 3 versiones de audio."""

import json
import re
import shutil
import unicodedata
from difflib import SequenceMatcher
from pathlib import Path

import datos

BASE = Path(__file__).resolve().parent
TIMING_FILE = BASE / "audio_timing.json"
WORD_TIMING_FILE = BASE / "palabras_timing.json"
PRESENTACION_HTML = BASE / "presentacion.html"
CAPTURAS_ORIGEN = BASE.parent / "capturas" / "png"
CAPTURAS_DESTINO = BASE / "capturas"

def cargar_timings():
    with open(TIMING_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def normalizar_palabra(texto):
    sin_acentos = unicodedata.normalize("NFD", texto.lower())
    return re.sub(r"[^a-z0-9]", "", "".join(
        caracter for caracter in sin_acentos
        if unicodedata.category(caracter) != "Mn"
    ))

def texto_a_tokens(texto):
    return re.findall(r"\S+", texto)

def alinear_palabras(textos, palabras_audio, duracion):
    tokens = [token for texto in textos for token in texto_a_tokens(texto)]
    reconocidas = [palabra for palabra in palabras_audio if palabra.get("word")]
    if not reconocidas:
        raise SystemExit("La transcripción no contiene palabras alineables")
    clave_tokens = [normalizar_palabra(token) for token in tokens]
    clave_reconocidas = [normalizar_palabra(palabra["word"]) for palabra in reconocidas]
    coincidencias = {}

    comparador = SequenceMatcher(None, clave_tokens, clave_reconocidas, autojunk=False)
    for bloque in comparador.get_matching_blocks():
        for desplazamiento in range(bloque.size):
            indice_token = bloque.a + desplazamiento
            indice_audio = bloque.b + desplazamiento
            coincidencias[indice_token] = {
                "start": float(reconocidas[indice_audio]["start"]),
                "end": float(reconocidas[indice_audio]["end"]),
            }

    indice = 0
    while indice < len(tokens):
        if indice in coincidencias:
            indice += 1
            continue
        inicio_tramo = indice
        while indice < len(tokens) and indice not in coincidencias:
            indice += 1
        fin_tramo = indice
        anterior = inicio_tramo - 1 if inicio_tramo > 0 else None
        siguiente = fin_tramo if fin_tramo < len(tokens) else None
        inicio = coincidencias[anterior]["end"] if anterior is not None else 0.0
        fin = coincidencias[siguiente]["start"] if siguiente is not None else duracion
        if fin < inicio:
            fin = inicio
        tramo = range(inicio_tramo, fin_tramo)
        pesos = [max(1, len(normalizar_palabra(tokens[i]))) for i in tramo]
        peso_total = sum(pesos)
        cursor = inicio
        for i, peso in zip(tramo, pesos):
            fin_palabra = cursor + (fin - inicio) * peso / peso_total
            coincidencias[i] = {"start": cursor, "end": fin_palabra}
            cursor = fin_palabra

    return [
        {"text": token, **coincidencias[indice]}
        for indice, token in enumerate(tokens)
    ]

def adjuntar_tiempos_guion(clave, version, timing, palabras_timing):
    voz = datos.VOCES[clave]
    intro = voz["intro_principal"]
    fuente = [{"texto": intro, "destino": timing["intro"]}]
    escenas_datos = {escena["id"]: escena for escena in datos.ESCENAS}

    for escena_timing in timing["escenas"]:
        escena = escenas_datos[escena_timing["id"]]
        oraciones = re.split(r"(?<=[.!?])\s+", escena["texto"].strip())
        grupos = escena.get("grupos") or [list(range(len(oraciones)))]
        for parte_timing, grupo in zip(escena_timing["partes"], grupos):
            texto = " ".join(oraciones[indice] for indice in grupo)
            fuente.append({"texto": texto, "destino": parte_timing})

    palabras = alinear_palabras(
        [parte["texto"] for parte in fuente],
        palabras_timing[clave][version],
        timing["total"],
    )
    cursor = 0
    for parte in fuente:
        cantidad = len(texto_a_tokens(parte["texto"]))
        parte["destino"]["words"] = palabras[cursor:cursor + cantidad]
        cursor += cantidad
    if cursor != len(palabras):
        raise SystemExit(f"No se pudo alinear el guion completo de {clave}/{version}")
    return intro

def armar_datos_web(timing, palabras_timing):
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

            intro = adjuntar_tiempos_guion(
                clave, version, tiempo_version, palabras_timing
            )
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
                    "texto": escena["texto"],
                    "grupos": escena.get("grupos"),
                    "capturas": escena["capturas"],
                })
            versiones[version] = {
                "archivo": tiempo_version["archivo"],
                "total": tiempo_version["total"],
                "intro": tiempo_version["intro"],
                "introWords": tiempo_version["intro"].get("words", []),
                "escenas": escenas,
            }

        alumnos[clave] = {
            "nombre": datos_alumno["nombre"],
            "bloque": datos_alumno["bloque"],
            "comision": datos_alumno["comision"],
            "codigo": datos_alumno["codigo"],
            "introText": datos_alumno["intro_principal"],
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
    if not WORD_TIMING_FILE.exists():
        raise SystemExit(
            f"Falta {WORD_TIMING_FILE.name}; generá marcas con generar_palabras.py"
        )
    palabras_timing = json.loads(WORD_TIMING_FILE.read_text(encoding="utf-8"))
    html = PRESENTACION_HTML.read_text(encoding="utf-8")
    match = re.search(r'window\.PRESENTACION\s*=\s*(\{.*?\});', html, re.DOTALL)
    if not match:
        raise SystemExit("No se encontró window.PRESENTACION")

    nuevo_presentacion = armar_datos_web(timing, palabras_timing)
    copiar_capturas(nuevo_presentacion)
    html = html.replace(
        match.group(1),
        json.dumps(nuevo_presentacion, ensure_ascii=False, separators=(",", ":")),
    )
    PRESENTACION_HTML.write_text(html, encoding="utf-8")
    print("presentacion.html actualizado con tres variantes sincronizadas")

if __name__ == "__main__":
    main()