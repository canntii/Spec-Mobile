const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const context = canvas.getContext('2d');
const messageDiv = document.getElementById('message');

// Acceder a la cámara
navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        video.srcObject = stream;
    })
    .catch(err => {
        console.error("Error al acceder a la cámara: ", err);
        messageDiv.textContent = 'No se pudo acceder a la cámara.';
    });

// Función para capturar la ubicación del usuario
function getLocation(){
    return new Promise((resolve, reject) => {
        if(!navigator.geolocation){
            reject('La geolocalización no es compatible con este navegador');
        }
        navigator.geolocation.getCurrentPosition(
            position => resolve({
                latitude: position.coords.latitude,
                longitude: position.coords.longitude
            }),
            error => reject('Error al obtener la ubicación: ' + error.message),
            {
                enableHighAccuracy: true,
                maximumAge: 0,
                timeout: 5000
            }
        );
    });
}

// Capturar imagen y enviar al backend
document.getElementById('capture').addEventListener('click', async () => {
    // Capturar la imagen
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    const imageDataUrl = canvas.toDataURL('image/png');


    try {
        // Enviar la imagen al endpoint /compare
        await fetch('http://127.0.0.1:8000/compare', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ user_image_base64: imageDataUrl })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Error en la respuesta del servidor: ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            const resultMessage = data.comparison_result || 'Comparación realizada con éxito';
            messageDiv.textContent = `${data.message || 'Comparación realizada con éxito'}: ${resultMessage}`;
        })
        .catch((error) => {
            console.error('Error en la comparación de imagen:', error);
            messageDiv.textContent = 'Ocurrió un error al procesar la imagen.';
        });

        // Obtener la ubicación del usuario
        const location = await getLocation();

        ubicacionFormateada = `https://www.google.com/maps?q=${location.latitude},${location.longitude}`

        await fetch('http://127.0.0.1:8000/agregar-registro', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                ubicacion: `https://www.google.com/maps?q=${location.latitude},${location.longitude}`
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Error en la respuesta del servidor: ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            messageDiv.textContent += `\nRegistro creado con éxito:`;
        })
        .catch((error) => {
            console.error('Error al registrar ubicación y hora:', error);
            messageDiv.textContent += '\nOcurrió un error al registrar la ubicación y hora.';
        });

    } catch(error) {
        console.error('Error al obtener la ubicación:', error);
        messageDiv.textContent = 'No se pudo obtener la ubicación del usuario.';
    }
});