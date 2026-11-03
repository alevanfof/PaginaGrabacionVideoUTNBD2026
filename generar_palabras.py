#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera timestamps por palabra para las nueve pistas de audio."""

import argparse
import json
from pathlib import Path

from faster_whisper import WhisperModel

BASE = Path(__file__).resolve().parent
TIMING_FILE = BASE / "audio_timing.json"
OUTPUT_FILE = BASE / "palabras_timing.json"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="base", help="Modelo faster-whisper")
    args = parser.parse_args()

    timing = json.loads(TIMING_FILE.read_text(encoding="utf-8"))
    model = WhisperModel(args.model, device="cpu", compute_type="int8")
    resultado = {}

    for alumno, datos_alumno in timing["alumnos"].items():
        resultado[alumno] = {}
        for version in ("principal", "agudo", "grave"):
            pista = datos_alumno[version]
            audio = BASE / pista["archivo"]
            print(f"Transcribiendo {alumno}/{version}...", flush=True)
            segmentos, _ = model.transcribe(
                str(audio),
                language="es",
                word_timestamps=True,
                vad_filter=False,
            )
            palabras = [
                {
                    "word": palabra.word.strip(),
                    "start": round(palabra.start, 3),
                    "end": round(palabra.end, 3),
                }
                for segmento in segmentos
                for palabra in (segmento.words or [])
                if palabra.word.strip()
            ]
            if not palabras:
                raise SystemExit(f"No se reconocieron palabras en {audio.name}")
            resultado[alumno][version] = palabras
            print(f"  {len(palabras)} palabras", flush=True)

    OUTPUT_FILE.write_text(
        json.dumps(resultado, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )
    print(f"Marcas guardadas en {OUTPUT_FILE.name}")


if __name__ == "__main__":
    main()
