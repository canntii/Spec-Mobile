


#Instalar cmake por si no esta instalado
if ! command -v cmake &> /de/null
then
  echo "CMake no encontrado, procediendo con instalacion..."
  apt-get install -y cmake
fi

source /home/site/wwwroot/.venv/Scripts/activate

uvicorn.run(app, host="0.0.0.0", port=8000)
