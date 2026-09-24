"""
Prueba mínima de conexión con Gemini API.
Solo confirma que la API key funciona antes de integrarlo al proyecto completo.
"""

import os
from google import genai

# Leemos la API key desde la variable de entorno
# Ojo la API key nunca debe de declararse en el programa
api_key = os.environ.get("GEMINI_API_KEY") # de esta manera nunca queda escrita y no se sube a git

if not api_key:
    print("ERROR: no se encontró la variable de entorno GEMINI_API_KEY.")
    print("Revisa que hayas corrido 'setx' y reiniciado PowerShell.")
else:
    # El cliente es el objeto que usamos para hablar con la API de Google
    client = genai.Client(api_key=api_key)

    # Esta parte manda el mensaje usando metodos que trae el SDK de googlem 
    respuesta = client.models.generate_content(
        model="gemini-3.1-flash-lite",  # modelo de prueba 
        contents="Hola, responde solo con: 'Conexión exitosa con Gemini'"
    )

    print(respuesta.text)