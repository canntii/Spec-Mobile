from firebase.firebase_service import FirebaseService
from routers.user_router import setup_user_router
from fastapi import FastAPI
from fastapi.security import HTTPBearer

app = FastAPI()

#Instanciar los servicios necesarios
firebase_service = FirebaseService()
security = HTTPBearer()

# Configurar los routers
user_router = setup_user_router(firebase_service)
app.include_router(user_router)


