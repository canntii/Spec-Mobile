from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
from firebase.firebase_service import FirebaseService
from routers.horario_router import setup_horario_router
from routers.user_router import setup_user_router


app = FastAPI()

# Configuración para archivos estáticos
app.mount("/assets", StaticFiles(directory="assets"), name="assets")
templates = Jinja2Templates(directory="templates")
firebase_service = FirebaseService()

# Configurar los routers
user_router = setup_user_router(firebase_service)
horario_router = setup_horario_router(firebase_service)
app.include_router(user_router)
app.include_router(horario_router)

@app.get("/", response_class=HTMLResponse)
async def device_info(request: Request):
    return templates.TemplateResponse("Home.html", {"request": request})

@app.get("/video", response_class=HTMLResponse)
async def video_info(request: Request):
    return templates.TemplateResponse("Video.html", {"request": request})

