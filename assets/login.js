// login.js
import { firebaseConfig } from './config.js';
import { initializeApp } from 'https://www.gstatic.com/firebasejs/9.16.0/firebase-app.js';
import { getAuth, signInWithEmailAndPassword } from 'https://www.gstatic.com/firebasejs/9.16.0/firebase-auth.js';

// Inicializa Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app); // Obtén la instancia de autenticación

document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevenir el envío del formulario

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    // Llamada a Firebase para iniciar sesión
    signInWithEmailAndPassword(auth, email, password)
        .then((userCredential) => {
            // Usuario autenticado, obtener el token
            return userCredential.user.getIdToken();
        })
        .then((token) => {
            // Aquí puedes enviar el token a tu backend
            return fetch('/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ token: token, email : email }), // Envía el token en el cuerpo de la solicitud
            });
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('Backend response:', data);
            console.log('Login exitoso');
        })
        .catch((error) => {
            // Manejo de errores
            const errorMessage = error.message;
            document.getElementById('errorMessage').innerText = errorMessage;
            document.getElementById('errorMessage').style.display = 'block';
            console.error('Error signing in:', error);
        });
});
