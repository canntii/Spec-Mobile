import firebase_admin
from firebase_admin import credentials, firestore, storage

class FirebaseService:
    _instance = None
    _service_account_key = "serviceAccountKey.json"
    _storage_bucket = "gs://userface-b47eb.firebasestorage.app"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # Inicializar Firebase una sola vez
            cred = credentials.Certificate(cls._service_account_key)
            firebase_admin.initialize_app(cred, {'storageBucket': cls._storage_bucket})
            cls._instance.db = firestore.client()
            cls._instance.bucket = storage.bucket()
        return cls._instance

    def get_db(self):
        return self.db

    def get_bucket(self):
        return self.bucket