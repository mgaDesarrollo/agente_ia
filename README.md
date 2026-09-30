# 🤖 Entorno de Desarrollo de Agentes de IA

Este repositorio contiene implementaciones de agentes de IA listos para usar, tanto en la nube (Gemini) como 100% locales (Ollama con streaming, memoria y herramientas).

---

## 🚀 Inicio Rápido

### 1. Preparar el entorno de Python
Abre tu terminal en esta carpeta y activa un entorno virtual:
```bash
python -m venv venv
.\venv\Scripts\activate
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

---

## 📂 Agentes Disponibles

### 1. `agente_ollama.py` (Local, Privado, Streaming y Memoria)
* **100% Local y privado** ejecutado con Ollama.
* **Streaming en tiempo real:** Muestra la respuesta token por token en la consola.
* **Memoria conversacional:** Recuerda el contexto durante la sesión.
* **Comandos:** Escribe `salir` para terminar o `limpiar` para resetear el historial.

```bash
# Requiere tener Ollama abierto con el modelo descargado (ej: ollama run llama3)
python agente_ollama.py
```

### 2. `agente_local_tools.py` (Agente Autónomo con Herramientas)
* Capacidad de **Function Calling** con Ollama.
* **Búsqueda Web:** Usa DuckDuckGo para buscar datos en vivo sin costo.
* **Calculadora:** Resuelve expresiones matemáticas con precisión.

```bash
# Recomendado con modelos compatibles con Tool Calling (llama3.1, llama3.2 o qwen2.5)
python agente_local_tools.py
```

### 3. `agente_gemini.py` (En la Nube con Google Gemini)
* Rápido y ligero usando la API gratuita de Gemini.
* Requiere clave en un archivo `.env` (`GOOGLE_API_KEY=AIzaSy...`).

```bash
python agente_gemini.py
```
