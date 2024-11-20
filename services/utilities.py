import base64
import numpy as np
from fastapi import HTTPException
import face_recognition
import cv2

@staticmethod
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