


# Actualizar índices de paquetes e instalar CMake si no está presente
apt-get update && apt-get install -y cmake

source /home/site/wwwroot/.venv/Scripts/activate

uvicorn.run(app, host="0.0.0.0", port=8000)
