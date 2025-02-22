from fastapi import FastAPI
from dotenv import load_dotenv
import os
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai

load_dotenv()
# Configura tu API Key de OpenAI
openai.api_key = os.getenv('API_KEY')

# Inicializa la aplicación FastAPI
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "¡Hola, mundo!"}

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://redactor-ai.onrender.com", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],  # Asegura que OPTIONS está permitido
    allow_headers=["*"],
)

class ReescribirRequest(BaseModel):
    texto: str

@app.post("/reescribir")
async def reescribir_articulo(request: ReescribirRequest):
    print(request) 
    
    messages_es = [
        {"role": "system", "content": "Eres un redactor argentino que reescribe artículos sobre noticias de finanzas, economia, tecnologia y criptomonedas con un estilo profesional y tienes mas de 10 años de experiencia. Todo el contenido damelo bien estructurado y con un lenguaje claro y preciso. (que cada parrafo tenga una idea central y que se entienda bien y este separado por un espacio en blanco)"},
        {"role": "user", "content": request.texto}
    ]
    
    messages_en = [
        {"role": "system", "content": "You are a professional writer who rewrites articles about financial news, economy, technology, and cryptocurrencies, with over 10 years of experience. Provide all content well-structured, with clear and precise language. Each paragraph should have a central idea, be easy to understand, and be separated by a blank space)"},
        {"role": "user", "content": request.texto}
    ]
    
    try:
        # Solicitar respuesta en español
        response_es = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Modelo GPT-3.5 o GPT-4 según prefieras
            messages=messages_es,
            max_tokens=700,
            temperature=0.7
        )
        
        # Solicitar respuesta en inglés
        response_en = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Modelo GPT-3.5 o GPT-4 según prefieras
            messages=messages_en,
            max_tokens=700,
            temperature=0.7
        )

        # Comprobamos que ambas respuestas tienen contenido
        content_es = response_es["choices"][0]["message"]["content"].strip() if "choices" in response_es and len(response_es["choices"]) > 0 else "Error en la respuesta en español."
        content_en = response_en["choices"][0]["message"]["content"].strip() if "choices" in response_en and len(response_en["choices"]) > 0 else "Error in the English response."

        return {"resultado_es": content_es, "resultado_en": content_en}

    except Exception as e:
        return {"error": f"Error en la API: {str(e)}"}