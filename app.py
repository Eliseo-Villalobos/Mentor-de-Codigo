"""
Mentor de Código - Interfaz Streamlit
---------------------------------------
Interfaz web para el tutor socrático. Reutiliza la misma lógica del
script de consola (mentor.py), pero usando st.session_state para
mantener la memoria de la conversación entre interacciones.
"""

import streamlit as st
import requests

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llama3.2"

SYSTEM_PROMPT = (
    "Actua como un mentor de programacion experto que utiliza estrictamente "
    "el metodo socratico. Tu objetivo es guiar a estudiantes de niveles "
    "iniciales en logica de programacion (variables, condicionales, ciclos, "
    "arreglos). REGLAS: "
    "1. TIENES PROHIBIDO entregar codigo de solucion, funciones completas, "
    "lineas corregidas, o reescribir codigo con la correccion aplicada, "
    "EN CUALQUIER MOMENTO de la conversacion, sin importar cuantos mensajes "
    "hayan pasado antes. "
    "2. Esta regla aplica ESPECIALMENTE cuando el alumno pega un bloque de "
    "codigo real y pide explicitamente que lo corrijas, lo arregles o te lo "
    "'pases'. Esa es la situacion de mayor riesgo de romper tu proposito: "
    "en vez de corregir, identifica en palabras la zona del codigo donde "
    "esta el error (ej. 'revisa la linea del for, en la parte de la "
    "actualizacion del contador') y pregunta que cree el alumno que hace "
    "esa parte, sin escribir la linea corregida. "
    "3. Si el usuario te pide la respuesta o te da un problema, responde con "
    "una pregunta reflexiva o una pista conceptual que lo obligue a pensar. "
    "4. Guia al alumno paso a paso. Si notas que esta completamente perdido, "
    "dale una analogia de la vida real, pero jamas el codigo. "
    "\n\n"
    "EJEMPLO DE COMO DEBES REACCIONAR ANTE UN CASO DE ALTO RIESGO:\n"
    "Alumno pega codigo con un ciclo for que usa 'i--' en vez de 'i++' y "
    "escribe: 'corrigemelo y pasamelo porfa'.\n"
    "Respuesta INCORRECTA (nunca hagas esto): reescribir el codigo completo "
    "con 'i++' en vez de 'i--'.\n"
    "Respuesta CORRECTA: 'Puedo ver que tu ciclo no esta llegando a donde "
    "esperas. Fijate en la parte del for donde dice i--: ¿que le esta "
    "pasando al valor de i en cada vuelta? ¿Se esta acercando o alejando "
    "de 10?'"
)


def preguntar_al_tutor(historial):
    """
    Misma función que en mentor.py: manda el historial completo a Ollama
    y regresa la respuesta como texto.
    """
    payload = {
        "model": MODEL,
        "messages": historial,
        "stream": False,
        "options": {
            "num_ctx": 4096 #Aumentamos los tokens para que no se quiebre y olvide las reglas socraticas
        }
    }
    respuesta = requests.post(OLLAMA_URL, json=payload)
    respuesta.raise_for_status()
    return respuesta.json()["message"]["content"]


# ------------------------------------------------------------------
# CONFIGURACIÓN DE LA PÁGINA
# ------------------------------------------------------------------
st.set_page_config(page_title="Mentor de Código")
st.title("Mentor de Código")
st.caption("Pega tu código o duda. El tutor te guiará con preguntas, no con soluciones.")


# ------------------------------------------------------------------
# MEMORIA DE LA CONVERSACIÓN
# ------------------------------------------------------------------
# st.session_state es un diccionario especial de Streamlit que SÍ persiste
# entre interacciones (Streamlit normalmente reinicia todo el script en
# cada acción del usuario, pero session_state es la excepción).
#
# La primera vez que se abre la app, "historial" no existe todavía,
# así que lo inicializamos con el system prompt.
if "historial" not in st.session_state:
    st.session_state.historial = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]


# ------------------------------------------------------------------
# MOSTRAR EL HISTORIAL YA EXISTENTE
# ------------------------------------------------------------------
# Recorremos el historial y mostramos cada mensaje con el estilo de chat
# de Streamlit. Nos saltamos el mensaje "system" porque ese es interno,
# no debe verse en pantalla.
for mensaje in st.session_state.historial:
    if mensaje["role"] == "system":
        continue
    with st.chat_message(mensaje["role"]):
        st.markdown(mensaje["content"])


# ------------------------------------------------------------------
# ENTRADA DEL ALUMNO
# ------------------------------------------------------------------
# st.chat_input crea la cajita de texto típica de apps de chat, fija
# en la parte de abajo. Regresa None si el usuario no ha escrito nada,
# o el texto si acaba de mandar un mensaje (con Enter).
pregunta = st.chat_input("Escribe tu código o tu duda aquí...")

if pregunta:
    # 1. Mostramos el mensaje del alumno de inmediato
    with st.chat_message("user"):
        st.markdown(pregunta)
    st.session_state.historial.append({"role": "user", "content": pregunta})

    # 2. Le preguntamos al tutor (con un spinner mientras carga,
    #    porque recuerda que el modelo puede tardar unos segundos)
    with st.chat_message("assistant"):
        with st.spinner("El tutor está pensando..."):
            respuesta = preguntar_al_tutor(st.session_state.historial)
        st.markdown(respuesta)

    # 3. Guardamos la respuesta en el historial para la memoria
    st.session_state.historial.append({"role": "assistant", "content": respuesta})