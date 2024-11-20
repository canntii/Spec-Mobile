FROM python:3.12

# Actualiza el sistema e instala cmake
RUN apt-get update && apt-get install -y cmake


ENV PIP_DISABLE_PIP_VERSION_CHECK=1

ENV PYTHONUNBUFFERED=1


WORKDIR /app

COPY . /app



RUN pip install -r requirements.txt

