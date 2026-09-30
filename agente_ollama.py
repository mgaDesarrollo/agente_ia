import sys
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

# 1. Importar ChatOllama (preferido: langchain_ollama, con fallback a langchain_community)
try:
    from langchain_ollama import ChatOllama
except ImportError:
    try:
        from langchain_community.chat_models import ChatOllama
    except ImportError:
        from langchain_community.llms import Ollama as ChatOllama

# Modelo por defecto en Ollama (puedes cambiarlo por: "llama3.2", "qwen2.5:7b", "mistral", etc.)
MODELO_OLLAMA = "llama3.2"

# 2. Inicializar el modelo con Streaming activado
llm = ChatOllama(
    model=MODELO_OLLAMA,
    temperature=0.7,
)

# 3. Crear el Prompt Conversacional
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "Eres un asistente de IA inteligente, preciso y amigable. "
        "Te ejecutas de forma 100% local y privada en la máquina del usuario. "
        "Responde en el idioma del usuario de manera estructurada y clara."
    ),
    MessagesPlaceholder(variable_name="historial"),
    ("human", "{pregunta}")
])

# 4. Crear la cadena base
cadena = prompt | llm

# 5. Sistema de Memoria de Conversación
historial_memoria = ChatMessageHistory()

def obtener_historial(session_id: str):
    return historial_memoria

agente_con_memoria = RunnableWithMessageHistory(
    cadena,
    obtener_historial,
    input_messages_key="pregunta",
    history_messages_key="historial"
)

# 6. Bucle de Chat Interactivo con Streaming
def iniciar_chat():
    print("=" * 60)
    print(f"🤖 Agente de IA Local Iniciado (Ollama: {MODELO_OLLAMA})")
    print("🔒 Modo 100% Local y Privado con Streaming y Memoria")
    print("=" * 60)
    print("Comandos disponibles:")
    print(" • 'salir', 'exit' o 'quit' : Terminar la sesión")
    print(" • 'limpiar'                : Borrar el historial de memoria")
    print("-" * 60 + "\n")

    config = {"configurable": {"session_id": "sesion_local"}}

    while True:
        try:
            pregunta = input("\n👤 Tú: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\nAgente: ¡Hasta la próxima!")
            break

        if not pregunta:
            continue

        if pregunta.lower() in ["salir", "exit", "quit"]:
            print("\nAgente: ¡Hasta luego! Que tengas un excelente día.")
            break

        if pregunta.lower() == "limpiar":
            historial_memoria.clear()
            print("\n🧹 Historial de memoria borrado.")
            continue

        print("\n🤖 Agente: ", end="", flush=True)

        try:
            # Streaming token por token en tiempo real
            chunk_completo = ""
            for chunk in agente_con_memoria.stream({"pregunta": pregunta}, config=config):
                contenido = chunk.content if hasattr(chunk, "content") else str(chunk)
                sys.stdout.write(contenido)
                sys.stdout.flush()
                chunk_completo += contenido
            print()  # Salto de línea al finalizar
        except Exception as e:
            print("\n\n❌ Error al conectar con Ollama.")
            print("Verifica que:")
            print(" 1. La aplicación de Ollama esté abierta en tu PC.")
            print(f" 2. Hayas descargado el modelo ejecutando en tu terminal: 'ollama run {MODELO_OLLAMA}'")
            print(f"\nDetalle técnico: {e}")

if __name__ == "__main__":
    iniciar_chat()
