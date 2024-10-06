# import firebase_admin
# from firebase_admin import credentials, firestore

# # Initialize Firebase Admin SDK
# from firebase_config import db

# # Data to add to Firestore
# data = {
#     'name': 'ggg',  # This is the document name
#     'description': 'This is a sample document for the collection.',
#     'timestamp': firestore.SERVER_TIMESTAMP  # Optional: add a timestamp
# }

# # Add a document to the 'db' collection

# # doc_ref.set(data)  # Use set instead of add to specify document ID

# # print("Document added to Firestore successfully.")

# # Function to listen for changes in the document
# def listen_for_changes(doc_name):
#     doc_ref = db.collection('gamesDB').document(doc_name)
#     # Define the callback function
#     def callback(doc_snapshot, changes, read_time):
#         for doc in doc_snapshot:
#             # Print the new name value whenever it changes
#             print(f"New name: {doc.to_dict().get('player1')}")

#     # Start listening to changes in the document
#     doc_watch = doc_ref.on_snapshot(callback)

#     # Keep the listener alive (you might want to adjust this in a real application)
#     print("Listening for changes to the document...")
#     while True:
#         pass  # Keep the script running to listen for changes

# # Call the listener function
# listen_for_changes(doc_ref)


from firebase_config import db
def listen_for_changes(doc_name):
    doc_ref = db.collection('gamesDB').document(doc_name)

    # Define the callback function
    def callback(doc_snapshot, changes, read_time):
        for doc in doc_snapshot:
            data = doc.to_dict()
            # Get the scores of both players
            player1_score = data.get('player1', {}).get('score', 0)
            player2_score = data.get('player2', {}).get('score', 0)
            
            # Return the scores as a tuple or list
            print(f"Player 1 Score: {player1_score}, Player 2 Score: {player2_score}")
            return (player1_score, player2_score)

    # Start listening to changes in the document
    doc_watch = doc_ref.on_snapshot(callback)

    # Keep the listener alive (you might want to adjust this in a real application)
    print("Listening for changes to the document...")
    while True:
        pass  # Keep the script running to listen for changes
listen_for_changes()