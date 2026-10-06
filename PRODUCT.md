# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Estudiantes universitarios de primer semestre (ingeniería / sistemas) en su primer curso de programación. Usan el Mentor fuera de clase, mientras hacen tareas o prácticas: se atoran con un ejercicio o un bug, pegan su código o escriben su duda, y quieren desatorarse. Su tentación natural es pedir la solución directa ("corrígemelo y pásamelo").

## Product Purpose

Mentor de Código es un tutor de IA que guía con el método socrático: responde con preguntas, pistas conceptuales y analogías de la vida real, y **nunca** entrega código de solución, líneas corregidas ni reescrituras. Cubre lógica de programación inicial: variables, condicionales, ciclos y arreglos.

Éxito = el alumno llega por sí mismo a la corrección y entiende por qué, en lugar de copiar una respuesta.

## Positioning

A diferencia de un chatbot general (ChatGPT, Gemini, Copilot), que resuelve el problema por el alumno, el Mentor se niega deliberadamente a hacerlo, incluso cuando el alumno pega código y pide la corrección explícitamente. Señala en palabras la zona del error ("revisa la línea del for, en la actualización del contador") y pregunta qué cree el alumno que hace esa parte. La restricción es el producto.

## Operating Context

- Sesión de chat de una sola conversación: el alumno escribe o pega código, el tutor responde en Markdown.
- Respuestas lentas: la primera respuesta con Ollama tarda ~10–12 s (carga del modelo en RAM); se muestra un estado de espera ("El tutor está pensando...").
- Corre localmente en la computadora del alumno / del equipo (`http://localhost:8501`), en Windows con PowerShell.
- El historial se pierde al recargar la página (limitación conocida del prototipo).

## Capabilities and Constraints

- **Stack:** Python + Streamlit (`st.chat_message`, `st.chat_input`, `st.session_state`). Se queda en Streamlit.
- **Backends (ambos se mantienen):**
  - Ollama local con `llama3.2` (`app.py`, `mentor.py`): sin internet ni API keys; requiere ~8 GB de RAM libres.
  - Gemini API `gemini-3.1-flash-lite` (`appGemini.py`, `mentor_gemini.py`): requiere la variable de entorno `GEMINI_API_KEY`.
- System prompt compartido en `prompts.py`; la interfaz de ambas apps vive en `ui.py`.
- También existen prototipos de consola (`mentor.py`, `mentor_gemini.py`) para probar el prompt.
- Terminología: "Mentor de Código", "tutor", "alumno", "duda".
- Sin decidir: persistencia del historial entre recargas, cuentas de usuario y un selector de backend dentro de la UI.

## Brand Commitments

- Nombre fijo: **Mentor de Código**.
- Toda la interfaz y todas las respuestas del tutor van **100% en español**.
- Referencia de interfaz elegida por el usuario: **ChatGPT** (chat familiar: barra lateral, burbuja del alumno a la derecha, caja de texto en píldora). Se ejecuta de forma directa, sin reinventar el patrón.
- Voz del tutor: cercana, paciente y guía; pregunta antes de afirmar y nunca regaña.
- Copy existente: "Pega tu código o duda. El tutor te guiará con preguntas, no con soluciones." / "Escribe tu código o tu duda aquí..." / "El tutor está pensando..."

## Evidence on Hand

- Guía de instalación para el equipo: `guia-instalacion.md`.
- Ejemplo canónico de caso de alto riesgo (ciclo `for` con `i--`) en `prompts.py`.
- No hay testimonios, métricas de aprendizaje, usuarios reales documentados ni logo. Nada de eso debe inventarse.

## Product Principles

1. **Nunca la respuesta.** Cualquier superficie, copy o función que acerque al alumno a obtener la solución hecha va en contra del producto.
2. **El alumno piensa; el tutor pregunta.** La interfaz debe invitar a explicar y razonar, no solo a pegar y esperar.
3. **Novato primero.** Se asume cero experiencia previa: lenguaje simple, sin jerga técnica innecesaria, sin intimidar.
4. **La espera es parte de la experiencia.** Los modelos tardan; la demora debe sentirse acompañada, no como si algo estuviera roto.
5. **Funciona local y en la nube por igual.** Ninguna decisión debe romper la paridad entre Ollama y Gemini.
