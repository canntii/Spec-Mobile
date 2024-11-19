import base64
import cv2
import face_recognition
from io import BytesIO
from fastapi import HTTPException
import requests
import numpy as np

class UserRepository():

    def get_user_image_from_firebase(self, id: str):
        try:
            user_ref = self.db.collection("user").document(id)
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

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

    @staticmethod
    def calculate_brightness(imagen_base64: str) -> str:

        #Decodifica la imagen de base64 a un arreglo de NumPy
        image_bytes = base64.b64decode(imagen_base64)
        image_np = np.frombuffer(image_bytes,dtype=np.uint8)
        image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)

        #Convertir a espacio de color HSV
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        bright = np.mean(hsv[:,:,2]) #canal de V

        #Umbral de brillo
        brightTop = 200
        brightFloor = 125

        if bright > brightTop:
            return "Brillo muy alto"
        elif bright < brightFloor :
            return "Brillo bajo"
        else :
            return "Brillo adecuado"

    @staticmethod
    def isFace(image_base64: str) ->bool:

        # Cargar el clasificador Haar para detección de rostros
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        #Decodificar la imagen
        image_bytes = base64.b64decode(image_base64)
        image_np = np.frombuffer(image_bytes, dtype=np.uint8)
        image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)

        #Convertir la imagen a escala de grises
        imageGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        #Detectar rostros
        faces = face_cascade.detectMultiScale(imageGray, 1.1, 4)

        #Verificar si se detectaron rostros
        if len(faces) > 0:
            return True
        else:
            return False

    @staticmethod
    def buildAnswer(calculate_brightness: str, isFace: bool) -> dict:

        return{
            "message" : calculate_brightness,
            "faces" : isFace
        }

