---
name: Mentor de Código
description: Tutor socrático de programación con la forma de un chat que el alumno ya sabe usar.
colors:
  tinta: "#0d0d0d"
  tinta-suave: "#5d5d5d"
  lienzo: "#ffffff"
  burbuja: "#f4f4f4"
  lateral: "#f9f9f9"
  hover: "#ececec"
  borde: "#e5e5e5"
  borde-foco: "#c9c9c9"
  codigo-fondo: "#f6f6f6"
  envio-hover: "#333333"
  envio-deshabilitado: "#d7d7d7"
  aviso: "#8a4b00"
  aviso-fondo: "#fff7ed"
  aviso-borde: "#fed7aa"
  aviso-punto: "#d97706"
  ok: "#10a37f"
  seleccion: "#cfe3ff"
typography:
  display:
    fontFamily: "'Segoe UI', system-ui, -apple-system, 'Helvetica Neue', Arial, sans-serif"
    fontSize: "1.85rem"
    fontWeight: 600
    letterSpacing: "-0.02em"
  title:
    fontFamily: "'Segoe UI', system-ui, -apple-system, 'Helvetica Neue', Arial, sans-serif"
    fontSize: "1.05rem"
    fontWeight: 600
  body:
    fontFamily: "'Segoe UI', system-ui, -apple-system, 'Helvetica Neue', Arial, sans-serif"
    fontSize: "1rem"
    fontWeight: 400
    lineHeight: 1.7
  body-sm:
    fontFamily: "'Segoe UI', system-ui, -apple-system, 'Helvetica Neue', Arial, sans-serif"
    fontSize: "0.9rem"
    fontWeight: 400
    lineHeight: 1.45
  label:
    fontFamily: "'Segoe UI', system-ui, -apple-system, 'Helvetica Neue', Arial, sans-serif"
    fontSize: "0.8rem"
    fontWeight: 600
  caption:
    fontFamily: "'Segoe UI', system-ui, -apple-system, 'Helvetica Neue', Arial, sans-serif"
    fontSize: "0.75rem"
    fontWeight: 400
  code:
    fontFamily: "'Cascadia Code', Consolas, 'SF Mono', Menlo, monospace"
    fontSize: "0.875rem"
rounded:
  inline: "0.35rem"
  boton: "0.6rem"
  base: "0.75rem"
  tarjeta: "1rem"
  burbuja: "1.5rem"
  pildora: "1.75rem"
  circulo: "50%"
spacing:
  xs: "0.4rem"
  sm: "0.6rem"
  md: "1rem"
  lg: "1.75rem"
  columna: "48rem"
components:
  compositor:
    backgroundColor: "{colors.lienzo}"
    textColor: "{colors.tinta}"
    rounded: "{rounded.pildora}"
    padding: "0.35rem 0.4rem 0.35rem 0.9rem"
  boton-enviar:
    backgroundColor: "{colors.tinta}"
    textColor: "{colors.lienzo}"
    rounded: "{rounded.circulo}"
    size: "2.25rem"
  boton-enviar-hover:
    backgroundColor: "{colors.envio-hover}"
  boton-enviar-deshabilitado:
    backgroundColor: "{colors.envio-deshabilitado}"
    textColor: "{colors.lienzo}"
  burbuja-alumno:
    backgroundColor: "{colors.burbuja}"
    textColor: "{colors.tinta}"
    rounded: "{rounded.burbuja}"
    padding: "0.65rem 1.15rem"
    width: "min(36rem, 85%)"
  boton-lateral:
    backgroundColor: "transparent"
    textColor: "{colors.tinta}"
    rounded: "{rounded.boton}"
    padding: "0.45rem 0.6rem"
  boton-lateral-hover:
    backgroundColor: "{colors.hover}"
  avatar-mentor:
    backgroundColor: "{colors.lienzo}"
    textColor: "{colors.tinta}"
    rounded: "{rounded.circulo}"
    size: "2rem"
  marca-icono:
    backgroundColor: "{colors.tinta}"
    textColor: "{colors.lienzo}"
    rounded: "{rounded.circulo}"
    size: "2rem"
  tarjeta-error:
    backgroundColor: "{colors.aviso-fondo}"
    textColor: "{colors.tinta}"
    rounded: "{rounded.tarjeta}"
    padding: "1rem 1.15rem"
  paso-numero:
    backgroundColor: "{colors.hover}"
    textColor: "{colors.tinta}"
    typography: "{typography.label}"
    rounded: "{rounded.circulo}"
    size: "1.4rem"
---

# Design System: Mentor de Código

## Overview

**Creative North Star: "La conversación conocida"**

El Mentor viste el canon de ChatGPT, elegido por el usuario y ejecutado sin ironía: lienzo blanco puro, tinta casi negra, una sola columna de lectura y una caja de texto en píldora. El alumno no tiene que aprender una interfaz; ya la conoce. Toda la novedad está en lo que el Mentor responde (preguntas, nunca soluciones), así que la piel se mantiene en silencio: grises neutros, sin color de marca, sin decoración.

La densidad es baja y la lectura manda. El Mentor habla sin burbuja, al ras de la columna, con un avatar de brújula en círculo de borde fino; el alumno habla en una burbuja gris a la derecha. El único color cálido del sistema es el ámbar de los avisos: aparece solo cuando algo falla y siempre trae pasos concretos para arreglarlo. El único movimiento propio es la espera: puntos que laten y, tras 5 s, una nota que explica por qué tarda el modelo.

Construido sobre Streamlit 1.65 en modo claro únicamente (`base = "light"`). Los tokens base viven en `.streamlit/config.toml`; lo que Streamlit no deja configurar vive como variables CSS en la cadena `ESTILOS` de `ui.py`. Las dos apps (`app.py`, `appGemini.py`) comparten esta misma interfaz.

**Key Characteristics:**
- Monocromo neutro: tinta #0d0d0d sobre blanco; el gris hace todo el trabajo de jerarquía.
- Una columna de 48rem; barra lateral gris claro a la izquierda.
- Formas suaves y redondas: píldora, burbuja, círculos; nada de esquinas duras.
- Ámbar reservado para errores amables; verde solo para el punto de "Listo".
- Casi sin sombra: solo la píldora del compositor flota.

## Colors

Una paleta neutra de grises cálidos-neutros sobre blanco, con un único acento semántico (ámbar) para errores y un punto verde de estado.

### Primary
- **Tinta** (tinta): texto, iconos, botón de enviar, círculo de la marca, foco visible. También es `primaryColor`, `textColor` y `linkColor` del tema de Streamlit. No es un acento: es la voz del sistema.

### Neutral
- **Lienzo** (lienzo): fondo de la columna principal, del área inferior (`stBottom`), de la píldora y del avatar del Mentor.
- **Gris burbuja** (burbuja): burbuja del alumno; también `secondaryBackgroundColor` del tema.
- **Gris lateral** (lateral): fondo de la barra lateral.
- **Gris hover** (hover): hover de botones laterales y círculos numerados de "Cómo funciona".
- **Borde** (borde): bordes de 1px de la barra lateral, píldora, avatar y separador de estado; `borderColor` del tema.
- **Borde de foco** (borde-foco): la píldora oscurece su borde a este gris al recibir foco.
- **Tinta suave** (tinta-suave): texto secundario (explicación de bienvenida, consejo, aviso al pie, títulos de sección laterales, nota de espera, puntos de "pensando").
- **Fondo de código** (codigo-fondo): `codeBackgroundColor` de Streamlit para bloques e inline code.

### Semantic
- **Ámbar aviso** (aviso / aviso-fondo / aviso-borde): título y números de pasos, fondo y borde de la tarjeta de error amable. Los bloques de código dentro de la tarjeta vuelven a blanco con borde ámbar.
- **Ámbar de estado** (aviso-punto): punto de estado en la barra lateral cuando hay un problema.
- **Verde listo** (ok): punto de estado "Listo" en la barra lateral. Nunca en botones ni texto.
- **Azul selección** (seleccion): solo `::selection`.

### Named Rules
**The Sin Acento Rule.** No hay color de marca. Las acciones primarias son tinta sobre blanco o blanco sobre tinta; si un nuevo elemento "necesita color" para destacar, la respuesta es peso, tamaño o posición.

**The Ámbar Solo Avisa Rule.** El ámbar aparece únicamente cuando algo falla y viene con instrucciones. Nunca se usa para resaltar, decorar ni marcar contenido normal.

## Typography

**Display Font:** Segoe UI (con system-ui, -apple-system, Helvetica Neue, Arial)
**Body Font:** la misma pila
**Label/Mono Font:** Cascadia Code (con Consolas, SF Mono, Menlo)

**Character:** Una sola familia de sistema, como en el canon de ChatGPT: la tipografía no se nota, el texto sí. El monoespaciado aparece solo en código, porque el código del alumno es contenido de primera clase.

### Hierarchy
- **Display** (600, 1.85rem, -0.02em; 1.6rem en ≤640px): solo el saludo de la pantalla inicial "¿En qué te atoraste hoy?".
- **Title** (600, 1.05rem): nombre de la marca en la barra lateral. El título de la tarjeta de error usa 600 a 1rem.
- **Body** (400, 1rem, 1.7): mensajes del chat y texto del compositor (1.5 en la caja de texto). La columna de 48rem mantiene la línea legible.
- **Body small** (400, 0.9–0.95rem, 1.45–1.55): pasos de "Cómo funciona", texto y pasos del error, línea "pensando".
- **Label** (600, 0.8rem, tinta suave): títulos de sección laterales ("Cómo funciona"), en caja de oración, sin mayúsculas sostenidas.
- **Caption** (400, 0.75–0.85rem, tinta suave): consejo de teclado, aviso al pie, estado del modelo, nota de espera.
- **Code** (0.875rem): bloques de código y código inline.

### Named Rules
**The Una Familia Rule.** Una sola pila sans en todo el sistema; la jerarquía sale de peso (400/500/600) y tamaño, nunca de una segunda familia ni de mayúsculas sostenidas.

## Layout

Columna única centrada (`layout="centered"`, max-width 48rem) con padding superior de 4rem e inferior de 2rem. Barra lateral izquierda que Streamlit abre en laptop y cierra en celular (`initial_sidebar_state="auto"`).

- **Pantalla inicial:** saludo centrado a 22vh del borde superior (6vh en ≤640px), ancho máximo 34rem, y el compositor justo debajo, dentro de un `st.container()` para que no se fije al pie.
- **Conversación:** el compositor se fija abajo (comportamiento nativo de `st.chat_input`); el aviso al pie va en `st.bottom`, centrado.
- **Ritmo:** 1.75rem entre mensajes; 0.85rem entre avatar y texto; sangrías laterales de 0.6rem alineadas en toda la barra lateral (marca, títulos, lista, estado).
- **Barra lateral, de arriba abajo:** marca, "Nueva conversación", "Cómo funciona" (lista numerada), estado del modelo separado por un borde superior.
- **Breakpoint:** uno solo, 640px.

## Elevation & Depth

Plano por defecto. La profundidad se comunica con tonos (blanco contra gris lateral, gris burbuja) y bordes de 1px, no con sombras. La única sombra es la de la píldora del compositor, que la hace flotar sobre el contenido, como en el canon.

### Shadow Vocabulary
- **Píldora flotante** (`box-shadow: 0 2px 10px rgba(13, 13, 13, 0.06), 0 1px 2px rgba(13, 13, 13, 0.04)`): solo la caja de texto.

### Named Rules
**The Una Sola Sombra Rule.** Solo el compositor tiene sombra. Tarjetas, burbujas, avatares y la barra lateral se separan por tono o por borde de 1px.

## Shapes

Lenguaje redondo y suave. Los radios crecen con la escala del elemento: código inline 0.35rem, botones 0.6rem (`buttonRadius`), base de widgets y bloques de código 0.75rem (`baseRadius`), tarjeta de error 1rem, burbuja del alumno 1.5rem, compositor 1.75rem (píldora). Todo lo que es un "objeto" pequeño (avatar, marca, botón de enviar, números de paso, puntos de estado y de espera, cursor de escritura) es un círculo perfecto. Bordes siempre de 1px.

## Components

### Buttons
- **Enviar:** círculo tinta de 2.25rem con flecha blanca dentro de la píldora; hover #333; deshabilitado gris claro con flecha blanca (mientras el Mentor responde o hay un error bloqueante).
- **Laterales ("Nueva conversación"):** fantasma, alineados a la izquierda, icono Material + texto 500; hover con fondo gris hover; foco con contorno de 2px en tinta (offset 1px); deshabilitado en tinta suave cuando no hay conversación.
- **Secundarios en la columna ("Reintentar"):** botón nativo de Streamlit con borde fino y radio de 0.6rem, icono Material a la izquierda.

### Cards / Containers
- **Tarjeta de error amable:** fondo ámbar claro, borde ámbar de 1px, radio 1rem, padding 1rem 1.15rem, `role="alert"`. Título en ámbar 600, explicación, y pasos numerados (número ámbar 600 en columna de 1.4rem). Un paso puede llevar un comando: se muestra con `st.code` justo debajo, con botón de copiar, sobre fondo blanco y borde ámbar. El detalle técnico va aparte en un expander "Detalle técnico (para el equipo)".
- Se implementa con `st.container(key="tarjeta_error")`; Streamlit le asigna la clase `st-key-tarjeta_error`, que es el gancho de estilo.

### Inputs / Fields
- **Compositor en píldora:** fondo blanco, borde 1px, radio 1.75rem, sombra flotante, botón de enviar circular al final. En foco el borde pasa a #c9c9c9 (sin halo de color). El placeholder cambia según el estado ("Escribe tu duda o pega tu código…", "Espera a que el Mentor termine…", "Primero resuelve el aviso de arriba").

### Navigation
- **Barra lateral:** fondo gris lateral con borde derecho de 1px. La marca (círculo tinta de 2rem con brújula SVG + "Mentor de Código") sube a la altura del botón nativo para cerrar la barra. "Cómo funciona" es una lista con números en círculos gris hover de 1.4rem. Al pie, punto de estado (verde "Listo" o ámbar con el título del problema) más backend y modelo en caption.

### Mensajes
- **Alumno:** burbuja gris a la derecha, radio 1.5rem, ancho máximo min(36rem, 85%), sin avatar. El código pegado sin comillas se detecta y se muestra como bloque de código (fondo blanco dentro de la burbuja).
- **Mentor:** sin burbuja, texto al ras de la columna; avatar de brújula Material en círculo blanco de 2rem con borde fino.

### Indicador "pensando" (componente firma)
Tres puntos de 0.4rem en tinta suave que laten (opacidad 0.25→1, 1.2s, desfase 0.15s) junto a "El Mentor está pensando…". A los 5 s aparece en 400ms una nota que explica la espera según el backend. Mientras llega el texto, un cursor circular de 0.55rem en tinta late al final (1s). Con `prefers-reduced-motion` todo queda estático y visible. `role="status"`.

## Do's and Don'ts

### Do:
- **Do** poner los colores, fuentes y radios base en `.streamlit/config.toml` y solo lo que Streamlit no expone en las variables de `ESTILOS`.
- **Do** usar tinta #0d0d0d sobre blanco para toda acción primaria; los estados son grises (hover #ececec, deshabilitado #d7d7d7).
- **Do** escribir cada error como tarjeta de error amable: título, por qué pasó y pasos numerados, con los comandos copiables.
- **Do** mantener redondos los objetos pequeños (avatar, botones de icono, contadores, puntos) y la escala de radios de 0.35rem a 1.75rem.
- **Do** respetar `prefers-reduced-motion` en cualquier animación nueva.
- **Do** apuntar a los elementos de Streamlit por `data-testid` o por la clase `st-key-<key>` de un contenedor con key, nunca por clases generadas (`st-emotion-cache-*`).

### Don't:
- **Don't** introducir un color de marca o acento cromático en botones, enlaces o encabezados.
- **Don't** usar ámbar fuera de errores y del punto de estado con problema.
- **Don't** mostrar trazas de Python al alumno; el detalle técnico va escondido en el expander para el equipo.
- **Don't** agregar sombras a tarjetas, burbujas o la barra lateral; la píldora es la única que flota.
- **Don't** volver al Streamlit por defecto: título grande en la página, avatares de colores, caja de texto plana.
- **Don't** agregar modo oscuro sin definir su paleta completa; el sistema es solo `base = "light"`.
