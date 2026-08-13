"""
Mentor de Código - Prototipo en consola
-----------------------------------------
Este script conecta con Ollama (corriendo localmente) para probar
el prompt socrático antes de meterlo a Streamlit.
"""

import requests  # Librería para hacer peticiones HTTP

# URL local donde Ollama expone su API (se levanta automáticamente al instalar Ollama)
OLLAMA_URL = "http://localhost:11434/api/chat"

# Nombre del modelo que descargaste con "ollama pull llama3.2"
MODEL = "llama3.2"

# El "system prompt" es la instrucción que define el comportamiento del tutor.
# Se manda UNA vez al inicio de la conversación, con role="system".
SYSTEM_PROMPT = (
    "Actua como un mentor de programacion experto que utiliza estrictamente "
    "el metodo socratico. Tu objetivo es guiar a estudiantes de niveles "
    "iniciales en logica de programacion (variables, condicionales, ciclos, "
    "arreglos). REGLAS: "
    "1. TIENES PROHIBIDO entregar codigo de solucion, funciones completas o "
    "corregir el sintaxis directamente. "
    "2. Si el usuario te pide la respuesta o te da un problema, responde con "
    "una pregunta reflexiva o una pista conceptual que lo obligue a pensar. "
    "3. Guia al alumno paso a paso. Si notas que esta completamente perdido, "
    "dale una analogia de la vida real, pero jamas el codigo."
)


def crear_historial():
    """
    Crea la lista de mensajes que se le manda al modelo.
    Cada mensaje es un diccionario con 'role' y 'content'.
    Roles posibles:
      - "system": instrucciones de comportamiento (solo una vez, al inicio)
      - "user": lo que escribe el alumno
      - "assistant": lo que responde el tutor (se va guardando aquí también,
        para que el modelo "recuerde" lo que ya dijo)
    """
    return [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]


def preguntar_al_tutor(historial):
    """
    Manda el historial completo de la conversación a Ollama y regresa
    la respuesta del modelo como texto.

    Se manda el historial COMPLETO cada vez (no solo el último mensaje)
    porque Ollama no tiene memoria propia entre peticiones: la "memoria"
    la maneja quien llama a la API, reenviando todo el contexto.
    """
    payload = {
        "model": MODEL,
        "messages": historial,
        "stream": False  # False = esperamos la respuesta completa de una vez
                          # (más adelante, en Streamlit, se puede usar True
                          # para que el texto aparezca palabra por palabra)
    }

    respuesta = requests.post(OLLAMA_URL, json=payload)
    respuesta.raise_for_status()  # lanza error si algo salió mal (ej. Ollama apagado)

    data = respuesta.json()
    return data["message"]["content"]


def main():
    print("=== Mentor de Código (prototipo consola) ===")
    print("Escribe tu duda de programación. Escribe 'salir' para terminar.\n")

    historial = crear_historial()

    while True:
        pregunta = input("Tú: ")

        if pregunta.lower() == "salir":
            print("¡Hasta luego!")
            break

        # 1. Agregamos la pregunta del alumno al historial
        historial.append({"role": "user", "content": pregunta})

        # 2. Le preguntamos al modelo (mandando TODO el historial)
        respuesta = preguntar_al_tutor(historial)

        # 3. Mostramos la respuesta
        print(f"\nTutor: {respuesta}\n")

        # 4. Guardamos también la respuesta del tutor en el historial,
        #    para que en la siguiente vuelta el modelo recuerde qué dijo
        historial.append({"role": "assistant", "content": respuesta})


if __name__ == "__main__":
    main()