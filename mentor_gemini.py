"""
Mentor de Código - Prototipo en consola (backend: Gemini API)
----------------------------------------------------------------
Misma lógica pedagógica que mentor_ollama.py, pero conectado a la
API de Gemini en vez de un modelo local. Usa el objeto Chat del SDK,
que maneja la memoria de conversación automáticamente (no tenemos
que armar la lista de historial a mano como con Ollama).
"""

import os
from google import genai
from google.genai import types

from prompts import SYSTEM_PROMPT  # mismo prompt que usa la versión de Ollama

MODEL = "gemini-3.1-flash-lite"


def crear_chat(client):
    """
    Crea una sesión de chat con Gemini, con el system prompt configurado
    desde el inicio (aquí se manda como 'system_instruction', separado
    de los mensajes normales, a diferencia de Ollama donde iba como un
    mensaje más con role='system').

    Recibe 'client' ya creado desde fuera (en vez de crearlo aquí adentro)
    para evitar un bug conocido de la librería: si el objeto Client se crea
    dentro de una función y no se guarda ninguna referencia a él después,
    Python lo recolecta como basura y cierra la conexión HTTP por debajo,
    aunque sigas usando el objeto 'chat' que sí se regresó.
    """
    chat = client.chats.create(
        model=MODEL,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT
        )
    )
    return chat


def main():
    print("=== Mentor de Código (prototipo consola - Gemini) ===")
    print("Escribe tu duda de programación. Escribe 'salir' para terminar.\n")

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "No se encontró la variable de entorno GEMINI_API_KEY. "
            "Revisa que la configuraste con 'setx' y reiniciaste PowerShell."
        )

    # 'client' se crea aquí, en main(), y se queda vivo durante TODO el
    # programa (mientras el while True siga corriendo) — así ya no se
    # recolecta como basura a medio camino.
    client = genai.Client(api_key=api_key)
    chat = crear_chat(client)

    while True:
        pregunta = input("Tú: ")

        if pregunta.lower() == "salir":
            print("¡Hasta luego!")
            break

        # A diferencia de Ollama, aquí NO mandamos el historial completo
        # a mano: el objeto 'chat' ya lo guarda internamente y lo reenvía
        # solo en cada llamada a send_message.
        respuesta = chat.send_message(pregunta)

        print(f"\nTutor: {respuesta.text}\n")


if __name__ == "__main__":
    main()