


# Verificar si CMake está instalado, e instalarlo si no lo está
if ! command -v cmake &> /dev/null
then
  echo "CMake no encontrado, procediendo con instalación..."
  apt-get install -y cmake
else
  echo "CMake ya está instalado."
fi




pip install --upgrade pip setuptools wheel

source /home/site/wwwroot/.venv/Scripts/activate

uvicorn.run(app, host="0.0.0.0", port=8000)
