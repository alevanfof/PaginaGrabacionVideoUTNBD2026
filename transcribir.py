# -*- coding: utf-8 -*-
"""Transcribe los audios con faster-whisper y deja las marcas de tiempo.

Salida:
    transcripcion.json        segmentos y palabras por integrante
    ScriptConTimestamp.md     guion con marcas mm:ss para revisar la sincronización

Las marcas que usa la web salen de la síntesis (audio_timing.json). Whisper
sirve para verificar que los cortes de escena caigan donde corresponde.
"""

import json
from pathlib import Path

from faster_whisper import WhisperModel

BASE = Path(__file__).resolve().parent
TIMING = BASE / "audio_timing.json"
OUT_JSON = BASE / "transcripcion.json"
OUT_MD = BASE / "ScriptConTimestamp.md"


def mmss(t):
    m, s = divmod(int(round(t)), 60)
    return f"{m:02d}:{s:02d}"


def main():
    timing = json.loads(TIMING.read_text(encoding="utf-8"))
    model = WhisperModel("base", device="cpu", compute_type="int8")

    salida = {}
    lineas = ["# Transcripción con marcas de tiempo", ""]

    for clave, info in timing["alumnos"].items():
        ruta = BASE / info["archivo"]
        print(f"Transcribiendo {clave} ({ruta.name})...")
        segmentos, _ = model.transcribe(
            str(ruta), language="es", word_timestamps=True, vad_filter=False
        )

        segs = []
        for s in segmentos:
            palabras = [
                {"word": w.word, "start": round(w.start, 2), "end": round(w.end, 2)}
                for w in (s.words or [])
            ]
            segs.append({
                "start": round(s.start, 2),
                "end": round(s.end, 2),
                "text": s.text.strip(),
                "words": palabras,
            })

        salida[clave] = {
            "archivo": info["archivo"],
            "total": info["total"],
            "escenas": [
                {"id": e["id"], "start": e["start"], "end": e["end"]}
                for e in info["escenas"]
            ],
            "segments": segs,
        }

        lineas.append(f"## {info['nombre']} · {info['comision']}")
        lineas.append("")
        lineas.append(f"Duración total: **{mmss(info['total'])}**")
        lineas.append("")
        lineas.append("| Escena | Inicio | Fin |")
        lineas.append("|---|---|---|")
        for e in info["escenas"]:
            lineas.append(f"| {e['id']} | {mmss(e['start'])} | {mmss(e['end'])} |")
        lineas.append("")
        for s in segs:
            lineas.append(f"- **{mmss(s['start'])}** {s['text']}")
        lineas.append("")

        # Verificación: cuánto texto de Whisper cae en cada escena.
        print(f"  {len(segs)} segmentos, {mmss(info['total'])}")

    OUT_JSON.write_text(json.dumps(salida, ensure_ascii=False, indent=1), encoding="utf-8")
    OUT_MD.write_text("\n".join(lineas), encoding="utf-8")
    print(f"\nEscrito {OUT_JSON.name} y {OUT_MD.name}")


if __name__ == "__main__":
    main()
