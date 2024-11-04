from fastapi import APIRouter, HTTPException
from models.models import Horario, Location, HorarioInput
from services.horario_service import HorarioService
from repositories.horario_repository import FirebaseHorarioRepository
from firebase.firebase_service import FirebaseService
from datetime import datetime

router = APIRouter()

def setup_horario_router(firebase_service: FirebaseService):
    horario_repository = FirebaseHorarioRepository(firebase_service.get_db())
    horario_service = HorarioService(horario_repository)

    @router.post("/agregar-registro", response_model=Horario)
    async def create_register(horario_data: HorarioInput):

        horario = Horario(
            fecha=datetime.now().strftime("%d/%m/%Y"),
            horaRegistrada=datetime.now().strftime("%I:%M%p"),
            ubicacion=horario_data.ubicacion,
            userFK=horario_data.userFK  # Utiliza el valor del JSON o el predeterminado
        )

        # Registrar horario
        return horario_service.register_horario(horario.model_dump())

    return router

