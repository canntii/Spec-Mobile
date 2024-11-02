from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.responses import HTMLResponse
from user_agents import parse
from fastapi.templating import Jinja2Templates
from device_detector import DeviceDetector

app = FastAPI()
templates = Jinja2Templates(directory="templates")



@app.get("/", response_class=HTMLResponse)
async def device_info(request: Request):
    user_agent = request.headers.get("User-Agent")

    device_detector = DeviceDetector(user_agent).parse()

    device_info = {
        "device_os" : device_detector.os_name(),
        "device.os_version": device_detector.os_name(),
        "device_engine" : device_detector.engine(),
        "device_brand": device_detector.device_brand(),
        "device_model" : device_detector.device_model(),
        "device_type" : device_detector.device_type(),
        "device feature" : device_detector.android_feature_phone(),
        "device top" : device_detector.android_device_type()
    }



    return templates.TemplateResponse("Home.html", {"request":request, "device_info" : device_info})





