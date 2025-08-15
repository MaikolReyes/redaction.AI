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
    
class TwitterRequest(BaseModel):
    texto: str
class TraducirRequest(BaseModel):
    texto: str
    titulos: str
    resumen: str

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

## Rewrite and Summary of Articles
@app.post("/reescribir")
async def reescribir_articulo(request: ReescribirRequest):
    
    titles = [
    {
        "role": "system",
        "content": ( 
            """A partir del siguiente artículo de noticias, generá 3 títulos diferentes. 
            Uno debe ser llamativo y captar la atención del lector, 
            otro debe sonar profesional y formal como si fuera para un medio serio, 
            y el tercero debe ser breve pero claro y descriptivo. 
            Evitá repetir las mismas palabras entre los títulos.
            
            Devuelve solo los títulos, sin texto adicional, sin encabezados ni espacios extra, tampoco con puntos o signos -.
            Solo listalos separados sin saltos de línea.
            """
        )
    },
    {"role": "user", "content": request.texto},
    ]
    
    title_response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=titles,
        )

    titles = title_response["choices"][0]["message"]["content"].strip()
    
    resumen = [
    {
        "role": "system",
        "content": ( 
            f"""A partir del siguiente artículo de noticias {request.texto}, generá 5 puntos resumiendo la noticia con los puntos mas importantes.
            Devuelve solo los puntos, sin texto adicional, sin encabezados ni espacios extra.
            Solo listalos separados por saltos de línea.
            Asegurate de que los puntos sean claros, concisos y reflejen los aspectos más relevantes de la noticia.
            No incluyas opiniones o juicios de valor, solo hechos y datos objetivos.
            """
        )
    },
    {"role": "user", "content": request.texto},
    ]
    
    resumen_response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=resumen,
        )

    resumen = resumen_response["choices"][0]["message"]["content"].strip()
    
    messages = [
        {
            "role": "system",
            "content": (
            """
Reescribí completamente el siguiente artículo desde cero, sin conservar ninguna frase, estructura ni orden original.

El nuevo texto debe estar diseñado para ser publicado en Financessignal, un sitio web de noticias financieras que cubre temas como criptomonedas, economía, finanzas y tecnología.

✅ Público objetivo:
Consumidores generales interesados en noticias financieras.

✅ Tono:
Formal, técnico y persuasivo.

✅ Estilo editorial:
Profesional, con enfoque analítico y profundidad conceptual.

🔧 Instrucciones específicas:
- Conservá los hechos clave del artículo original, pero reorganizá la narrativa y cambiá el enfoque para hacerlo único.
- Reformulá todas las ideas con vocabulario distinto, evitando cualquier frase idéntica o estructura similar.
- No copies citas textuales ni fragmentos del artículo original. Parafraseá todo con estilo propio.
- Añadí valor con contenido nuevo: contexto adicional, implicancias estratégicas, ejemplos, comparaciones internacionales, o referencias a tendencias actuales.
- Estructurá el artículo en secciones claras y bien definidas, como:
- Introducción
- Contexto del problema
- Análisis del impacto
- Opiniones del sector
- Oportunidades para inversores
- Riesgos latentes
- Conclusión estratégica
- Optimizá el contenido para SEO:
- Incluí palabras clave relevantes relacionadas con el tema.
- Generá un título atractivo y optimizado para buscadores.
- Redactá una metadescripción de máximo 160 caracteres.
- Sugerí 3–5 palabras clave principales.
- Proponé enlaces internos (a otras notas de Financessignal) y externos (a fuentes confiables).

🎯 Objetivo final:
El artículo reescrito debe tener 0% de similitud textual con el original, ser percibido como contenido único y de alta calidad editorial, y estar listo para publicación en Financessignal.
                """
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

        return {"resultado": content, "titulos": titles, "resumen": resumen}

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
            Eres un asistente experto en redacción creativa para redes sociales. 
            A partir del texto proporcionado, crea un resumen atractivo y llamativo para Instagram.
            Debe contener emojis y un tono persuasivo. 
            
            No pidas información adicional y no incluyas explicaciones.
            '''
        )
    },
    {"role": "user", "content": request.texto},
    
    ]
    
    try:
        resume_response_ig = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=resume_ig,
        )
    
        resume_ig = resume_response_ig["choices"][0]["message"]["content"].strip()
    
        return {"resume_ig": resume_ig}

    except Exception as e:
        return {"error": f"Error en la API: {str(e)}"}
    
    ## Notice for Instagram
@app.post("/resumeTwitter")
async def resumir_twitter(request: TwitterRequest):
    
    resume_twitter= [
    {
        "role": "system",
        "content": ( 
            '''
            Eres un experto en redacción para Twitter/X. 
            A partir del texto proporcionado, crea un hilo para twitter, atractivo e impactante que no supere los 280 caracteres por tweet.
            
            Debe captar la atención en los primeros segundos, incluir al menos un emoji y hasta 3 hashtags relevantes.
            
            Cada hilo debe estar enumerado con un emoji de numero que comienze con 1️⃣ y continue con los siguientes numeros hasta el tweet numero 7.
            
            No pidas información adicional, no incluyas explicaciones y no uses enlaces.
            '''
        )
    },
    {"role": "user", "content": request.texto},
    
    ]
    
    try:
        resume_response_x = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=resume_twitter,
        )
    
        resume_twitter = resume_response_x["choices"][0]["message"]["content"].strip()
    
        return {"resume_twitter": resume_twitter}

    except Exception as e:
        return {"error": f"Error en la API: {str(e)}"}

## Traductor
@app.post("/traducir")
async def traducir_texto(request: TraducirRequest):
    
    titles_en = [
    {
        "role": "system",
        "content": 
        f"""Traduce estas 3 opciones de títulos al inglés:
        {request.titulos}
        Devuelve solo las traducciones exactas de los títulos, sin texto adicional, sin encabezados ni espacios extra.
        Solo listalos separados por saltos de línea.
        """
    },
    {"role": "user", "content": request.titulos},
    ]
    
    title_response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=titles_en,
        )

    titles_en = title_response["choices"][0]["message"]["content"].strip()
    
    resumen_en = [
    {
        "role": "system",
        "content": ( 
            f"""Traduce este resumen de 5 puntos donde se resume la noticia al inglés: {request.resumen}
            Devuelve solo los puntos, sin texto adicional, sin encabezados ni espacios extra.
            Solo listalos separados por saltos de línea.
            """
        )
    },
    {"role": "user", "content": request.resumen},
    ]
    
    resumen_response_en = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=resumen_en,
        )

    resumen_en = resumen_response_en["choices"][0]["message"]["content"].strip()
    
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

        return {"resultado": content, "titles_en": titles_en, "resumen_en": resumen_en}

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