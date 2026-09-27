# Entorno de Desarrollo de Agente de IA (Gratis)

Acabo de configurarte esta carpeta con lo básico para que empieces a programar tu Agente de IA sin costo. 

## Pasos para probarlo (Puedes usar VS Code, PyCharm o la terminal de Antigravity):

### 1. Preparar el entorno (Python)
Te recomiendo crear un entorno virtual para no mezclar librerías. Abre tu terminal en esta carpeta y ejecuta:
```bash
python -m venv venv
.\venv\Scripts\activate
```

### 2. Instalar las dependencias
Instalamos LangChain (el framework estándar de la industria) y otras herramientas:
```bash
pip install -r requirements.txt
```

### 3. Elegir tu IA (Tienes 2 opciones preparadas)

#### Opción A: Usar Google Gemini (Archivo `agente_gemini.py`)
Es en la nube, rapidísimo, y la API de desarrollador de Google es gratis.
1. Ve a [Google AI Studio](https://aistudio.google.com/app/apikey) y genera una API Key gratis.
2. Crea un archivo llamado `.env` en esta misma carpeta.
3. Dentro del `.env`, escribe: `GOOGLE_API_KEY=tu_clave_aqui`
4. Ejecuta el script:
```bash
python agente_gemini.py
```

#### Opción B: Usar Ollama (Archivo `agente_ollama.py`)
Es 100% local, no usa internet, es privado, pero usa los recursos de tu PC (CPU/GPU).
1. Descarga e instala [Ollama](https://ollama.com/).
2. En tu terminal, descarga un modelo gratuito ejecutando: `ollama run llama3` (puede tardar un poco dependiendo de tu internet).
3. Una vez listo, ejecuta el script:
```bash
python agente_ollama.py
```
