import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("./cligame-firebase-adminsdk-oju86-c97312a6fb.json")
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()