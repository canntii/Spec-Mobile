from pydantic import BaseModel

class ImageData(BaseModel):
    user_image_base64: str

class ImageResponse(BaseModel):
    faces: bool
    message: str

class CompareRequest(BaseModel):
    image_firebase: str
    image_webcam: str