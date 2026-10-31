# -*- coding: utf-8 -*-
"""Genera el audio de cada integrante con Edge TTS.

Cada escena se parte en fragmentos (uno por captura) para que la web pueda
mostrar cada imagen exactamente cuando se la menciona. Salida:

    audio/<alumno>.mp3        audio completo del bloque
    audio_timing.json         inicio y fin de cada escena y de cada fragmento
    texto_video.txt           texto normalizado que se sintetizó

Uso:  python generar_audio.py [--forzar]
"""

import asyncio
import json
import os
import re
import sys
from pathlib import Path

import edge_tts
from pydub import AudioSegment

import datos

BASE = Path(__file__).resolve().parent
AUDIO_DIR = BASE / "_audio"
OUT_DIR = BASE / "audio"
TIMING = BASE / "audio_timing.json"
TEXT_OUT = BASE / "texto_video.txt"

RATE = "-5%"
GAP_PARTE_MS = 420      # pausa entre fragmentos de una misma escena
GAP_ESCENA_MS = 900     # pausa entre escenas

os.environ["PATH"] = r"C:\ffmpeg" + os.pathsep + os.environ.get("PATH", "")
AudioSegment.converter = r"C:\ffmpeg\ffmpeg.exe"
AudioSegment.ffmpeg = r"C:\ffmpeg\ffmpeg.exe"
AudioSegment.ffprobe = r"C:\ffmpeg\ffprobe.exe"

# Normalización para TTS: siglas y términos que la voz leería mal.
REPS = [
    (r"\bCROSS JOIN\b", "cros yoin"),
    (r"\bGROUP BY\b", "grup bai"),
    (r"\bHAVING\b", "jeiving"),
    (r"\bJOIN\b", "yoin"),
    (r"\bSELECT FOR UPDATE\b", "select for update"),
    (r"\bREPEATABLE READ\b", "ripitabol, rid"),
    (r"\bREAD COMMITTED\b", "rid comited"),
    (r"\bInnoDB\b", "ino de be"),
    (r"\bMySQL\b", "mai ese cu ele"),
    (r"\bCTE\b", "ce te e"),
    (r"\bSQL\b", "ese cu ele"),
    (r"\bVARCHAR\b", "varcar"),
    (r"\bCHECK\b", "chec"),
    (r"\bUNIQUE\b", "iunik"),
    (r"\bON DELETE RESTRICT\b", "on delít ristrict"),
    (r"\bSELECT\b", "select"),
    (r"\bPREPARE\b", "pri peir"),
    (r"\bCOMMIT\b", "comit"),
    (r"\bROLLBACK\b", "rolbac"),
    (r"\bEXPLAIN\b", "expléin"),
    (r"\bCASE\b", "queis"),
    (r"\bMOD\b", "mod"),
    (r"\bDER\b", "de e erre"),
    (r"\bVIP\b", "vi ai pi"),
]


def normalize(text: str) -> str:
    text = text.replace("«", "").replace("»", "").replace("**", "")
    text = text.replace("“", "").replace("”", "").replace("`", "")
    for patron, reemplazo in REPS:
        text = re.sub(patron, reemplazo, text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def partes_de_escena(escena):
    """Devuelve los fragmentos de audio de una escena (uno por captura)."""
    oraciones = re.split(r"(?<=[.!?])\s+", escena["texto"].strip())
    grupos = escena.get("grupos")
    if not grupos:
        grupos = [list(range(len(oraciones)))]
    partes = []
    for grupo in grupos:
        partes.append(" ".join(oraciones[i] for i in grupo))
    return partes


def construir_segmentos():
    """Lista plana de fragmentos a sintetizar, con su alumno y escena."""
    segs = []
    for clave, info in datos.VOCES.items():
        segs.append({
            "alumno": clave,
            "voz": info["voz"],
            "id": f"{clave}_intro",
            "tipo": "intro",
            "escena": None,
            "captura": None,
            "texto": normalize(info["intro"]),
        })
        for escena in datos.escenas_de(clave):
            partes = partes_de_escena(escena)
            if len(partes) != len(escena["capturas"]):
                raise SystemExit(
                    f"{escena['id']}: {len(partes)} fragmentos para "
                    f"{len(escena['capturas'])} capturas"
                )
            for i, parte in enumerate(partes):
                segs.append({
                    "alumno": clave,
                    "voz": info["voz"],
                    "id": f"{clave}_{escena['id']}_p{i + 1}",
                    "tipo": "escena",
                    "escena": escena["id"],
                    "captura": i,
                    "texto": normalize(parte),
                })
    return segs


async def sintetizar(seg, destino: Path):
    for intento in range(1, 4):
        try:
            comm = edge_tts.Communicate(seg["texto"], seg["voz"], rate=RATE)
            await comm.save(str(destino))
            if destino.exists() and destino.stat().st_size > 1000:
                return
        except Exception as e:  # pragma: no cover - red
            print(f"  intento {intento} falló: {e}", file=sys.stderr)
        await asyncio.sleep(1.5)
    raise RuntimeError(f"No se pudo generar {seg['id']}")


def concatenar(segs, alumno):
    """Une los fragmentos de un alumno y devuelve la estructura de tiempos."""
    propios = [s for s in segs if s["alumno"] == alumno]
    final = AudioSegment.silent(duration=0)
    t = 0.0
    intro = None
    escenas = []
    escena_actual = None

    for i, seg in enumerate(propios):
        clip = AudioSegment.from_file(AUDIO_DIR / f"{seg['id']}.mp3", format="mp3")
        dur = len(clip) / 1000.0
        inicio, fin = round(t, 3), round(t + dur, 3)
        final += clip
        t += dur

        if seg["tipo"] == "intro":
            intro = {"start": inicio, "end": fin}
        else:
            if escena_actual is None or escena_actual["id"] != seg["escena"]:
                escena_actual = {"id": seg["escena"], "start": inicio, "end": fin, "partes": []}
                escenas.append(escena_actual)
            escena_actual["end"] = fin
            escena_actual["partes"].append({
                "captura": seg["captura"],
                "start": inicio,
                "end": fin,
            })

        if i < len(propios) - 1:
            siguiente = propios[i + 1]
            gap = GAP_ESCENA_MS if (
                seg["tipo"] == "intro" or siguiente["tipo"] == "intro"
                or seg["escena"] != siguiente["escena"]
            ) else GAP_PARTE_MS
            final += AudioSegment.silent(duration=gap)
            t += gap / 1000.0

    salida = OUT_DIR / f"{alumno}.mp3"
    final.export(str(salida), format="mp3", bitrate="64k")
    return {
        "archivo": f"audio/{alumno}.mp3",
        "total": round(len(final) / 1000.0, 3),
        "intro": intro,
        "escenas": escenas,
    }


async def main():
    forzar = "--forzar" in sys.argv
    AUDIO_DIR.mkdir(exist_ok=True)
    OUT_DIR.mkdir(exist_ok=True)

    segs = construir_segmentos()
    lineas = []
    for s in segs:
        lineas.append(f"[{s['id']}]")
        lineas.append(s["texto"])
        lineas.append("")
    TEXT_OUT.write_text("\n".join(lineas), encoding="utf-8")

    total_palabras = sum(len(s["texto"].split()) for s in segs)
    print(f"Fragmentos: {len(segs)} | palabras: {total_palabras}")

    for s in segs:
        destino = AUDIO_DIR / f"{s['id']}.mp3"
        if forzar or not destino.exists() or destino.stat().st_size < 1000:
            print(f"  generando {s['id']} ({len(s['texto'].split())} pal)...")
            await sintetizar(s, destino)
        else:
            print(f"  reutilizando {s['id']}")

    timing = {"rate": RATE, "alumnos": {}}
    for clave, info in datos.VOCES.items():
        print(f"\nConcatenando {clave}...")
        data = concatenar(segs, clave)
        data.update({
            "nombre": info["nombre"],
            "voz": info["voz"],
            "bloque": info["bloque"],
            "comision": info["comision"],
            "codigo": info["codigo"],
        })
        timing["alumnos"][clave] = data
        m, s = divmod(int(round(data["total"])), 60)
        print(f"  {m}:{s:02d} · intro {data['intro']['start']:.2f}-{data['intro']['end']:.2f}")
        for e in data["escenas"]:
            print(f"  {e['id']}: {e['start']:7.2f} -> {e['end']:7.2f} "
                  f"({len(e['partes'])} fragmentos)")

    TIMING.write_text(json.dumps(timing, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\nEscrito {TIMING.name} y {OUT_DIR.name}/")


if __name__ == "__main__":
    asyncio.run(main())
