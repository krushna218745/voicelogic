import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("firebase_key.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

def save_turn(session_id, user_text, buyer_text, state):
    db.collection("sessions").document(session_id).collection("turns").add({
        "user": user_text,
        "buyer": buyer_text,
        "state": state
    })
