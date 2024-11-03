import base64
import os
import numpy as np
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import firebase_admin
from firebase_admin import credentials, firestore
import face_recognition
import cv2
import requests
from io import BytesIO

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {'storageBucket': os.getenv('STORAGE_BUCKET')})

db = firestore.client()

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Modelo para la imagen enviada desde el frontend
class ImageData(BaseModel):
    user_image_base64: str  # Asegúrate de que el nombre coincide con lo que envías

def process_image_from_base64(image_base64):
    try:
        # Decodificar la imagen de base64
        image_data = base64.b64decode(image_base64.split(",")[1])
        nparr = np.frombuffer(image_data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        face_encodings = face_recognition.face_encodings(rgb_img)

        if len(face_encodings) > 0:
            return face_encodings
        else:
            raise ValueError("No se encontraron rostros en la imagen")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al procesar la imagen: {str(e)}")


def get_user_image_from_firebase(id):
    user_ref = db.collection("user").document(id)
    user_data = user_ref.get().to_dict()

    if not user_data or "imageUrl" not in user_data:
        raise HTTPException(status_code=404, detail="Usuario o imagen no encontrado")

    image_url = user_data["imageUrl"]
    response = requests.get(image_url)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Error al obtener la imagen de Firebase")

    # Cargar la imagen desde la URL y convertirla a un formato compatible
    image = face_recognition.load_image_file(BytesIO(response.content))
    face_encodings = face_recognition.face_encodings(image)

    if not face_encodings:
        raise HTTPException(status_code=404, detail="No se encontró un rostro en la imagen")

    return face_encodings[0]  # Devuelve la primera codificación encontrada


@app.post("/compare")
async def compare_images(image_data: ImageData):
    try:

        tolerance = 0.4

        # Obtener la codificación facial del usuario desde Firebase
        user_firebase_face_encoding = get_user_image_from_firebase(os.getenv('BRYAN_USER_ID'))



        # Procesar la imagen del usuario desde base64
        user_face_encodings = process_image_from_base64(image_data.user_image_base64)

        # Verificar si se obtuvo alguna codificación facial
        if not user_face_encodings:
            raise HTTPException(status_code=400, detail="No se encontraron rostros en la imagen del usuario")

        # Obtener la primera codificación de la imagen del usuario
        user_face_encoding = user_face_encodings[0]

        # Comparar las codificaciones faciales
        results = face_recognition.compare_faces([user_firebase_face_encoding], user_face_encoding, tolerance= tolerance)

        # Determinar si hay coincidencia
        match = bool(results[0])  # True si hay coincidencia, False si no

        # Mensaje basado en el resultado de la comparación
        if match:
            comparison_result = "Las imágenes corresponden a la misma persona."
        else:
            comparison_result = "Las imágenes no corresponden a la misma persona."

        return {
            "message": "Comparación realizada con éxito",
            "match": match,
            "comparison_result": comparison_result,  # Mensaje de comparación
            "user_face_encoding": user_face_encoding.tolist()  # Devolver codificación de la imagen del usuario
        }

    except Exception as e:
        print(f"Error al comparar imágenes: {e}")  # Imprimir el error para depuración
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@app.get("/", response_class=HTMLResponse)
async def device_info(request: Request):
    return templates.TemplateResponse("Home.html", {"request": request})

@app.get("/video", response_class=HTMLResponse)
async def video_info(request: Request):
    return templates.TemplateResponse("Video.html", {"request": request})


#DOCUMENTATION TEMPLATES TEMPLATESTEMPLATESTEMPLATESTEMPLATESTEMPLATESTEMPLATESTEMPLATESTEMPLATESTEMPLATESTEMPLATESTEMPLATES
#STABLE VERSION STABLE VERSION STABLE VERSION STABLE VERSION STABLE VERSION STABLE VERSION STABLE VERSION