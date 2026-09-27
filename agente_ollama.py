from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate

# 1. Inicializar el modelo local
# NOTA: Requiere tener Ollama ejecutándose en tu PC y haber descargado el modelo (ej: 'ollama run llama3')
llm = Ollama(model="llama3")

# 2. Crear el prompt
template = """
Eres un asistente de IA que se ejecuta de forma local y 100% privada.
Responde a la siguiente pregunta de manera clara.

Usuario: {pregunta}
Asistente:"""
prompt = PromptTemplate.from_template(template)

# 3. Crear la cadena con LCEL
chain = prompt | llm

# Probar el agente
if __name__ == "__main__":
    print("🤖 Agente de IA Iniciado (Usando Ollama - 100% Local y Privado)")
    pregunta_usuario = "Explica brevemente la ventaja de correr un modelo de IA en modo local."
    print(f"Pregunta: {pregunta_usuario}")
    print("Generando respuesta localmente...\n")
    
    try:
        # Invocar la cadena
        respuesta = chain.invoke({"pregunta": pregunta_usuario})
        print("\nRespuesta del Agente:")
        print(respuesta)
    except Exception as e:
        print("\nError al generar la respuesta. ¿Tienes Ollama abierto y el modelo 'llama3' descargado?")
        print(f"Detalle del error: {e}")
