
from routers.user_router import setup_user_router
from fastapi import FastAPI

app = FastAPI()

# Configurar los routers
user_router = setup_user_router()
app.include_router(user_router)



