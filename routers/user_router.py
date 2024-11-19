from starlette.websockets import WebSocket, WebSocketDisconnect

from models.models import ImageData
from repositories.user_repository import  UserRepository
import time
import face_recognition
from services.utilities import process_image_from_base64
from fastapi import APIRouter, HTTPException, WebSocketException

router = APIRouter()

def setup_user_router():
    user_repository = UserRepository()

    @router.post("/compare")
    async def compare_images(user_id: str, image_data: ImageData):
        try:
            # Inicializa cronometro para ver cuanto se tarda
            start_time = time.time()  # inicio de temporizador

            tolerance = 0.4

            # Obtener la codificación facial del usuario desde Firebase
            user_firebase_face_encoding = user_repository.get_user_image_from_firebase(user_id)

            # Procesar la imagen de la camara que viene en base64
            user_face_encodings = process_image_from_base64(image_data.user_image_base64)

            # Verificar si se obtuvo alguna codificación facial viene del frontend
            if not user_face_encodings:
                raise HTTPException(status_code=400, detail="No se encontraron rostros en la imagen del usuario")

            # Obtener la primera codificación de la imagen del usuario que viene de la camara
            user_face_encoding = user_face_encodings[0]

            # Comparar las codificaciones faciales
            results = face_recognition.compare_faces([user_firebase_face_encoding], user_face_encoding,
                                                     tolerance=tolerance)

            # Determinar si hay coincidencia (convertir a booleano nativo)
            match = bool(results[0])

            # Mensaje basado en el resultado de la comparación
            if match:
                comparison_result = True
            else:
                comparison_result = False

            end_time = time.time()
            execution_time = end_time - start_time

            print(f"El reconocimiento facial dura {execution_time}")
            # deberia de durar aprox 3s
            return {
                "message": "Comparación realizada con éxito",
                "match": match,
                "comparison_result": comparison_result
            }

        except Exception as e:
            print(f"Error al comparar imágenes: {e}")
            raise HTTPException(status_code=500, detail="Error interno del servidor")

    @router.websocket("/ws/calculate_brightness")
    async def websocket_endpoint(websocket: WebSocket):
        await websocket.accept()
        try:
            while True:
                try:
                    # Recepción de datos en base64
                    data = await websocket.receive_text()
                    bright = user_repository.calculate_brightness(data)
                    face = user_repository.isFace(data)
                    result = user_repository.buildAnswer(bright, face)

                    await websocket.send_json(result)
                except WebSocketException as e:
                    await websocket.send_text(f"Error en el mensaje recibido: {str(e)}")
        except WebSocketDisconnect:
            print("WebSocket desconectado")
        except Exception as e:
            print(f"Error inesperado: {str(e)}")
        finally:
            await websocket.close()



    return router
