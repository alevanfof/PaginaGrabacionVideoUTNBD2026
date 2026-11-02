# -*- coding: utf-8 -*-
"""Genera el audio de cada integrante con Edge TTS.

Cada escena se parte en fragmentos (uno por captura) para que la web pueda
mostrar cada imagen exactamente cuando se la menciona. Salida:

    audio/<alumno>[vX].mp3        audios completos de cada versión
    audio_timing.json             inicio y fin de cada escena y de cada fragmento, con múltiples versiones
    texto_video.txt               texto normalizado que se sintetizó

Uso:  python generar_audio.py [--forzar]
"""

import asyncio
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import edge_tts

import datos

BASE = Path(__file__).resolve().parent
AUDIO_DIR = BASE / "_audio"
OUT_DIR = BASE / "audio"
TIMING = BASE / "audio_timing.json"
TEXT_OUT = BASE / "texto_video.txt"
AUDIO_MANIFEST = BASE / "_audio_manifest.json"

GAP_PARTE_MS = 420      # pausa entre fragmentos de una misma escena
GAP_ESCENA_MS = 900     # pausa entre escenas

FFMPEG = r"C:\ffmpeg\ffmpeg.exe"


def check_ffmpeg():
    """Verificar que ffmpeg esté disponible."""
    try:
        result = subprocess.run([FFMPEG, "-version"], capture_output=True, timeout=5)
        return result.returncode == 0
    except FileNotFoundError:
        print(f"⚠️ No se encontró {FFMPEG}.")
        return False


if not check_ffmpeg():
    print("❌ Error: ffmpeg no disponible para concatenar audios.")
    sys.exit(1)


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
    text = text.replace('"', '').replace("''", '').replace("`", "")
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


def prefijo_version(v):
    """Devuelve el sufijo para el nombre de archivo según la versión."""
    if v == "principal":
        return ""
    elif v == "agudo":
        return "_v2"
    elif v == "grave":
        return "_v3"
    return f"_v{ord(v[0])}"


def RATE_FIX(alumno):
    """Rate fallback por alumno"""
    return "-5%"


def pausa_configurada(seg):
    escena = next(
        (
            e for e in datos.escenas_de(seg["alumno"])
            if e["id"] == seg.get("escena")
        ),
        None,
    )
    if not escena:
        return None
    pausa = escena.get("pausas_despues", {}).get(seg.get("captura"))
    if pausa is None:
        return None
    if isinstance(pausa, dict):
        return pausa
    return {"ms": int(pausa), "mensaje": "Ejecución en vivo"}


def gap_despues(seg, next_seg):
    pausa = pausa_configurada(seg)
    if pausa:
        return int(pausa["ms"])

    cambia_escena = (
        seg["tipo"] == "intro"
        or next_seg["tipo"] == "intro"
        or seg.get("escena") != next_seg.get("escena")
    )
    return GAP_ESCENA_MS if cambia_escena else GAP_PARTE_MS


def construir_segmentos():
    """Lista plana de fragmentos a sintetizar, con su alumno y escena. Soporta múltiples voces por alumno."""
    segs = []
    orden_voces = ["principal", "agudo", "grave"]

    for clave, info in datos.VOCES.items():
        # Usar solo la voz principal si no hay voces_alternativas (compatibilidad retro)
        voces_alternativas = info.get("voces_alternativas", [
            {"id": "principal", "voz": "es-AR-TomasNeural", "pitch": 0, "rate": None, "descripcion": ""}
        ])

        for voz_data in voces_alternativas:
            version = voz_data["id"]
            prefijo = f"_v{orden_voces.index(version) + 1}" if version in orden_voces else "_v1"

            # Intro con la voz seleccionada
            segs.append({
                "alumno": clave,
                "voz": voz_data["voz"],
                "pitch": voz_data.get("pitch", 0),
                "rate": voz_data.get("rate") or RATE_FIX(clave),
                "version": version,
                "id": f"{clave}_intro{prefijo}",
                "tipo": "intro",
                "escena": None,
                "captura": None,
                "texto": normalize(info.get("intro_principal", info.get("intro", ""))),
            })

            # Escenas con la voz seleccionada
            for escena in datos.escenas_de(clave):
                partes = partes_de_escena(escena)
                grupos = escena.get("grupos") or [[]]
                indices_usados = [i for grupo in grupos for i in grupo]
                if sorted(indices_usados) != list(range(len(oraciones_de(escena)))):
                    raise SystemExit(
                        f"{escena['id']}: los grupos no incluyen cada oración exactamente una vez"
                    )
                if len(partes) != len(escena["capturas"]):
                    raise SystemExit(
                        f"{escena['id']}: {len(partes)} fragmentos para "
                        f"{len(escena['capturas'])} capturas"
                    )
                for i, parte in enumerate(partes):
                    segs.append({
                        "alumno": clave,
                        "voz": voz_data["voz"],
                        "pitch": voz_data.get("pitch", 0),
                        "rate": voz_data.get("rate") or RATE_FIX(clave),
                        "version": version,
                        "id": f"{clave}_{escena['id']}_p{i + 1}{prefijo}",
                        "tipo": "escena",
                        "escena": escena["id"],
                        "captura": i,
                        "texto": normalize(parte),
                    })
    return segs


def oraciones_de(escena):
    return re.split(r"(?<=[.!?])\s+", escena["texto"].strip())


def firma_segmento(seg):
    contenido = {
        campo: seg.get(campo)
        for campo in ("id", "texto", "voz", "pitch", "rate", "version")
    }
    serializado = json.dumps(contenido, ensure_ascii=False, sort_keys=True)
    return hashlib.sha256(serializado.encode("utf-8")).hexdigest()


def guardar_manifest(manifest):
    temporal = AUDIO_MANIFEST.with_suffix(".tmp")
    temporal.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    AUDIO_MANIFEST.write_text(temporal.read_text(encoding="utf-8"), encoding="utf-8")
    temporal.unlink(missing_ok=True)


async def sintetizar(seg, destino: Path):
    for intento in range(1, 4):
        try:
            # edge_tts soporta pitch con valor numerico (ej: 100 para +100Hz) o "+100Hz"
            # y rate con porcentaje (ej: "+5%", "-5%")
            pitch_val = seg.get("pitch", 0)
            rate_val = seg.get("rate", "-5%")

            # Convertir pitch numerico a formato Edge TTS si es necesario
            if isinstance(pitch_val, int) and pitch_val != 0:
                pitch_str = f"+{pitch_val}Hz" if pitch_val > 0 else f"{pitch_val}Hz"
            elif not pitch_val or pitch_val == "0Hz":
                pitch_str = None  # No pasar pitch si es 0
            else:
                pitch_str = pitch_val

            comm_kwargs = {
                "text": seg["texto"],
                "voice": seg["voz"],
                "rate": rate_val,
            }
            if pitch_str:
                comm_kwargs["pitch"] = pitch_str

            comm = edge_tts.Communicate(**comm_kwargs)
            await comm.save(str(destino))
            if destino.exists() and destino.stat().st_size > 1000:
                return
        except Exception as e:
            print(f"  intento {intento} falló: {e}", file=sys.stderr)
        await asyncio.sleep(1.5)
    raise RuntimeError(f"No se pudo generar {seg['id']}")


def concat_with_ffmpeg(propio, t_current):
    """Concatena fragmentos usando ffmpeg y agrega gaps."""
    files = []
    for seg in propio:
        path = AUDIO_DIR / f"{seg['id']}.mp3"
        if not path.exists():
            print(f"    ✗ Missing: {path}")
            return None, None

        file_entry = {"path": str(path), "seg": seg}

        # Get duration using ffprobe
        dur_ms = 0.0
        result = subprocess.run(
            [FFMPEG, "-i", str(path)],
            capture_output=True, text=True
        )
        for line in result.stderr.split('\n'):
            if 'Duration:' in line:
                parts = line.split('Duration:')
                if len(parts) > 1:
                    dur_str = parts[1].split(',')[0].strip()
                    h, m_dur, s_dur = dur_str.split(':')
                    dur_ms = (float(h) * 3600 + float(m_dur) * 60 + float(s_dur)) * 1000
                break

        file_entry["dur_ms"] = dur_ms
        files.append(file_entry)

    if not files:
        return None, None

    # Create distinct silence files so each configured pause keeps its duration.
    concat_files = []
    silence_files = []

    for i, fe in enumerate(files):
        concat_files.append(fe["path"])
        pausa = pausa_configurada(fe["seg"])
        if i < len(files) - 1 or pausa:
            gap = (
                gap_despues(fe["seg"], files[i + 1]["seg"])
                if i < len(files) - 1
                else int(pausa["ms"])
            )
            silence_file = BASE / f"_gap_{i:03}.mp3"
            result = subprocess.run([
                FFMPEG, "-y", "-f", "lavfi", "-i", f"aevalsrc=0:d={gap/1000}",
                "-ar", "24000", "-ac", "1", "-c:a", "libmp3lame", "-b:a", "48k",
                str(silence_file)
            ], capture_output=True, text=True)
            if result.returncode != 0:
                raise RuntimeError(f"No se pudo crear una pausa de {gap} ms: {result.stderr[-1000:]}")
            concat_files.append(str(silence_file))
            silence_files.append(silence_file)

    # Write concat file
    concat_file = BASE / "_temp_concat.txt"
    with open(concat_file, "w", encoding="utf-8") as f:
        for cf in concat_files:
            f.write(f"file '{cf}'\n")

    # Concatenate and cleanup temp files
    salida = OUT_DIR / (f"{files[0]['seg']['alumno']}{prefijo_version(files[0]['seg']['version'])}.mp3")

    cmd = [
        FFMPEG, "-y", "-f", "concat", "-safe", "0", "-i", str(concat_file),
        "-c:a", "libmp3lame", "-q:a", "3", str(salida),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"No se pudo concatenar {salida.name}: {result.stderr[-2000:]}")
    if not salida.exists() or salida.stat().st_size < 1000:
        raise RuntimeError(f"El archivo concatenado está vacío o incompleto: {salida}")

    for silence_file in silence_files:
        silence_file.unlink(missing_ok=True)
    concat_file.unlink(missing_ok=True)

    # Build timeline
    intro = None
    escenas = []
    t = 0.0

    for i, fe in enumerate(files):
        seg = fe["seg"]
        dur_ms = fe["dur_ms"]
        inicio, fin = round(t, 3), round(t + dur_ms / 1000.0, 3)

        if seg["tipo"] == "intro":
            intro = {"start": inicio, "end": fin}
        elif seg.get("escena"):
            scene_id = seg["escena"]
            if escenas and escenas[-1]["id"] == scene_id:
                escenas[-1]["end"] = fin
                escenas[-1]["partes"].append({"captura": seg["captura"], "start": inicio, "end": fin})
            else:
                escenas.append({"id": scene_id, "start": inicio, "end": fin, "partes": [{"captura": seg["captura"], "start": inicio, "end": fin}], "pausas": []})

        t += dur_ms / 1000.0

        # Add gap time
        pausa = pausa_configurada(seg)
        if i < len(files) - 1 or pausa:
            gap = (
                gap_despues(seg, files[i + 1]["seg"])
                if i < len(files) - 1
                else int(pausa["ms"])
            )
            if pausa and seg.get("escena"):
                escena_timing = next(
                    escena for escena in escenas if escena["id"] == seg["escena"]
                )
                inicio_pausa = round(t, 3)
                escena_timing["pausas"].append({
                    "start": inicio_pausa,
                    "end": round(inicio_pausa + gap / 1000.0, 3),
                    "mensaje": pausa["mensaje"],
                })
            t += gap / 1000.0

    total = round(t, 3)

    return {
        "archivo": str(salida.relative_to(BASE)),
        "total": total,
        "intro": intro,
        "escenas": escenas,
    }, files[0]["seg"]["alumno"]


def concatenar(segs, alumno, version="principal"):
    """Une los fragmentos de un alumno para una versión específica usando ffmpeg concat."""
    propio = [s for s in segs if s["alumno"] == alumno and s.get("version") == version]
    if not propio:
        print(f"  ✗ Warning: no segments for {alumno} v{version}")
        return None

    result, alumn = concat_with_ffmpeg(propio, 0.0)
    return result


async def main(forzar):
    segs = construir_segmentos()
    total_palabras = sum(len(s["texto"].split()) for s in segs)

    # Asegurar que el directorio existe
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Directorio de audio: {AUDIO_DIR.resolve()}")

    print(f"Fragmentos: {len(segs)} | palabras: {total_palabras}")

    manifest = {}
    if AUDIO_MANIFEST.exists():
        manifest = json.loads(AUDIO_MANIFEST.read_text(encoding="utf-8"))

    for s in segs:
        destino = AUDIO_DIR / f"{s['id']}.mp3"
        firma = firma_segmento(s)
        reutilizable = (
            not forzar
            and destino.exists()
            and destino.stat().st_size >= 1000
            and manifest.get(s["id"]) == firma
        )
        if not reutilizable:
            print(f"  generando {s['id']} ({s.get('version', 'v1')} | {len(s['texto'].split())} pal)...")
            await sintetizar(s, destino)
            manifest[s["id"]] = firma
            guardar_manifest(manifest)
        else:
            print(f"  reutilizando {s['id']}")

    timing = {"rate": "-5%", "alumnos": {}, "voces_disponibles": ["principal", "agudo", "grave"]}

    for clave in datos.VOCES.keys():
        print(f"\nProcesando {clave}...")

        for version in ["principal", "agudo", "grave"]:
            res = concatenar(segs, clave, version)
            if res:
                timing["alumnos"][clave] = {
                    **timing.get("alumnos", {}).get(clave, {}),
                    version: res,
                    "voces_disponibles": ["principal", "agudo", "grave"],
                }

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    with open(TIMING, "w", encoding="utf-8") as f:
        json.dump(timing, f, indent=2, ensure_ascii=False)

    print(f"\nGuion {TEXT_OUT}:")
    guion = []
    for clave, info in datos.VOCES.items():
        guion.append(info["nombre"])
        guion.append("=" * len(info["nombre"]))
        for seg in segs:
            if seg["alumno"] == clave and seg["version"] == "principal":
                etiqueta = "Presentación" if seg["tipo"] == "intro" else (
                    f"{seg['escena']} · captura {seg['captura'] + 1}"
                )
                guion.append(f"\n[{etiqueta}]\n{seg['texto']}")
        guion.append("")
    TEXT_OUT.write_text("\n".join(guion), encoding="utf-8")

    print(f"Timing guardado en {TIMING}")


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--forzar", action="store_true")
    a = p.parse_args()

    asyncio.run(main(a.forzar))
