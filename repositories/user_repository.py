from abc import ABC, abstractmethod
import face_recognition
from io import BytesIO
from fastapi import HTTPException
import requests


class UserRepository(ABC):

    @abstractmethod
    def get_user_image_from_firebase(self, id: str):
        pass

class FirebaseUserRepository(UserRepository):
    def __init__(self, db, bucket):
        self.db = db
        self.bucket = bucket


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