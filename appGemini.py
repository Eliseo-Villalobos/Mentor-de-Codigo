"""
Mentor de Código - Interfaz Streamlit (backend: Gemini API)
----------------------------------------------------------------
Misma interfaz que app.py (Ollama), pero conectada a Gemini.
"""

import os
import streamlit as st
from google import genai
from google.genai import types

from prompts import SYSTEM_PROMPT  # mismo prompt que la versión de Ollama

MODEL = "gemini-3.1-flash-lite"


# ------------------------------------------------------------------
# CONFIGURACIÓN DE LA PÁGINA
# ------------------------------------------------------------------
st.set_page_config(page_title="Mentor de Código (Gemini)", page_icon="🧭")
st.title("🧭 Mentor de Código — Gemini")
st.caption("Pega tu código o duda. El tutor te guiará con preguntas, no con soluciones.")


# ------------------------------------------------------------------
# CLIENTE Y CHAT (guardados en session_state)
# ------------------------------------------------------------------
# IMPORTANTE: tanto 'client' como 'chat' se guardan en st.session_state,
# no como variables sueltas. Streamlit vuelve a correr TODO el script en
# cada interacción; si 'client' no quedara guardado en session_state,
# se recrearía (o se perdería la referencia) en cada recarga y podríamos
# toparnos con el mismo bug de "client has been closed" que vimos en la
# consola, además de perder la memoria de la conversación.
if "gemini_client" not in st.session_state:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        st.error(
            "No se encontró la variable de entorno GEMINI_API_KEY. "
            "Configúrala con 'setx' en PowerShell y reinicia."
        )
        st.stop()  # detiene la ejecución de la app aquí si no hay API key

    st.session_state.gemini_client = genai.Client(api_key=api_key)

if "chat" not in st.session_state:
    st.session_state.chat = st.session_state.gemini_client.chats.create(
        model=MODEL,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT
        )
    )


# ------------------------------------------------------------------
# MOSTRAR EL HISTORIAL YA EXISTENTE
# ------------------------------------------------------------------
# A diferencia de la versión de Ollama (donde armábamos nuestra propia
# lista 'historial'), aquí le preguntamos directamente al objeto 'chat'
# por su historial con get_history() — Gemini ya lo trae guardado.
for mensaje in st.session_state.chat.get_history():
    rol = "user" if mensaje.role == "user" else "assistant"
    texto = mensaje.parts[0].text
    with st.chat_message(rol):
        st.markdown(texto)


# ------------------------------------------------------------------
# ENTRADA DEL ALUMNO
# ------------------------------------------------------------------
pregunta = st.chat_input("Escribe tu código o tu duda aquí...")

if pregunta:
    with st.chat_message("user"):
        st.markdown(pregunta)

    with st.chat_message("assistant"):
        with st.spinner("El tutor está pensando..."):
            respuesta = st.session_state.chat.send_message(pregunta)
        st.markdown(respuesta.text)

    # No hace falta guardar nada manualmente aquí: chat.send_message()
    # ya actualizó el historial interno del objeto 'chat' por su cuenta.