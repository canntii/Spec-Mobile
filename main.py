from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from user_agents import parse

app = FastAPI()

@app.get("/")
async def device_info(request: Request):
    user_agent = request.headers.get("User-Agent")
    user_agent_parsed = parse(user_agent)

    # Obtener el modelo del dispositivo
    device_model = user_agent_parsed.device.family  # Esto a menudo da un nombre genérico
    if user_agent_parsed.is_mobile:
        device_model += f" {user_agent_parsed.device.brand}"

    # Crear un diccionario con la información del dispositivo
    device_info = {
        "is_mobile": user_agent_parsed.is_mobile,
        "is_tablet": user_agent_parsed.is_tablet,
        "is_pc": user_agent_parsed.is_pc,
        "browser": user_agent_parsed.browser.family,
        "browser_version": user_agent_parsed.browser.version_string,
        "os": user_agent_parsed.os.family,
        "os_version": user_agent_parsed.os.version_string,
        "device": device_model,
    }
    return JSONResponse(content=device_info)





