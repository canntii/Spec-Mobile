from pydantic import BaseModel, EmailStr

class Horario(BaseModel):
    fecha: str
    horaRegistrada: str
    ubicacion: str
    userFK: str


class HorarioInput(BaseModel):
    ubicacion : str
    userFK: str = "/user/LvPZakIp67d9wl3soXf"  # Valor predeterminado

class User(BaseModel):
    UserLastName : str
    cedula : str
    horaOficialEntrada : str
    imageUrl : str
    userName : str
    email : str
    id : str = None

class Location(BaseModel):
    location: dict

class ImageData(BaseModel):
    user_image_base64: str