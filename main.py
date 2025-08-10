from fastapi import FastAPI # type: ignore
from dotenv import load_dotenv # type: ignore
import os
from fastapi.middleware.cors import CORSMiddleware # type: ignore
from pydantic import BaseModel # type: ignore
import openai

load_dotenv()
# Configura tu API Key de OpenAI
openai.api_key = os.getenv('API_KEY')

# Inicializa la aplicación FastAPI
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "¡Hola, mundo!"}

class ReescribirRequest(BaseModel):
    texto: str
class InstagramRequest(BaseModel):
    texto: str
class TraducirRequest(BaseModel):
    texto: str

class ImagenRequest(BaseModel):
    prompt: str
    
# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://redactor-ai.onrender.com", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],  # Asegura que OPTIONS está permitido
    allow_headers=["*"],
)


@app.post("/reescribir")
async def reescribir_articulo(request: ReescribirRequest):
    
    titles = [
    {
        "role": "system",
        "content": ( 
            ''' 
            Dame 3 opciones de titulos para este articulo, una opcion que sea llamativo, otro mas profesional y otro que sea breve pero descriptivo.
            '''
        )
    },
    {"role": "user", "content": request.texto},
    ]
    
    title_response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=titles,
        )

    titles = title_response["choices"][0]["message"]["content"].strip()
    
    messages = [
        {
            "role": "system",
            "content": (
                '''
                Tu tarea es reescribir completamente el siguiente artículo de forma creativa, clara y original, manteniendo los puntos clave y el mensaje central. No solo cambies palabras: reorganiza ideas,
                mejora la redacción y estructura el contenido para hacerlo más útil, profundo y atractivo para el lector. Añadí ejemplos nuevos, explicaciones adicionales, preguntas frecuentes, comparaciones o consejos prácticos relevantes 
                que no estén en el texto original. Evitá repetir frases hechas o fórmulas comunes. El resultado debe ser un artículo que se sienta escrito por una persona experta, sea valioso para el usuario
                y cumpla con los estándares de calidad de contenido de Google (E-E-A-T: experiencia, conocimiento, autoridad y confiabilidad). No menciones que se trata de una reescritura o menciones fuentes de la informacion.
                '''
            ),
        },
        {"role": "user", "content": request.texto},
    ]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=messages,
        )

        content = (
            response["choices"][0]["message"]["content"].strip()
            if "choices" in response and len(response["choices"]) > 0
            else "Error en la respuesta en español."
        )

        return {"resultado": content, "titulos": titles}

    except Exception as e:
        return {"error": f"Error en la API: {str(e)}"}

## Notice for Instagram
@app.post("/resumeIG")
async def resumir_instagram(request: InstagramRequest):
    
    resume_ig = [
    {
        "role": "system",
        "content": ( 
            ''' 
            Dame 3 opciones de titulos para este articulo, una opcion que sea llamativo, otro mas profesional y otro que sea breve pero descriptivo en ingles.
            '''
        )
    },
    {"role": "user", "content": request.texto},
    
    ]
    
    try:
        resume_response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=resume_ig,
        )
    
        resume_ig = resume_response["choices"][0]["message"]["content"].strip()
    
        return {"resume_ig": resume_ig}

    except Exception as e:
        return {"error": f"Error en la API: {str(e)}"}

## Traductor
@app.post("/traducir")
async def traducir_texto(request: TraducirRequest):
    
    titles_en = [
    {
        "role": "system",
        "content": ( 
            ''' 
            Dame 3 opciones de titulos para este articulo, una opcion que sea llamativo, otro mas profesional y otro que sea breve pero descriptivo en ingles.
            '''
        )
    },
    {"role": "user", "content": request.texto},
    ]
    
    title_response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=titles_en,
        )

    titles_en = title_response["choices"][0]["message"]["content"].strip()
    
    messages = [
        {"role": "system", "content": "Por favor, traduce el siguiente texto al inglés de forma clara y precisa, manteniendo el mismo texto pero solo traducido al ingles."},
        {"role": "user", "content": request.texto},
    ]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=messages,
        )

        content = (
            response["choices"][0]["message"]["content"].strip()
            if "choices" in response and len(response["choices"]) > 0
            else "Error en la respuesta de traducción."
        )

        return {"resultado": content, "titles_en": titles_en}

    except Exception as e:
        return {"error": f"Error en la API: {str(e)}"}
# @app.post("/create-image")
# async def crear_imagen(request: ImagenRequest):
#     try:
#         response = openai.Image.create(
#             model="dall-e-3",
#             prompt=request.prompt,
#             n=1,
#             size="1024x1024",
#             response_format="url"
#         )

#         image_url = response["data"][0]["url"]
#         return {"imagen": image_url}

#     except Exception as e:
#         return {"error": f"Error al generar la imagen: {str(e)}"}