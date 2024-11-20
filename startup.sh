


# Actualizar índices de paquetes e instalar CMake si no está presente
if ! command -v cmake &> /dev/null
then
  echo "CMake no encontrado, procediendo con actualización de índices e instalación..."
  apt-get update -y && apt-get install -y cmake
else
  echo "CMake ya está instalado."
fi

# Actualizar pip, setuptools y wheel
pip install --upgrade pip setuptools wheel



pip install --upgrade pip setuptools wheel

source /home/site/wwwroot/.venv/Scripts/activate

uvicorn.run(app, host="0.0.0.0", port=8000)
