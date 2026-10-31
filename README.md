# TFI · Bases de Datos I · Web de exposición

Presentación autocontenida para grabar los tres bloques del Trabajo Final
Integrador de Bases de Datos I. Cada integrante elige su bloque, suena su audio
y la presentación avanza sola: portada, tres escenas con capturas y cierre. Al
terminar el audio, todo se detiene.

No muestra el guion ni indica que hay una grabación en curso: solo títulos,
subtítulos y capturas del sistema funcionando.

## Cómo usarla

1. Abrir `presentacion.html` en Chrome, Edge o Firefox.
2. Elegir el bloque de Alejandro, Gabriel o Josue.
3. Grabar la pantalla. La secuencia se reproduce completa y se detiene al final.

La ruedita de la esquina inferior derecha abre los ajustes de voz (velocidad y
tono). Se guardan en el navegador y no se ven durante la grabación. `Esc` vuelve
al selector.

## Bloques

| Integrante | Comisión | Duración | Contenido |
|---|---|---|---|
| Alejandro Fernández | C2-3 | 3:04 | Sistema, modelo de datos e índices |
| Gabriel Di Lorenzo | C2-3 | 2:26 | Carga masiva, consultas y roles |
| Josue Gallardo | C2-12 | 2:53 | Seguridad, transacciones y concurrencia |

## Estructura

```
webVideoGuion/
├─ datos.py               voces, textos, escenas, grupos y capturas
├─ generar_audio.py       síntesis con Edge TTS y marcas de tiempo
├─ transcribir.py         verificación con faster-whisper
├─ generar_web.py         arma presentacion.html y el audio embebido
├─ plantilla.html         diseño y motor de sincronización
├─ audio_timing.json      inicio/fin de cada escena y fragmento
├─ transcripcion.json     transcripción con palabras y tiempos
├─ ScriptConTimestamp.md  guion con marcas mm:ss (control interno)
├─ presentacion.html      web final
├─ audio/                 MP3 por integrante + audio_data.js (base64)
└─ capturas/              capturas usadas por la presentación
```

## Regenerar

Requisitos: Python 3.12, `edge-tts`, `pydub`, `faster-whisper` y FFmpeg en
`C:\ffmpeg` (o en el `PATH`).

```bash
python generar_audio.py      # sintetiza y arma audio/ + audio_timing.json
python transcribir.py        # verifica la transcripción (opcional)
python generar_web.py        # genera presentacion.html y audio_data.js
```

`generar_audio.py` reutiliza los fragmentos ya sintetizados en `_audio/`. Para
forzar una nueva síntesis completa: `python generar_audio.py --forzar`.

## Cómo funciona la sincronización

El audio se sintetiza en fragmentos: uno por captura. Al concatenarlos se
registran los tiempos exactos de cada escena y de cada fragmento en
`audio_timing.json`. La web usa esos tiempos para cambiar de diapositiva y de
captura, sin depender de estimaciones.

El audio va embebido en base64 (`audio/audio_data.js`) y se reproduce con Web
Audio, lo que permite ajustar velocidad y tono por separado. Si el navegador no
lo permite, cae a un `<audio>` normal y el ajuste de tono se desactiva.

## Ajustes de voz

- Velocidad: 0,75× a 1,25×.
- Tono: −100 a +100 cents.
- Se guardan en `localStorage` con la clave `tfi-voz`.

Las tres voces son de Edge TTS, con velocidad base `-5%`:

- Alejandro: `es-AR-TomasNeural`
- Gabriel: `es-CO-GonzaloNeural`
- Josue: `es-MX-JorgeNeural`
