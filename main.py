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
    
    messages = [
        {"role": "system", "content": "Por favor, reescribe el siguiente artículo de manera completamente original, manteniendo el mismo significado y los puntos clave. Asegúrate de cambiar la estructura del contenido y usar un vocabulario y frases diferentes. Incluye ejemplos relevantes e ideas que no estén presentes en el texto original. El objetivo es hacer que la versión reescrita sea única, evitando el plagio, mientras se transmite el mismo mensaje. Responde en espanol y tambien dame una version del mismo texto traducido al ingles (Dame siempre mas de 1000 palabras)"},
        {"role": "user", "content": request.texto}
    ]
    
    try:
        # Solicitar respuesta en español
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Modelo GPT-3.5 o GPT-4 según prefieras
            messages=messages,
            max_tokens=4000,
            temperature=0.7
        )
        

        # Comprobamos que ambas respuestas tienen contenido
        content = response["choices"][0]["message"]["content"].strip() if "choices" in response and len(response["choices"]) > 0 else "Error en la respuesta en español."

        return {"resultado": content,}

    except Exception as e:
        return {"error": f"Error en la API: {str(e)}"}