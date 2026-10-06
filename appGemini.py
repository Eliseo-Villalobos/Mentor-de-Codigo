"""
Mentor de Código - Interfaz Streamlit (backend: Gemini API)
----------------------------------------------------------------
Misma interfaz que app.py (vive en ui.py), pero conectada a Gemini.
"""

import os

import httpx
import streamlit as st
from google import genai
from google.genai import errors, types

from prompts import SYSTEM_PROMPT  # mismo prompt que la versión de Ollama
from ui import Backend, ErrorAmable, ejecutar_app

MODEL = "gemini-3.1-flash-lite"


def revisar():
    if not os.environ.get("GEMINI_API_KEY"):
        return ErrorAmable(
            "Falta la API key de Gemini",
            "Esta versión del Mentor necesita la variable de entorno `GEMINI_API_KEY`.",
            pasos=[
                ("En PowerShell guarda tu llave (cambia `tu-api-key` por la tuya):",
                 'setx GEMINI_API_KEY "tu-api-key"'),
                "Cierra y vuelve a abrir PowerShell.",
                ("Abre otra vez el Mentor:", "streamlit run appGemini.py"),
            ],
            bloquea=True,
        )
    return None


def _cliente():
    # IMPORTANTE: el 'client' se guarda en st.session_state, no como variable
    # suelta. Streamlit vuelve a correr TODO el script en cada interacción; si
    # no quedara guardado, se recrearía (o se perdería la referencia) y
    # podríamos toparnos con el bug de "client has been closed" que vimos
    # en la consola.
    if "gemini_client" not in st.session_state:
        st.session_state.gemini_client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    return st.session_state.gemini_client


def responder(mensajes):
    """
    A diferencia de la versión anterior (que usaba el objeto 'chat' de Gemini),
    aquí mandamos el historial completo en cada llamada, igual que con Ollama.
    Así "Nueva conversación" y "Reintentar" funcionan igual en ambas versiones.
    Gemini llama "model" a lo que nosotros llamamos "assistant".
    """
    contenido = [
        types.Content(
            role="user" if m["role"] == "user" else "model",
            parts=[types.Part(text=m["content"])],
        )
        for m in mensajes
    ]
    try:
        for pedazo in _cliente().models.generate_content_stream(
            model=MODEL,
            contents=contenido,
            config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
        ):
            if pedazo.text:
                yield pedazo.text
    except errors.APIError as e:
        if e.code == 429:
            raise ErrorAmable(
                "Se acabó la cuota gratuita por ahora",
                "Gemini limita cuántas preguntas se pueden hacer por minuto y por día.",
                pasos=["Espera un minuto y presiona Reintentar."],
                detalle=str(e),
            )
        if e.code in (400, 401, 403) and "API key" in str(e):
            raise ErrorAmable(
                "La API key de Gemini no es válida",
                "Revisa que `GEMINI_API_KEY` tenga la llave correcta y completa.",
                pasos=["Corrige la llave con `setx`.", "Reinicia PowerShell y la app."],
                detalle=str(e),
            )
        raise ErrorAmable(
            "Gemini regresó un error",
            "Intenta de nuevo en un momento.",
            detalle=str(e),
        )
    except (httpx.TransportError, OSError) as e:  # sin internet, DNS, etc.
        raise ErrorAmable(
            "No hay conexión con Gemini",
            "Esta versión necesita internet. Revisa tu conexión.",
            pasos=["Revisa tu conexión a internet.", "Presiona Reintentar."],
            detalle=str(e),
        )


ejecutar_app(
    Backend(
        nombre="Gemini · nube",
        modelo=MODEL,
        responder=responder,
        revisar=revisar,
        nota_espera="Esperando la respuesta de Gemini…",
    )
)
