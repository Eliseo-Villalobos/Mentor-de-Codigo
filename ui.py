"""
Mentor de Código - Interfaz compartida
---------------------------------------
Toda la interfaz de chat vive aquí, para que app.py (Ollama) y
appGemini.py (Gemini) se vean y se comporten exactamente igual. Cada
archivo de app solo arma su "Backend" (cómo hablar con su modelo) y
llama a ejecutar_app(backend).

La memoria de la conversación es una lista propia en st.session_state:
    st.session_state.mensajes = [{"role": "user"|"assistant", "content": "..."}]
El system prompt NO va en esta lista: cada backend lo agrega por su cuenta.
"""

import re
from dataclasses import dataclass, field
from typing import Callable, Iterator, Optional

import streamlit as st


# ------------------------------------------------------------------
# PIEZAS QUE CADA BACKEND LE ENTREGA A LA INTERFAZ
# ------------------------------------------------------------------
class ErrorAmable(Exception):
    """
    Error explicado en español para el alumno, en vez de una traza de Python.
    - titulo: qué pasó, en una frase.
    - mensaje: por qué pasó.
    - pasos: qué hacer para arreglarlo, en orden. Cada paso es un texto, o
      un par (texto, comando) cuando hay que correr algo: el comando se
      muestra justo debajo de su paso, con botón para copiar.
    - bloquea: True si la app no puede funcionar en absoluto (ej. falta la
      API key); en ese caso se deshabilita la caja de texto.
    - detalle: el error técnico original, escondido en un desplegable para
      quien lo quiera ver (útil para el equipo, no para el alumno).
    """

    def __init__(self, titulo, mensaje, pasos=None, bloquea=False, detalle=None):
        super().__init__(titulo)
        self.titulo = titulo
        self.mensaje = mensaje
        self.pasos = pasos or []
        self.bloquea = bloquea
        self.detalle = detalle


@dataclass
class Backend:
    nombre: str  # ej. "Ollama · local"
    modelo: str  # ej. "llama3.2"
    # Recibe la conversación y regresa la respuesta en pedacitos (streaming).
    responder: Callable[[list], Iterator[str]]
    # Revisa la configuración; regresa un ErrorAmable o None si todo está bien.
    revisar: Callable[[], Optional[ErrorAmable]] = field(default=lambda: None)
    # Lo que se explica si la respuesta tarda más de unos segundos.
    nota_espera: str = "La respuesta está tardando un poco más de lo normal."


# ------------------------------------------------------------------
# ESTILOS
# ------------------------------------------------------------------
# Los colores base, la fuente y los bordes van en .streamlit/config.toml.
# Aquí solo va lo que Streamlit no deja configurar: el acomodo tipo
# ChatGPT (burbuja del alumno a la derecha, caja de texto en píldora, etc.)
ESTILOS = """
<style>
:root {
  --tinta: #0d0d0d;
  --tinta-suave: #5d5d5d;
  --burbuja: #f4f4f4;
  --lateral: #f9f9f9;
  --hover: #ececec;
  --borde: #e5e5e5;
  --aviso: #8a4b00;
  --aviso-fondo: #fff7ed;
  --aviso-borde: #fed7aa;
  --ok: #10a37f;
}

::selection { background: #cfe3ff; color: var(--tinta); }

/* --- Chrome de Streamlit: lo dejamos casi invisible --------------- */
header[data-testid="stHeader"] { background: transparent; }
[data-testid="stDecoration"], [data-testid="stStatusWidget"] { display: none; }
.stMain [data-testid="stMainBlockContainer"] {
  max-width: 48rem;
  padding-top: 4rem;
  padding-bottom: 2rem;
}

/* --- Barra lateral ----------------------------------------------- */
[data-testid="stSidebar"] { background: var(--lateral); border-right: 1px solid var(--borde); }
[data-testid="stSidebarContent"] { display: flex; flex-direction: column; }
[data-testid="stSidebarUserContent"] { padding-top: 0; }
/* La marca sube a la altura del botón para cerrar la barra, como en ChatGPT */
.marca-fila { margin-top: -3.1rem; }
.marca { display: flex; align-items: center; gap: 0.6rem; margin: 0 0 1rem 0.6rem; height: 2.25rem; }
.marca-icono {
  width: 2rem; height: 2rem; border-radius: 50%;
  background: var(--tinta); color: #fff;
  display: grid; place-items: center; flex: none;
}
.marca-nombre { font-weight: 600; font-size: 1.05rem; color: var(--tinta); }
[data-testid="stSidebar"] .stButton button {
  justify-content: flex-start;
  background: transparent;
  border: 1px solid transparent;
  color: var(--tinta);
  font-weight: 500;
  padding: 0.45rem 0.6rem;
  transition: background-color 120ms ease-out;
}
[data-testid="stSidebar"] .stButton button > div { width: 100%; justify-content: flex-start; }
[data-testid="stSidebar"] .stButton button:disabled { color: var(--tinta-suave); background: transparent; }
[data-testid="stSidebar"] .stButton button:hover { background: var(--hover); color: var(--tinta); }
[data-testid="stSidebar"] .stButton button:focus-visible { outline: 2px solid var(--tinta); outline-offset: 1px; }
.lateral-titulo {
  font-size: 0.8rem; font-weight: 600; color: var(--tinta-suave);
  margin: 1.25rem 0 0.5rem 0.6rem;
}
.como-funciona { list-style: none; margin: 0; padding: 0 0.6rem; counter-reset: paso; }
.como-funciona li {
  counter-increment: paso;
  display: grid; grid-template-columns: 1.4rem 1fr; gap: 0.4rem;
  font-size: 0.9rem; line-height: 1.45; color: var(--tinta);
  margin: 0 0 0.65rem; padding: 0;
}
.como-funciona li::before {
  content: counter(paso);
  width: 1.4rem; height: 1.4rem; border-radius: 50%;
  background: var(--hover); color: var(--tinta);
  font-size: 0.75rem; font-weight: 600;
  display: grid; place-items: center;
}
.estado {
  display: flex; align-items: flex-start; gap: 0.55rem;
  margin: 1.5rem 0.6rem 0; padding-top: 1rem; border-top: 1px solid var(--borde);
  font-size: 0.85rem; line-height: 1.4; color: var(--tinta-suave);
}
.estado b { color: var(--tinta); font-weight: 600; display: block; }
.estado-punto { width: 0.55rem; height: 0.55rem; border-radius: 50%; background: var(--ok); margin-top: 0.4rem; flex: none; }
.estado.problema .estado-punto { background: #d97706; }

/* --- Pantalla inicial -------------------------------------------- */
.bienvenida { text-align: center; margin: 22vh auto 1.75rem; max-width: 34rem; }
.bienvenida-titulo {
  font-size: 1.85rem; font-weight: 600; letter-spacing: -0.02em;
  color: var(--tinta); padding: 0; margin: 0 0 0.6rem;
}
.bienvenida-texto { color: var(--tinta-suave); font-size: 1rem; line-height: 1.55; margin: 0; }
.consejo { text-align: center; color: var(--tinta-suave); font-size: 0.8rem; margin-top: 0.75rem; }

/* --- Mensajes ---------------------------------------------------- */
[data-testid="stChatMessage"] {
  background: transparent;
  padding: 0;
  margin-bottom: 1.75rem;
  gap: 0.85rem;
}
[data-testid="stChatMessageContent"] p,
[data-testid="stChatMessageContent"] li { font-size: 1rem; line-height: 1.7; }

/* Mensaje del alumno: burbuja gris a la derecha, sin avatar */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
  flex-direction: row-reverse;
}
[data-testid="stChatMessageAvatarUser"] { display: none; }
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) [data-testid="stChatMessageContent"] {
  flex: 0 1 auto;
  margin: 0 0 0 auto;
  max-width: min(36rem, 85%);
  background: var(--burbuja);
  border-radius: 1.5rem;
  padding: 0.65rem 1.15rem;
}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) [data-testid="stChatMessageContent"] pre {
  background: #fff;
}

/* Avatar del Mentor: brújula en círculo con borde fino */
[data-testid="stChatMessageAvatarCustom"],
[data-testid="stChatMessageAvatarAssistant"] {
  background: #fff;
  border: 1px solid var(--borde);
  color: var(--tinta);
  border-radius: 50%;
  width: 2rem; height: 2rem;
}

/* Cursor que parpadea mientras llega la respuesta */
.cursor {
  display: inline-block; width: 0.55rem; height: 0.55rem; border-radius: 50%;
  background: var(--tinta); margin-left: 0.2rem; vertical-align: middle;
  animation: latido 1s ease-in-out infinite;
}

/* "El Mentor está pensando..." */
.pensando { display: flex; flex-direction: column; gap: 0.3rem; padding-top: 0.3rem; }
.pensando-linea { display: flex; align-items: center; gap: 0.6rem; color: var(--tinta-suave); font-size: 0.95rem; }
.puntos { display: inline-flex; gap: 0.25rem; }
.puntos i {
  width: 0.4rem; height: 0.4rem; border-radius: 50%; background: var(--tinta-suave);
  animation: latido 1.2s ease-in-out infinite;
}
.puntos i:nth-child(2) { animation-delay: 0.15s; }
.puntos i:nth-child(3) { animation-delay: 0.3s; }
.pensando-nota {
  font-size: 0.85rem; color: var(--tinta-suave);
  opacity: 0; animation: aparecer 400ms ease-out 5s forwards;
}
@keyframes latido { 0%, 100% { opacity: 0.25; } 50% { opacity: 1; } }
@keyframes aparecer { to { opacity: 1; } }

/* --- Tarjeta de error amable ------------------------------------- */
.st-key-tarjeta_error {
  background: var(--aviso-fondo);
  border: 1px solid var(--aviso-borde);
  border-radius: 1rem;
  padding: 1rem 1.15rem;
  gap: 0.5rem;
  color: var(--tinta);
}
/* Streamlit le pone margin-bottom negativo al markdown; dentro de la tarjeta lo anulamos */
.st-key-tarjeta_error [data-testid="stMarkdownContainer"] { margin-bottom: 0; }
.st-key-tarjeta_error [data-testid="stCode"] pre { background: #fff; border: 1px solid var(--aviso-borde); }
.error-titulo { font-size: 1rem; font-weight: 600; color: var(--aviso); margin-bottom: 0.2rem; }
.error-texto { font-size: 0.95rem; line-height: 1.55; }
.error-paso { display: grid; grid-template-columns: 1.4rem 1fr; gap: 0.4rem; font-size: 0.95rem; line-height: 1.55; }
.error-paso-num { font-weight: 600; color: var(--aviso); }
.error-texto code, .error-paso code { white-space: nowrap; background: #fff; border: 1px solid var(--aviso-borde); border-radius: 0.35rem; padding: 0.05rem 0.35rem; }

/* --- Caja de texto en píldora, estilo ChatGPT -------------------- */
[data-testid="stChatInput"] > div {
  border-radius: 1.75rem;
  border: 1px solid var(--borde);
  background: #fff;
  box-shadow: 0 2px 10px rgba(13, 13, 13, 0.06), 0 1px 2px rgba(13, 13, 13, 0.04);
  padding: 0.35rem 0.4rem 0.35rem 0.9rem;
}
[data-testid="stChatInput"] > div:focus-within { border-color: #c9c9c9; }
[data-testid="stChatInput"] textarea { font-size: 1rem; line-height: 1.5; caret-color: var(--tinta); }
[data-testid="stChatInputSubmitButton"] {
  background: var(--tinta);
  color: #fff;
  border-radius: 50%;
  width: 2.25rem; height: 2.25rem; min-width: 2.25rem;
}
[data-testid="stChatInputSubmitButton"]:hover { background: #333; color: #fff; }
[data-testid="stChatInputSubmitButton"]:disabled { background: #d7d7d7; color: #fff; }
[data-testid="stBottom"] > div { background: #fff; }
.aviso-pie { text-align: center; color: var(--tinta-suave); font-size: 0.75rem; margin: 0.4rem 0 0; }

/* --- Bloques de código ------------------------------------------- */
[data-testid="stCode"] pre, .stCodeBlock pre { border-radius: 0.75rem; }

@media (max-width: 640px) {
  .bienvenida { margin-top: 6vh; }
  .bienvenida-titulo { font-size: 1.6rem; }
}

@media (prefers-reduced-motion: reduce) {
  .cursor, .puntos i { animation: none; opacity: 1; }
  .pensando-nota { animation: none; opacity: 1; }
}
</style>
"""

ICONO_MENTOR = ":material/explore:"

SVG_BRUJULA = (
    '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
    'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
    '<circle cx="12" cy="12" r="9"/><path d="m15.5 8.5-2 5-5 2 2-5z"/></svg>'
)


# ------------------------------------------------------------------
# DETECTAR CÓDIGO PEGADO
# ------------------------------------------------------------------
# Si el alumno pega código sin las comillas ``` de Markdown, Streamlit lo
# mostraría como texto normal: se pierde la sangría y los * o _ se vuelven
# cursivas. Aquí detectamos qué líneas parecen código y las envolvemos en
# un bloque de código, SOLO para mostrarlo. Al modelo le llega el texto
# original, tal cual lo escribió el alumno.
_PATRON_CODIGO = re.compile(
    r"[;{}]\s*$"                                   # termina en ; { }
    r"|^\s{2,}\S"                                  # tiene sangría
    r"|^\s*(for|while|if|elif|else|def|return|print|printf|int|float|"
    r"double|char|string|bool|var|let|const|function|public|private|"
    r"class|import|from|#include|using|cout|cin|System\.out)\b"
    r"|==|!=|\+\+|--|<=|>=|\+=|-="
    r"|^\s*[A-Za-z_]\w*(\[.*\])?\s*=\s*\S"          # asignación: x = 5
    r"|\w+\(.*\)\s*:?\s*$"                          # llamada o def ... :
)


def _parece_codigo(linea):
    return bool(linea.strip()) and bool(_PATRON_CODIGO.search(linea))


def _adivinar_lenguaje(codigo):
    if re.search(r"#include|printf|scanf", codigo):
        return "c"
    if re.search(r"cout|cin|std::", codigo):
        return "cpp"
    if "System.out" in codigo or re.search(r"public\s+(static|class)", codigo):
        return "java"
    if re.search(r"console\.log|\b(let|const|function)\b|=>", codigo):
        return "javascript"
    if re.search(r"^\s*(def|elif|print\()|:\s*$|\brange\(", codigo, re.M):
        return "python"
    return ""


def formatear_mensaje_alumno(texto):
    if "```" in texto:
        return texto  # el alumno ya lo formateó él mismo
    lineas = texto.splitlines()
    marcadas = [i for i, linea in enumerate(lineas) if _parece_codigo(linea)]
    # Una sola línea "con pinta de código" en un mensaje corto suele ser
    # una frase normal ("si x = 5 por qué..."), así que pedimos al menos 2,
    # o una sola línea que claramente termine en ; { o }.
    if not marcadas or (len(marcadas) < 2 and not re.search(r"[;{}]\s*$", lineas[marcadas[0]])):
        return texto
    inicio, fin = marcadas[0], marcadas[-1]
    antes = "\n".join(lineas[:inicio]).strip()
    codigo = "\n".join(lineas[inicio : fin + 1])
    despues = "\n".join(lineas[fin + 1 :]).strip()
    partes = []
    if antes:
        partes.append(antes)
    partes.append(f"```{_adivinar_lenguaje(codigo)}\n{codigo}\n```")
    if despues:
        partes.append(despues)
    return "\n\n".join(partes)


# ------------------------------------------------------------------
# PIEZAS DE LA PANTALLA
# ------------------------------------------------------------------
def _html(contenido):
    st.markdown(contenido, unsafe_allow_html=True)


def _escapar(texto):
    return texto.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _con_codigo(texto):
    """Convierte `algo` en <code>algo</code> dentro de los textos de error."""
    return re.sub(r"`([^`]+)`", r"<code>\1</code>", _escapar(texto))


def _tarjeta_error(error):
    # Un contenedor con key recibe la clase CSS "st-key-tarjeta_error", así
    # podemos meter bloques de código (con botón de copiar) DENTRO de la tarjeta.
    with st.container(key="tarjeta_error"):
        _html(
            f'<div role="alert"><div class="error-titulo">{_escapar(error.titulo)}</div>'
            f'<div class="error-texto">{_con_codigo(error.mensaje)}</div></div>'
        )
        for numero, paso in enumerate(error.pasos, start=1):
            texto, comando = paso if isinstance(paso, tuple) else (paso, None)
            _html(
                f'<div class="error-paso"><span class="error-paso-num">{numero}.</span>'
                f"<span>{_con_codigo(texto)}</span></div>"
            )
            if comando:
                st.code(comando, language=None)
    if error.detalle:
        with st.expander("Detalle técnico (para el equipo)"):
            st.code(error.detalle, language=None)


def _nueva_conversacion():
    st.session_state.mensajes = []
    st.session_state.pendiente = False
    st.session_state.error = None


def _reintentar():
    st.session_state.error = None
    st.session_state.pendiente = True


def _barra_lateral(backend, problema):
    with st.sidebar:
        _html(
            '<div class="marca-fila"><div class="marca">'
            f'<span class="marca-icono">{SVG_BRUJULA}</span>'
            '<span class="marca-nombre">Mentor de Código</span>'
            "</div></div>"
        )
        st.button(
            "Nueva conversación",
            icon=":material/edit_square:",
            on_click=_nueva_conversacion,
            use_container_width=True,
            disabled=not st.session_state.mensajes,
        )
        _html(
            '<div class="lateral-titulo">Cómo funciona</div>'
            '<ol class="como-funciona">'
            "<li>Pega tu código o cuéntame tu duda.</li>"
            "<li>Te respondo con preguntas y pistas, nunca con la solución.</li>"
            "<li>Tú llegas a la respuesta, y así se te queda.</li>"
            "</ol>"
        )
        if problema:
            estado = (
                '<div class="estado problema">'
                '<span class="estado-punto"></span>'
                f"<span><b>{_escapar(problema.titulo)}</b>{backend.nombre} · {backend.modelo}</span>"
                "</div>"
            )
        else:
            estado = (
                '<div class="estado">'
                '<span class="estado-punto"></span>'
                f"<span><b>Listo</b>{backend.nombre} · {backend.modelo}</span>"
                "</div>"
            )
        _html(estado)


def _pensando(nota):
    return (
        '<div class="pensando" role="status">'
        '<span class="pensando-linea"><span class="puntos"><i></i><i></i><i></i></span>'
        "El Mentor está pensando…</span>"
        f'<span class="pensando-nota">{_escapar(nota)}</span>'
        "</div>"
    )


def _generar_respuesta(backend):
    """
    Pide la respuesta al backend y la va mostrando palabra por palabra.
    Mientras no llega el primer pedacito, se ve el indicador de "pensando".
    """
    with st.chat_message("assistant", avatar=ICONO_MENTOR):
        espacio = st.empty()
        espacio.markdown(_pensando(backend.nota_espera), unsafe_allow_html=True)
        texto = ""
        try:
            for pedazo in backend.responder(st.session_state.mensajes):
                texto += pedazo
                espacio.markdown(texto + '<span class="cursor"></span>', unsafe_allow_html=True)
        except ErrorAmable as error:
            espacio.empty()
            st.session_state.error = error
            st.session_state.pendiente = False
            return
        except Exception as error:  # cualquier cosa inesperada
            espacio.empty()
            st.session_state.error = ErrorAmable(
                "Algo salió mal al pedir la respuesta",
                "No es tu culpa. Intenta de nuevo en un momento.",
                detalle=f"{type(error).__name__}: {error}",
            )
            st.session_state.pendiente = False
            return
        espacio.markdown(texto)

    st.session_state.mensajes.append({"role": "assistant", "content": texto})
    st.session_state.pendiente = False


def _guardar_pregunta(pregunta):
    texto = pregunta.strip() if pregunta else ""
    if not texto:
        return
    st.session_state.mensajes.append({"role": "user", "content": texto})
    st.session_state.error = None
    st.session_state.pendiente = True
    st.rerun()


# ------------------------------------------------------------------
# LA APP COMPLETA
# ------------------------------------------------------------------
def ejecutar_app(backend):
    st.set_page_config(
        page_title="Mentor de Código",
        page_icon=ICONO_MENTOR,
        layout="centered",
        initial_sidebar_state="auto",  # abierta en laptop, cerrada en celular
    )
    _html(ESTILOS)

    # st.session_state SÍ persiste entre interacciones (Streamlit vuelve a
    # correr todo el script en cada acción, pero session_state se conserva).
    st.session_state.setdefault("mensajes", [])
    st.session_state.setdefault("pendiente", False)  # ¿falta responder al alumno?
    st.session_state.setdefault("error", None)

    problema = backend.revisar()
    bloqueado = bool(problema and problema.bloquea)
    _barra_lateral(backend, problema)

    # --- Pantalla inicial: saludo y caja de texto al centro ------------
    if not st.session_state.mensajes:
        _html(
            '<div class="bienvenida">'
            '<div class="bienvenida-titulo" role="heading" aria-level="1">¿En qué te atoraste hoy?</div>'
            '<div class="bienvenida-texto">Pega tu código o cuéntame tu duda. No te voy a dar la solución: '
            "te voy a hacer preguntas para que llegues tú a ella.</div>"
            "</div>"
        )
        # Si ya sabemos que algo falla (Ollama apagado, falta la API key...),
        # lo decimos desde el inicio, no hasta que el alumno manda su duda.
        if problema:
            _tarjeta_error(problema)
        # Dentro de un contenedor, st.chat_input se queda en su lugar (al
        # centro) en vez de fijarse hasta abajo de la página.
        with st.container():
            pregunta = st.chat_input(
                "Primero resuelve el aviso de arriba" if bloqueado else "Escribe tu duda o pega tu código…",
                key="entrada",
                disabled=bloqueado,
            )
            if not bloqueado:
                _html('<div class="consejo">Enter para enviar · Shift + Enter para un salto de línea</div>')
        _guardar_pregunta(pregunta)
        return

    # --- Conversación --------------------------------------------------
    for mensaje in st.session_state.mensajes:
        if mensaje["role"] == "user":
            with st.chat_message("user"):
                st.markdown(formatear_mensaje_alumno(mensaje["content"]))
        else:
            with st.chat_message("assistant", avatar=ICONO_MENTOR):
                st.markdown(mensaje["content"])

    # La caja de texto se fija abajo (como en ChatGPT) y se deshabilita
    # mientras el Mentor responde, para no mandar dos preguntas a la vez.
    pregunta = st.chat_input(
        "Espera a que el Mentor termine…" if st.session_state.pendiente else "Responde o pregunta algo más…",
        key="entrada",
        disabled=st.session_state.pendiente or bloqueado,
    )
    with st.bottom:
        _html(
            '<div class="aviso-pie">El Mentor puede equivocarse, y nunca te dará la '
            "solución completa: esa parte te toca a ti.</div>"
        )

    if st.session_state.pendiente:
        _generar_respuesta(backend)
        st.rerun()  # para volver a habilitar la caja de texto

    if st.session_state.error:
        with st.chat_message("assistant", avatar=ICONO_MENTOR):
            _tarjeta_error(st.session_state.error)
            st.button("Reintentar", icon=":material/refresh:", on_click=_reintentar)

    _guardar_pregunta(pregunta)
