import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

# Cargar variables de entorno (tu API key)
load_dotenv()

if not os.environ.get("GOOGLE_API_KEY"):
    print("Por favor, configura tu GOOGLE_API_KEY en un archivo .env (ejemplo: GOOGLE_API_KEY=AIzaSy...)")
    print("Puedes conseguir una gratis en: https://aistudio.google.com/app/apikey")
    exit()

# 1. Inicializar el modelo (Usamos la capa gratuita de Gemini 1.5 Flash)
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.7)

# 2. Crear el prompt conversacional
prompt = ChatPromptTemplate.from_messages([
    ("system", "Eres un asistente de IA muy útil y amigable. Responde de forma clara y concisa."),
    MessagesPlaceholder(variable_name="historial"),
    ("human", "{pregunta}")
])

# 3. Crear la cadena básica
chain = prompt | llm

# 4. Agregar Memoria (Historial de conversación)
# Usamos ChatMessageHistory para guardar los mensajes en memoria local
historial_memoria = ChatMessageHistory()

def obtener_historial(session_id: str):
    return historial_memoria

agente_con_memoria = RunnableWithMessageHistory(
    chain,
    obtener_historial,
    input_messages_key="pregunta",
    history_messages_key="historial"
)

# 5. Bucle de Chat Interactivo
if __name__ == "__main__":
    print("🤖 Agente de IA Iniciado (Gemini API Gratis) - Modo Chat Interactivo")
    print("Escribe 'salir' para terminar.\n")
    
    while True:
        pregunta_usuario = input("Tú: ")
        
        if pregunta_usuario.lower() in ['salir', 'exit', 'quit']:
            print("Agente: ¡Hasta luego!")
            break
            
        respuesta = agente_con_memoria.invoke(
            {"pregunta": pregunta_usuario},
            config={"configurable": {"session_id": "unica"}}
        )
        
        print(f"Agente: {respuesta.content}\n")
