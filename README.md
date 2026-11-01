# TFI · Bases de Datos I · Web de exposición

Presentación para grabar los tres bloques del Trabajo Final Integrador de Bases
de Datos I. Cada integrante elige su bloque y una de las tres versiones de pitch;
la presentación avanza sincronizada con el audio y las capturas.
`index.html` redirige al ingresar al sitio a `presentacion.html`.

No muestra el guion completo. Durante cada demostración aparece una tarjeta
**Ejecución en vivo** con la tarea y el tiempo disponible; se puede pausar con
la barra espaciadora para extenderla.

## Cómo usarla

1. Abrir `presentacion.html` en Chrome, Edge o Firefox.
2. Elegir el bloque de Alejandro, Gabriel o Josue.
3. Grabar la pantalla. La secuencia se reproduce completa y se detiene al final.

La ruedita de la esquina inferior derecha permite elegir el pitch pregrabado y
ajustar la velocidad. La duración estimada de cada bloque y la suma de los tres
se actualizan con esos ajustes. `Esc` vuelve al selector.

Los audios de Edge TTS son guías para grabar y no deben incluirse en el video
final: el checklist del guion pide voces reales. Las pausas silenciosas dejan
tiempo para ejecutar las consultas y demostraciones en vivo.

## Bloques

| Integrante | Comisión | Duración | Contenido |
|---|---|---|---|
| Alejandro Fernández | C2-3 | 3:40 | Sistema, modelo de datos e índices |
| Gabriel Di Lorenzo | C2-3 | 3:51 | Carga masiva, consultas y roles |
| Josue Gallardo | C2-12 | 3:58 | Seguridad, transacciones y concurrencia |

Las tres guías principales suman 11:29, incluidas 205 segundos de pausas de
ejecución repartidas entre los integrantes. Las variantes aguda y grave suman
11:21 y 11:39, respectivamente.

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
├─ index.html             punto de entrada para Vercel
├─ presentacion.html      web final
├─ audio/                 MP3 por integrante y variante
└─ capturas/              capturas usadas por la presentación
```

## Regenerar

Requisitos: Python 3.12, `edge-tts`, `pydub`, `faster-whisper` y FFmpeg en
`C:\ffmpeg` (o en el `PATH`).

```bash
python generar_audio.py       # sintetiza las tres variantes y actualiza audio_timing.json
python adaptar_presentacion.py
python check_duracion.py      # comprueba objetivo de 11–12 min y velocidades
```

`generar_audio.py` reutiliza los fragmentos cuyo texto y configuración no
cambiaron. Para forzar una nueva síntesis completa: `python generar_audio.py --forzar`.

## Cómo funciona la sincronización

El audio se sintetiza en fragmentos: uno por captura. `audio_timing.json`
registra los tiempos de cada variante, incluidas las pausas de ejecución.
`adaptar_presentacion.py` actualiza las diapositivas para que sigan esos tiempos.

## Publicar en Vercel

Importar este repositorio y configurar **Root Directory** como `./` (la raíz del
repositorio). Es un sitio estático: no necesita comando de build. `index.html`
redirige la ruta raíz `/` a la presentación. Después del despliegue, se puede
abrir tanto la URL del sitio como `/presentacion.html`.

## Ajustes de voz

- Velocidad: 0,80× a 1,10×; el cálculo del tiempo total refleja la velocidad.
- Pitch: principal, agudo o grave, generado por separado con Edge TTS.
- Se guardan en `localStorage` con la clave `tfi-voz`.

Las tres voces son de Edge TTS, con velocidad base `-5%`:

- Alejandro: `es-AR-TomasNeural`
- Gabriel: `es-CO-GonzaloNeural`
- Josue: `es-MX-JorgeNeural`
