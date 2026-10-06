---
version: 1
slug: "ui-py"
primary_target: "ui.py"
related_targets: ["app.py","appGemini.py"]
---

# Chat del Mentor (Streamlit)

Scope: la pantalla única de chat, compartida por `app.py` (Ollama) y `appGemini.py` (Gemini) vía `ui.py`.
Mode: Operate. Tarea: el alumno pega código o escribe su duda, lee la pregunta guía, responde, repite.
Constraints: Streamlit (sin frontend propio), 100% español, demo en laptop frente al profesor.
User-pinned direction: interfaz de ChatGPT como referencia (canon tomado por el usuario; ejecutado sin ironía).
Requested UX: botón nueva conversación, errores amables, mejor manejo de código pegado.

## Direction contract

THESIS: Un chat que cualquier alumno ya sabe usar porque se comporta como ChatGPT, pero cuyo único trabajo es devolver la pregunta. Rechaza el Streamlit por defecto: título grande, avatares de colores, caja de texto plana y trazas de Python como errores.

OWN-WORLD: Blanco puro, tinta #0d0d0d, gris de burbuja #f4f4f4, barra lateral #f9f9f9, bordes #e5e5e5. Segoe UI / system-ui, código en Cascadia Code / Consolas. Burbuja de alumno redondeada a la derecha; mentor sin burbuja, con brújula. Compositor en píldora con botón negro circular.

STORY: El alumno entiende en una línea que el Mentor no da soluciones, pega su código, ve que se respeta su formato, lee una pregunta que aparece palabra por palabra y responde. Si algo falla, sabe exactamente qué hacer.

FIRST VIEWPORT: Barra lateral izquierda (marca, Nueva conversación, Cómo funciona, estado del modelo abajo). Centro vacío: saludo "¿En qué te atoraste hoy?" en el centro óptico, línea de explicación debajo, compositor en píldora centrado justo bajo el saludo; acción primaria = escribir.

FORM: Canon ChatGPT elegido por el usuario (sin roll; no seed key). Movimiento propio: indicador "El Mentor está pensando" que, tras unos segundos, explica la carga del modelo en vez de parecer congelado.

FINISH: unreviewed and undocumented is unfinished; this build ends with the finish review, the verdict, DESIGN.md, and every shipping raster carrying its provenance
