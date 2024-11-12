
const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const snapButton = document.getElementById('snap');

//Acceder a la camara

navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        video.srcObject = stream;
    })
    .catch(err => {
        console.error("Error accessing the camera: ", err);
    });

// Capturar la imagen al hacer clic en el botón "Take Photo"
snapButton.addEventListener('click', () => {
    const context = canvas.getContext('2d');
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    const imageDataUrl = canvas.toDataURL('image/png');
    document.getElementById('imageUrl').value = imageDataUrl; // Guardar la imagen en el campo oculto
});

async function registerUser() {
    const formData = {
        userName: document.getElementById('userName').value,
        UserLastName: document.getElementById('UserLastName').value,
        cedula: document.getElementById('cedula').value,
        email: document.getElementById('email').value,
        image64: document.getElementById('imageUrl').value,
        password : document.getElementById('password').value
    };

    try {
        const response = await fetch('http://127.0.0.1:8000/create-user', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        if (response.ok) {
            const data = await response.json();
            alert(`User created successfully: ${data.userName}`);
        } else {
            alert('Error creating user: ' + response.statusText);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error connecting to the server.');
    }
}
