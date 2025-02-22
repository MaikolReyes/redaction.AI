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
        {"role": "system", "content": "Por favor, reescribe el siguiente artículo de manera completamente original, manteniendo el mismo significado y los puntos clave. Asegúrate de cambiar la estructura del contenido y usar un vocabulario y frases diferentes. Incluye ejemplos relevantes e ideas que no estén presentes en el texto original. El objetivo es hacer que la versión reescrita sea única, evitando el plagio, mientras se transmite el mismo mensaje. Responde solo en español, sin inglés y si te escribo en inglés, debes traducirlo al español."},
        {"role": "user", "content": request.texto}
    ]
    
    messages_en = [
        {"role": "system", "content": "Please rewrite the following article in a completely original way while maintaining the same meaning and key points. Ensure that the structure of the content is changed, and use different wording and phrasing. Include relevant examples and insights that are not present in the original text. The goal is to make the rewritten version unique, avoiding plagiarism, while still conveying the same message. Respond only in English, no Spanish and if I write to you in Spanish, you should translate it to English."},
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