import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("./cligame-firebase-adminsdk-oju86-c97312a6fb.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

data = {
    'name': 'ggg',  # This is the document name
    'description': 'This is a sample document for the collection.',
    'timestamp': firestore.SERVER_TIMESTAMP  # Optional: add a timestamp
}


doc_ref = db.collection('DB').document('ggg')
doc_ref.set(data)  # Use set instead of add to specify document ID

print("Document added to Firestore successfully.")

def listen_for_changes(doc_ref):

    def callback(doc_snapshot, changes, read_time):
        for doc in doc_snapshot:
            # Print the new name value whenever it changes
            print(f"New name: {doc.to_dict().get('name')}")

    # Start listening to changes in the document
    doc_watch = doc_ref.on_snapshot(callback)

    print("Listening for changes to the document...")
    while True:
        pass  # Keep the script running to listen for changes

# Call the listener function
listen_for_changes(doc_ref)