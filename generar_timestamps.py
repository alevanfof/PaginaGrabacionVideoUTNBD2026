#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera el guión con timestamps detallados usando Whisper para transcribir y cronometrar.

Salida: Guion_With_Timestamps.md - cada frase con inicio/fin en segundos.

Requiere: whisper, ffmpeg, y los audios generados.
"""

import json
import sys
from pathlib import Path
from datetime import datetime

# Forzar UTF-8 para stdout en Windows
if sys.platform == 'win32':
    sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)

BASE = Path(__file__).resolve().parent
TIMING_FILE = BASE / "audio_timing.json"


def transcribir_audio_whisper(audio_path: Path, model_size="medium"):
    """Transcribe un audio usando faster-whisper."""
    try:
        from faster_whisper import WhisperModel
        
        # Detectar GPU disponible y cargar modelo
        device = "cuda" if sys.platform != 'win32' else "auto"
        
        print(f"\n[INFO] Cargando {model_size}...")
        model = WhisperModel(model_size, device=device, compute_type="float16" if sys.platform == 'win32' else "int8")
        
        print(f"[INFO] Transcribiendo {audio_path.name}...")
        
        # Transcribir segmentos más pequeños para mayor precisión
        segments, info = model.transcribe(
            str(audio_path),
            language="es",
            beam_size=5,
            vad_filter=True,
            vad_parameters={"min_silence_duration_ms": 500},
            condition_on_previous_text=False
        )
        
        segmentos = []
        for seg in segments:
            if seg.text.strip():
                segmentos.append({
                    "start": round(seg.start, 3),
                    "end": round(seg.end, 3),
                    "text": seg.text.strip()
                })
        
        print(f"[OK] Transcripción completada: {len(segmentos)} segmentos")
        return segmentos
    
    except Exception as e:
        msg = f"[ERROR] Falló transcripción: {e}"
        print(msg)
        # Fallback: usar whisper tradicional si está disponible
        try:
            return transcribir_legacy_whisper(audio_path)
        except:
            return None


def transcribir_legacy_whisper(audio_path: Path):
    """Fallback para whisper original."""
    print("\n[INFO] Usando fallback con whisper tradicional...")
    import subprocess
    
    result = subprocess.run(
        ["whisper", str(audio_path), "--language", "es", "--task", "transcribe"],
        capture_output=True,
        text=True,
        timeout=600
    )
    
    if result.returncode != 0:
        print(f"[ERROR] Whisper tradicional falló")
        return None
    
    # Parsear output de whisper
    lines = result.stdout.split("\n")
    segmentos = []
    current = {}
    
    for line in lines:
        if "Segment" in line and current.get("text"):
            segmentos.append(current)
            current = {}
        if "start:" in line:
            try: current["start"] = float(line.split(":")[1].strip())
            except: pass
        if "end:" in line:
            try: current["end"] = float(line.split(":")[1].strip())
            except: pass
        if "text:" in line:
            current["text"] = ":".join(line.split(":")[1:]).strip()
    
    if current.get("text"):
        segmentos.append(current)
    
    return segmentos


def generar_timestamped_script():
    """Genera el guión completo con timestamps de todos los audios."""
    with open(TIMING_FILE, "r", encoding="utf-8") as f:
        timing_data = json.load(f)
    
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    output_lines = [
        "# Guion del TFI · Con Timestamps (generado con Whisper)",
        "",
        f"**Fecha de generación:** {ahora}",
        "",
        "---",
        ""
    ]
    
    total_segmentos = 0
    
    for alumno, versiones in timing_data["alumnos"].items():
        # Filtrar solo las versiones reales (no 'voces_disponibles' o keys auxiliares)
        versiones_reales = {k: v for k, v in versiones.items() if isinstance(v, dict) and "archivo" in v}
        
        if not versiones_reales:
            continue
        
        output_lines.extend([
            f"## 👤 {alumno.capitalize()}",
            "",
            "---",
            ""
        ])
        
        for version, data in versiones_reales.items():
            audio_path = BASE / data["archivo"]
            if not audio_path.exists():
                print(f"[WARN] Archivo no existe: {audio_path}")
                continue
            
            segmentos = transcribir_audio_whisper(audio_path)
            if not segmentos:
                print(f"[WARN] No se pudo transcribir {data['archivo']}")
                continue
            
            total_segmentos += len(segmentos)
            
            output_lines.extend([
                f"### 🎤 Versión **{version}**",
                "",
                f"**Duración total:** {data['total']:.2f} segundos",
                ""
            ])
            
            # Tabla de segmentos
            output_lines.append("| Tiempo | Texto |")
            output_lines.append("|--------|-------|")
            
            for i, seg in enumerate(segmentos, 1):
                texto_escaped = seg["text"].replace("|", "\\|").replace("\n", " ")
                output_lines.append(f"| {seg['start']:.2f}-{seg['end']:.2f}s | {texto_escaped} |")
            
            output_lines.append("")
            output_lines.append("")
    
    # Guardar archivo
    output_file = BASE / "Guion_With_Timestamps.md"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(output_lines))
    
    print(f"\n[✅] Guión guardado en {output_file}")
    print(f"[INFO] Total segmentos transcritos: {total_segmentos}")


if __name__ == "__main__":
    import argparse
    
    p = argparse.ArgumentParser()
    p.add_argument("--model", default="medium", help="Modelo whisper (tiny, small, medium, large)")
    args = p.parse_args()
    
    try:
        generar_timestamped_script()
    except KeyboardInterrupt:
        print("\n[INTERRUPT] Cancelado por usuario")
    except Exception as e:
        print(f"[ERROR] Excepción: {e}")
        import traceback
        traceback.print_exc()
