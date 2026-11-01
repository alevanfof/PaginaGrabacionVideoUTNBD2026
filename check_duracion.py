#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Comprueba la duración conjunta de las guías de audio por variante de pitch."""

import json
from pathlib import Path
import sys

BASE = Path(__file__).resolve().parent
TIMING_FILE = BASE / "audio_timing.json"
OBJETIVO_MIN_SEGUNDOS = 11 * 60
OBJETIVO_MAX_SEGUNDOS = 12 * 60
MINIMO_FINAL_SEGUNDOS = 10 * 60
MAXIMO_FINAL_SEGUNDOS = 15 * 60
VERSIONES = ("principal", "agudo", "grave")
VELOCIDADES = (0.8, 1.0, 1.1)


def formato(total):
    segundos = round(total)
    return f"{segundos // 60}:{segundos % 60:02d}"


def main():
    data = json.loads(TIMING_FILE.read_text(encoding="utf-8"))
    duraciones = {}

    for version in VERSIONES:
        duraciones[version] = {
            alumno: float(info[version]["total"])
            for alumno, info in data["alumnos"].items()
        }
        total = sum(duraciones[version].values())
        objetivo_ok = OBJETIVO_MIN_SEGUNDOS <= total <= OBJETIVO_MAX_SEGUNDOS
        print(
            f"{version}: {formato(total)} total — "
            f"{'OK' if objetivo_ok else 'FUERA DEL OBJETIVO 11–12 MIN'}"
        )
        for alumno, duracion in duraciones[version].items():
            print(f"  {alumno}: {formato(duracion)}")
        for velocidad in VELOCIDADES:
            duracion_reproduccion = total / velocidad
            print(
                f"  a {velocidad:.2f}×: "
                f"{formato(duracion_reproduccion)} de reproducción"
            )
            if not MINIMO_FINAL_SEGUNDOS <= duracion_reproduccion <= MAXIMO_FINAL_SEGUNDOS:
                print("    ADVERTENCIA: fuera del rango final de 10–15 minutos.")

    if any(
        not OBJETIVO_MIN_SEGUNDOS <= sum(duraciones[v].values()) <= OBJETIVO_MAX_SEGUNDOS
        for v in VERSIONES
    ):
        sys.exit("Al menos una variante queda fuera del objetivo de 11–12 minutos.")
    if any(
        not MINIMO_FINAL_SEGUNDOS
        <= sum(duraciones[v].values()) / velocidad
        <= MAXIMO_FINAL_SEGUNDOS
        for v in VERSIONES
        for velocidad in VELOCIDADES
    ):
        sys.exit("Al menos una velocidad queda fuera del rango final de 10–15 minutos.")


if __name__ == "__main__":
    main()
