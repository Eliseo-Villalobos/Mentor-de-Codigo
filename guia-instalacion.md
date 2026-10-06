# Guía de instalación - Mentor de Código

Esta guía sirve para que cualquiera que quiera tener el programa y poder ejecutarlo bien

## Requisitos previos
- Windows con PowerShell (esta guía está adaptada a PowerShell)
- Python instalado (3.10 o superior recomendado)
- Al menos 8GB de RAM libres (el modelo usado es ligero, pero necesita espacio)

---

## Paso 1: Instalar Ollama

Ollama es el programa que corre el modelo de IA localmente en tu computadora (sin necesidad de internet ni API keys de pago).

1. Descarga el instalador desde: https://ollama.com/download
2. Instálalo como cualquier programa de Windows (siguiente, siguiente, finalizar).
3. Verifica que quedó instalado abriendo PowerShell y corriendo:
   ```powershell
   ollama --version
   ```

## Paso 2: Descargar el modelo

Elegimos `llama3.2` porque es ligero (corre bien incluso en equipos con RAM limitada) y sigue bien las instrucciones del prompt socrático.
(Esto puede cambiar a futuro, considerando las respuestas que nos va dando los modelos de prueba)
```powershell
ollama pull llama3.2
```

Esto descarga ~2GB. Solo se hace una vez.

Para confirmar que funciona, prueba:
```powershell
ollama run llama3.2
```
Escribe algo, confirma que responde, y sal con `/bye`.

## Paso 3: Preparar la carpeta del proyecto

1. Clona o descarga la carpeta completa del proyecto. La interfaz necesita juntos: `app.py`, `appGemini.py`, `ui.py` (la interfaz compartida), `prompts.py` y la carpeta `.streamlit/` (el tema visual).

2. Dentro de la carpeta, crea un entorno virtual de Python (esto evita conflictos con otras librerías que ya tengas instaladas):
   ```powershell
   python -m venv venv
   ```

3. Activa el entorno virtual:
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```
   Deberías ver `(venv)` al inicio de la línea en PowerShell.

   > **Si sale un error de "ejecución de scripts deshabilitada"**, corre esto una sola vez y vuelve a intentar el paso anterior:
   > ```powershell
   > Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   > ```

4. Con el entorno activado, instala las librerías necesarias:
   ```powershell
   pip install requests streamlit google-genai
   ```

## Paso 4: Probar el prototipo de consola (opcional)

Sirve para confirmar rápido que todo conecta bien, antes de ir a la interfaz completa:
```powershell
python mentor.py
```
Escribe una duda de programación y confirma que el tutor responde con preguntas, no con código. Escribe `salir` para terminar.

## Paso 5: Correr la interfaz completa (Streamlit)

```powershell
streamlit run app.py
```

Esto abre automáticamente el navegador en `http://localhost:8501` con la interfaz de chat del mentor.

---

## Notas importantes para el equipo

- **Ollama debe estar corriendo en segundo plano** para que `mentor.py` o `app.py` funcionen (normalmente arranca solo tras instalarlo, pero si no responde, prueba abrir la app de Ollama o correr `ollama serve` en una terminal aparte).
- La primera respuesta del modelo tarda más (~10-12 segundos) porque tiene que cargarse en RAM. Las siguientes son más rápidas.
- El historial de conversación se reinicia si recargas la página del navegador (F5) — es una limitación conocida del prototipo actual.
- Todos deben usar **el mismo modelo (`llama3.2`)** para que las pruebas sean consistentes entre las computadoras del equipo.
