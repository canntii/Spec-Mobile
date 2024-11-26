from starlette.websockets import WebSocket, WebSocketDisconnect
from models.models import CompareRequest
from repositories.user_repository import  UserRepository
from fastapi import APIRouter, HTTPException, WebSocketException


router = APIRouter()

def setup_user_router():
    user_repository = UserRepository()

    @router.post("/recognition/compare")
    async def compare_images(request: CompareRequest):
        try:

            comparison_function =  user_repository.compare_faces(request.image_firebase, request.image_webcam)

            print(f"Contenido de comparison_function: {comparison_function}")
            result = comparison_function["Match"]

            return {
                "Code" : "200",
                "Message" : "Comparación Éxitosa",
                "Match": result,
            }

        except Exception as e:
            print(f"Error al conectar: {e}")
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
