#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera guion legible usando los timestamps ya calculados en audio_timing.json."""

import json
from pathlib import Path
from datetime import datetime

BASE = Path(__file__).resolve().parent
TIMING_FILE = BASE / "audio_timing.json"


def format_tiempo(segundos):
    """Convierte segundos a formato mm:ss.ms"""
    minutos = int(segundos // 60)
    segs = segundos % 60
    return f"{minutos:02d}:{segs:05.2f}"


def generar_gui_on_formatado():
    """Genera guion en Markdown desde audio_timing.json."""
    
    with open(TIMING_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    hoy = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    output = []
    
    # Header
    output.append("# 📚 Guión del TFI - Bases de Datos")
    output.append("")
    output.append(f"**Generado:** {hoy}")
    output.append(f"**Rate fijo:** {data['rate']}")
    output.append("")
    output.append("---")
    output.append("")
    
    # Por alumno
    for alumno, versiones in data["alumnos"].items():
        output.extend([
            f"\n## 👤 {alumno.capitalize()}",
            ""
        ])
        
        # Filtrar solo versiones reales
        verdaderas = {k: v for k, v in versiones.items() 
                     if isinstance(v, dict) and "archivo" in v}
        
        for version, info in verdaderas.items():
            total = info.get("total", 0)
            
            output.extend([
                f"\n### 🎤 Versión **{version}**",
                "",
                f"**Archivo:** `{info['archivo']}`",
                f"**Duración total:** {format_tiempo(total)} ({total:.1f}s)",
                ""
            ])
            
            # Escenas
            escenas = info.get("escenas", [])
            
            for i, escena in enumerate(escenas, 1):
                scene_id = escena.get("id", "")
                total_dur = escena["end"] - escena["start"]
                
                output.extend([
                    f"**Escena {i}: {scene_id.upper()}**",
                    f"   • Inicio: {format_tiempo(escena['start'])} | Fin: {format_tiempo(escena['end'])}",
                    f"   • Duración total: {format_tiempo(total_dur)}",
                    ""
                ])
                
                for j, parte in enumerate(escena.get("partes", []), 1):
                    captura = parte.get("captura", j)
                    output.append(f"   `{format_tiempo(parte['start'])}` -> Captura {captura}: " + 
                                 f"{format_tiempo(parte['end'] - parte['start'])}")
                
                output.append("")
            
            output.extend(["", "---", ""])
    
    # Guardar archivo
    salida = BASE / "Guion_Con_Timestamps.md"
    with open(salida, "w", encoding="utf-8") as f:
        f.write("\n".join(output))
    
    print(f"[OK] Guardado en: {salida}")


if __name__ == "__main__":
    try:
        generar_gui_on_formatado()
    except Exception as e:
        print(f"[ERROR] Error: {e}")
        import traceback
        traceback.print_exc()
