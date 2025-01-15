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

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://redactionai.netlify.app/"],  # Cambia esto al dominio de tu frontend en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ReescribirRequest(BaseModel):
    texto: str
    estilo: str

@app.post("/reescribir")
async def reescribir_articulo(request: ReescribirRequest):
    print(request) 
    messages = [
        {"role": "system", "content": f"Eres un asistente que reescribe artículos con el estilo {request.estilo}."},
        {"role": "user", "content": request.texto}
    ]
    try:
        # Usando el endpoint correcto para el modelo de chat
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Modelo GPT-3.5 o GPT-4 según prefieras
            messages=messages,
            max_tokens=1000,
            temperature=0.7
        )
# Manejo seguro de la respuesta
        if response.get("choices") and len(response["choices"]) > 0:
            content = response["choices"][0]["message"]["content"].strip()
            return {"resultado": content}
        else:
            return {"error": "La API no generó una respuesta válida."}
    except Exception as e:
        return {"error": f"Error en la API: {str(e)}"}