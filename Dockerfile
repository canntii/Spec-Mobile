FROM python:3.12

# Actualizar los repositorios de APT
RUN apt-get update

# Actualiza el sistema e instala cmake
RUN apt-get update && apt-get install -y cmake

# Instalar libGL y dependencias de OpenCV
RUN apt-get install -y libgl1-mesa-glx

# Instalar bibliotecas adicionales de OpenCV
RUN apt-get install -y libglib2.0-0 libsm6 libxext6 libxrender1



ENV PIP_DISABLE_PIP_VERSION_CHECK=1

ENV PYTHONUNBUFFERED=1


WORKDIR /app

COPY . /app



RUN pip install -r requirements.txt


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
