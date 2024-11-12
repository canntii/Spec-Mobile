from pydantic import BaseModel

class ImageData(BaseModel):
    user_image_base64: str

