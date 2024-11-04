from models.models import User
from repositories.user_repository import UserRepository

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def register_user(self, user_data: dict) -> User:
        user = User(**user_data)  # Crear un objeto User a partir de los datos
        return self.user_repository.create_user(user)

    def get_user(self, user_id: str) -> User:
        return self.user_repository.get_user(user_id)

    def update_user(self, user_id: str, user_data: dict) -> User:
        user = User(**user_data)  # Crear un objeto User a partir de los datos
        return self.user_repository.update_user(user_id, user)

    def delete_user(self, user_id: str) -> None:
        self.user_repository.delete_user(user_id)


