# firebase_config.py
import pyrebase
from datetime import datetime

config = {
    "apiKey": "AIzaSyB7gDx6VONsbszUWZGKqP5lTf8iHhXjEw0",
    "authDomain": "slip-gaji-novus.firebaseapp.com",
    "databaseURL": "https://slip-gaji-novus-default-rtdb.asia-southeast1.firebasedatabase.app/", 
    "projectId": "slip-gaji-novus",
    "storageBucket": "slip-gaji-novus.appspot.com",
    "messagingSenderId": "1069035610491",
    "appId": "1:1069035610491:web:8a3d7cfeee3e964f6f822f"
}

# Inisialisasi Firebase
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()
storage = firebase.storage()

def log_backup_event(status, message):
    db.child("backup_logs").push({
        "status": status,
        "timestamp": datetime.now().isoformat(),
        "message": message
    })
