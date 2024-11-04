from models.models import Horario
from repositories.horario_repository import HorarioRepository

class HorarioService:
    def __init__(self, horario_repository: HorarioRepository):
        self.horario_repository = horario_repository  # Asegúrate de que es una instancia

    def register_horario(self, horario_data: dict) -> Horario:
        horario = Horario(**horario_data)  # Crear un objeto Horario a partir de los datos
        return self.horario_repository.create_register(horario)  # Usar la instancia correcta

