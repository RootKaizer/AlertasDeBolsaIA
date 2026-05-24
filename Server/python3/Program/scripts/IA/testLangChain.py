from langchain_ollama  import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
import os

# Obtener la API key de la variable de entorno $1 que mencionas
# o pasarla directamente aquí
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "tu-api-key-aqui")

# configuración para gemini
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash-002",
    temperature=0.3,
    google_api_key=GOOGLE_API_KEY
)

# Usar modelo local (debes tenerlo descargado: ollama pull llama3.2)
#    llm = ChatOllama(
#        model="llama3.2",  # o "mistral", "codellama", etc.
#        temperature=0.3
#    )

history = []
history.append(SystemMessage(content="Eres un experto en trading y analisis de mercado."))
history.append(HumanMessage(content="Analiza los mercados que van decallendo y que tiene buen prospecto de recuperarse..."))



# Usar
response = llm.invoke(history)
print(response.content)
