from fastapi import APIRouter, HTTPException
from models.models import User, ImageData
from services.user_service import UserService
from repositories.user_repository import FirebaseUserRepository
from firebase.firebase_service import FirebaseService
import time
import face_recognition
from services.utilities import process_image_from_base64

router = APIRouter()

def setup_user_router(firebase_service: FirebaseService):
    user_repository = FirebaseUserRepository(firebase_service.get_db())
    user_service = UserService(user_repository)

    @router.post("/users/", response_model=User)
    async def create_user(user:User):
        return user_service.register_user(user.model_dump())

    @router.get("/users/{user_id}", response_model=User)
    async def read_user(user_id: str):
        user = user_service.get_user(user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    @router.put("/users/{user_id}", response_model=User)
    async def update_user(user_id: str, user: User):
        return user_service.update_user(user_id, user.model_dump())

    @router.delete("/users/{user_id}", response_model=None)
    async def delete_user(user_id: str):
        user_service.delete_user(user_id)
        return {"detail": "User deleted"}

    @router.post("/compare")
    async def compare_images(image_data: ImageData):
        try:
            # Inicializa cronometro para ver cuanto se tarda
            start_time = time.time()  # inicio de temporizador

            tolerance = 0.4
            # Obtener la codificación facial del usuario desde Firebase
            user_firebase_face_encoding = user_repository.get_user_image_from_firebase("LvPZakIp67d9wl3soXfJ")

            # Procesar la imagen del usuario desde base64
            user_face_encodings = process_image_from_base64(image_data.user_image_base64)

            # Verificar si se obtuvo alguna codificación facial viene del frontend
            if not user_face_encodings:
                raise HTTPException(status_code=400, detail="No se encontraron rostros en la imagen del usuario")

            # Obtener la primera codificación de la imagen del usuario que viene del frontend
            user_face_encoding = user_face_encodings[0]

            # Comparar las codificaciones faciales
            results = face_recognition.compare_faces([user_firebase_face_encoding], user_face_encoding,
                                                     tolerance=tolerance)

            # Determinar si hay coincidencia (convertir a booleano nativo)
            match = bool(results[0])  # Convertir a bool nativo

            # Mensaje basado en el resultado de la comparación
            if match:
                comparison_result = "Las imágenes corresponden a la misma persona."
            else:
                comparison_result = "Las imágenes no corresponden a la misma persona."

            end_time = time.time()
            execution_time = end_time - start_time

            print(f"El reconocimiento facial dura {execution_time}")
            # deberia de durar aprox 3s
            return {
                "message": "Comparación realizada con éxito",
                "match": match,
                "comparison_result": comparison_result,  # Mensaje de comparación
                "user_face_encoding": user_face_encoding.tolist()  # Devolver codificación de la imagen del usuario
            }

        except Exception as e:
            print(f"Error al comparar imágenes: {e}")  # Imprimir el error para depuración
            raise HTTPException(status_code=500, detail="Error interno del servidor")


    return router
