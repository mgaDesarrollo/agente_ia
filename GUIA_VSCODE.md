# Guía de Uso e Implementación en Visual Studio Code (VS Code)

Esta guía te explicará cómo configurar tu entorno, utilizar los agentes de IA creados (Gemini y Ollama), y aprovechar al máximo las herramientas que ofrece VS Code para el desarrollo.

## 1. Abrir el Proyecto en VS Code

1. Abre **Visual Studio Code**.
2. Ve al menú superior: `Archivo` > `Abrir Carpeta...` (o `File` > `Open Folder...`).
3. Selecciona la carpeta de tu proyecto (donde están guardados los archivos `.py` y el `README.md`).

## 2. Extensiones Recomendadas

Para programar agentes de IA en Python cómodamente, te sugiero instalar estas extensiones desde el panel de Extensiones de VS Code (el ícono de los cuadrados en la barra lateral izquierda o presionando `Ctrl + Shift + X`):

- **Python (de Microsoft):** Obligatoria. Ofrece autocompletado, depuración (debugging) y soporte para entornos virtuales.
- **Python Debugger (de Microsoft):** Para poder encontrar errores en tu código paso a paso.
- **DotENV:** Colorea y resalta la sintaxis de tu archivo `.env` para que sea más fácil leer tus API Keys.

## 3. Configurar el Entorno Virtual en VS Code

Es importante que VS Code sepa qué entorno de Python estás usando para que el autocompletado y LangChain funcionen sin marcar errores.

1. Abre una nueva terminal integrada en VS Code (`Ver` > `Terminal` o `Ctrl + \``).
2. Si aún no creaste el entorno, ejecuta: `python -m venv venv`
3. Dile a VS Code que use este entorno:
   - Presiona `Ctrl + Shift + P` para abrir la Paleta de Comandos.
   - Escribe y selecciona: **`Python: Select Interpreter`** (Python: Seleccionar Intérprete).
   - Elige el que dice algo como `.\venv\Scripts\python.exe` (suele tener una estrella o decir "Recomendado").
4. A partir de ahora, cada vez que abras una terminal nueva en VS Code, verás un `(venv)` al principio de la línea, indicando que está activado.

## 4. Instalación de Dependencias

Con la terminal activada `(venv)`, instala los paquetes necesarios (si no lo hiciste antes):

```bash
pip install -r requirements.txt
```

## 5. Configurar tus Credenciales

1. En la barra lateral (Explorador de archivos), haz clic en el botón de "Nuevo Archivo".
2. Nómbralo exactamente **`.env`** (asegúrate del punto inicial).
3. Pega tu API Key de Google (necesaria para `agente_gemini.py`):

```env
GOOGLE_API_KEY=AIzaSyTuClaveAca...
```
*(Guarda el archivo presionando `Ctrl + S`)*

## 6. Ejecutar los Agentes

Puedes probar tus agentes directamente en la terminal de VS Code.

**Para probar el Agente Gemini (en la nube):**
```bash
python agente_gemini.py
```

**Para probar el Agente Ollama (local y privado):**
*(Recuerda tener la aplicación de Ollama abierta en tu PC)*
```bash
python agente_ollama.py
```

## 7. Depuración (Debugging) Avanzada en VS Code

Si tu agente falla o quieres ver cómo "piensa" paso a paso:

1. Abre `agente_gemini.py`.
2. Haz clic a la izquierda de los números de línea (por ejemplo, en la línea donde está `respuesta = chain.invoke(...)`). Aparecerá un **punto rojo** (Breakpoint).
3. Ve a la pestaña "Ejecución y depuración" (ícono de play con un bicho) en la barra lateral, o presiona `Ctrl + Shift + D`.
4. Haz clic en **"Ejecutar y depurar"** y elige **"Archivo de Python"**.
5. El código se detendrá exactamente en el punto rojo y podrás ver qué variables tiene en memoria, cuál fue la respuesta exacta de la IA antes de imprimirla, etc.

## 8. Siguientes Pasos (Evolución de tu Agente)

Para seguir haciendo crecer tu agente desde VS Code, puedes intentar:
- **Cambiar el Prompt:** Entra a los archivos `.py` y modifica la variable `template`. ¡Haz que el agente asuma una personalidad diferente!
- **Agregar Memoria:** Investiga la clase `ConversationBufferMemory` de LangChain para que el agente recuerde mensajes anteriores.
- **Agregar Herramientas:** Investiga los "LangChain Agents" para darle capacidades a tu IA (ej. buscar en Google o leer un archivo de tu PC).
