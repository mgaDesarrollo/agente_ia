import sys
from duckduckgo_search import DDGS
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

try:
    from langchain_ollama import ChatOllama
except ImportError:
    from langchain_community.chat_models import ChatOllama

# ==========================================
# 1. Definición de Herramientas (Tools)
# ==========================================

@tool
def buscar_en_internet(consulta: str) -> str:
    """Busca información actualizada en la web usando DuckDuckGo."""
    try:
        with DDGS() as ddgs:
            resultados = list(ddgs.text(consulta, max_results=3))
            if not resultados:
                return "No se encontraron resultados en la web."
            
            texto_formateado = []
            for r in resultados:
                texto_formateado.append(f"- Título: {r.get('title')}\n  Enlace: {r.get('href')}\n  Resumen: {r.get('body')}")
            return "\n\n".join(texto_formateado)
    except Exception as e:
        return f"Error al buscar en la web: {e}"

@tool
def calculadora(expresion: str) -> str:
    """Calcula expresiones matemáticas de forma segura. Ejemplo: '1500 * 1.21' o '2**8'."""
    try:
        # Permitir solo caracteres matemáticos seguros
        caracteres_permitidos = "0123456789+-*/().,% "
        if not all(c in caracteres_permitidos for c in expresion):
            return "Expresión no válida. Solo se permiten números y operadores aritméticos."
        resultado = eval(expresion, {"__builtins__": None}, {})
        return f"Resultado de {expresion} = {resultado}"
    except Exception as e:
        return f"Error al calcular: {e}"

herramientas = [buscar_en_internet, calculadora]
mapa_herramientas = {t.name: t for t in herramientas}

# ==========================================
# 2. Inicialización del LLM con Tools
# ==========================================
MODELO_OLLAMA = "llama3.2"  # Modelos recomendados para tools: llama3.2, llama3.1, qwen2.5

llm = ChatOllama(
    model=MODELO_OLLAMA,
    temperature=0.2,
).bind_tools(herramientas)

# ==========================================
# 3. Prompt Conversacional
# ==========================================
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "Eres un agente de IA autónomo y capacitado. Tienes acceso a herramientas externas como "
        "búsqueda en internet y calculadora. Úsalas cuando la pregunta requiera datos actualizados "
        "o cálculos matemáticos precisos."
    ),
    MessagesPlaceholder(variable_name="historial"),
    ("human", "{pregunta}")
])

cadena = prompt | llm

# ==========================================
# 4. Historial y Ejecución de Herramientas
# ==========================================
historial_memoria = ChatMessageHistory()

def procesar_pregunta(pregunta_usuario: str):
    # Obtener historial actual
    mensajes_previos = historial_memoria.messages
    
    # Invocar LLM
    respuesta_llm = cadena.invoke({
        "pregunta": pregunta_usuario,
        "historial": mensajes_previos
    })
    
    # Guardar pregunta del usuario
    historial_memoria.add_user_message(pregunta_usuario)

    # Verificar si el modelo decidió invocar herramientas (Tool Calls)
    if hasattr(respuesta_llm, "tool_calls") and respuesta_llm.tool_calls:
        for tool_call in respuesta_llm.tool_calls:
            nombre_tool = tool_call["name"]
            argumentos = tool_call["args"]
            print(f"\n⚙️  [Ejecutando herramienta: {nombre_tool}] con {argumentos}...")
            
            herramienta = mapa_herramientas.get(nombre_tool)
            if herramienta:
                resultado = herramienta.invoke(argumentos)
                print(f"📄 [Resultado]: {resultado[:200]}...")
                
                # Segundo paso: Generar respuesta final con el resultado
                prompt_sintesis = (
                    f"El usuario preguntó: '{pregunta_usuario}'. "
                    f"La herramienta '{nombre_tool}' devolvió la siguiente información:\n{resultado}\n\n"
                    f"Por favor responde al usuario de forma amigable y completa usando esta información."
                )
                respuesta_final = ChatOllama(model=MODELO_OLLAMA, temperature=0.7).invoke(prompt_sintesis)
                historial_memoria.add_ai_message(respuesta_final.content)
                return respuesta_final.content
    
    historial_memoria.add_ai_message(respuesta_llm.content)
    return respuesta_llm.content

def iniciar_agente():
    print("=" * 65)
    print(f"🤖 Agente Autónomo con Herramientas (Ollama: {MODELO_OLLAMA})")
    print("🛠️  Herramientas integradas: Búsqueda Web (DuckDuckGo), Calculadora")
    print("=" * 65)
    print("Escribe 'salir' para finalizar o 'limpiar' para resetear memoria.\n")

    while True:
        try:
            pregunta = input("\n👤 Tú: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n¡Hasta pronto!")
            break

        if not pregunta:
            continue
        if pregunta.lower() in ["salir", "exit", "quit"]:
            break
        if pregunta.lower() == "limpiar":
            historial_memoria.clear()
            print("🧹 Historial borrado.")
            continue

        try:
            print("\n🤖 Pensando...")
            respuesta = procesar_pregunta(pregunta)
            print(f"\n🤖 Agente: {respuesta}")
        except Exception as e:
            print(f"\n❌ Error al ejecutar el agente: {e}")
            print(f"Asegúrate de tener Ollama activo y el modelo '{MODELO_OLLAMA}' descargado.")

if __name__ == "__main__":
    iniciar_agente()
