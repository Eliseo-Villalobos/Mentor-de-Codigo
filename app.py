"""
Mentor de Código - Interfaz Streamlit (backend: Ollama local)
---------------------------------------------------------------
La interfaz vive en ui.py (compartida con appGemini.py). Aquí solo está
cómo hablar con Ollama: mandar la conversación y recibir la respuesta
en pedacitos (streaming), para que aparezca palabra por palabra.
"""

import json
import os

import requests

from prompts import SYSTEM_PROMPT  # mismo prompt que la versión de Gemini
from ui import Backend, ErrorAmable, ejecutar_app

# 127.0.0.1 y no "localhost": en Windows, "localhost" intenta primero IPv6 y
# tarda ~2 s extra en cada petición antes de caer a IPv4, que es donde escucha Ollama.
OLLAMA_BASE = "http://127.0.0.1:11434"
# Todo el equipo debe usar llama3.2 para que las pruebas sean consistentes.
# La variable de entorno solo sirve para probar otro modelo sin tocar el código.
MODEL = os.environ.get("MENTOR_OLLAMA_MODEL", "llama3.2")


def _ollama_apagado(detalle=None):
    return ErrorAmable(
        "Ollama no está respondiendo",
        "El Mentor usa Ollama para correr el modelo en tu computadora, y no lo encontré.",
        pasos=[
            ("Abre la app de Ollama, o corre esto en otra terminal:", "ollama serve"),
            "Espera unos segundos y vuelve a intentarlo.",
        ],
        detalle=detalle,
    )


def _falta_modelo(detalle=None):
    return ErrorAmable(
        f"Falta descargar el modelo {MODEL}",
        "Ollama está funcionando, pero todavía no tiene el modelo que usa el Mentor.",
        pasos=[
            ("En PowerShell corre esto (descarga ~2 GB, solo una vez):", f"ollama pull {MODEL}"),
            "Cuando termine, vuelve a intentarlo.",
        ],
        detalle=detalle,
    )


def revisar():
    """Revisión rápida para el indicador de estado de la barra lateral."""
    try:
        r = requests.get(f"{OLLAMA_BASE}/api/tags", timeout=1.5)
        r.raise_for_status()
    except requests.RequestException:
        return _ollama_apagado()
    instalados = {m["name"].split(":")[0] for m in r.json().get("models", [])}
    if MODEL.split(":")[0] not in instalados:
        return _falta_modelo()
    return None


def responder(mensajes):
    """
    Manda el historial COMPLETO a Ollama (Ollama no tiene memoria propia
    entre peticiones) y va regresando la respuesta en pedacitos.
    """
    payload = {
        "model": MODEL,
        "messages": [{"role": "system", "content": SYSTEM_PROMPT}] + mensajes,
        "stream": True,  # la respuesta llega por partes, una línea JSON por parte
        "options": {
            "num_ctx": 4096  # Aumentamos los tokens para que no se quiebre y olvide las reglas socraticas
        },
    }
    try:
        respuesta = requests.post(
            f"{OLLAMA_BASE}/api/chat", json=payload, stream=True, timeout=(5, 300)
        )
    except requests.ConnectionError as e:
        raise _ollama_apagado(str(e))
    except requests.Timeout as e:
        raise ErrorAmable(
            "El modelo tardó demasiado en contestar",
            "Puede pasar si la computadora tiene poca RAM libre o el modelo apenas se está cargando.",
            pasos=["Cierra programas pesados.", "Presiona Reintentar."],
            detalle=str(e),
        )

    if respuesta.status_code == 404:
        raise _falta_modelo(respuesta.text)
    if not respuesta.ok:
        raise ErrorAmable(
            "Ollama regresó un error",
            "Intenta de nuevo. Si se repite, reinicia la app de Ollama.",
            detalle=f"HTTP {respuesta.status_code}: {respuesta.text}",
        )

    for linea in respuesta.iter_lines():
        if not linea:
            continue
        datos = json.loads(linea)
        if "error" in datos:
            raise ErrorAmable(
                "Ollama regresó un error",
                "Intenta de nuevo. Si se repite, reinicia la app de Ollama.",
                detalle=datos["error"],
            )
        pedazo = datos.get("message", {}).get("content", "")
        if pedazo:
            yield pedazo


ejecutar_app(
    Backend(
        nombre="Ollama · local",
        modelo=MODEL,
        responder=responder,
        revisar=revisar,
        nota_espera="La primera respuesta tarda un poco más mientras el modelo se carga.",
    )
)
