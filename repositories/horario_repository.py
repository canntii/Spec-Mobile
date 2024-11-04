
from abc import ABC, abstractmethod
from fastapi import FastAPI, HTTPException, Request
from models.models import Horario, Location


class HorarioRepository(ABC):

    @abstractmethod
    def create_register(self, horario: Horario) -> Horario:
        pass


class FirebaseHorarioRepository(HorarioRepository):
    def __init__(self, db):
        self.db = db

    def create_register(self, horario: Horario) -> Horario:
        horario_data = horario.model_dump(exclude={'id'})
        horario_ref = self.db.collection("horario").add(horario_data)
        return horario
