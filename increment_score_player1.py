# from firebase_admin import credentials, firestore, initialize_app

# cred = credentials.Certificate("./cligame-firebase-adminsdk-oju86-c97312a6fb.json")
# initialize_app(cred)
from firebase_config import db
from utility import questions

def update_player1_score(game_id, player1_answer, correct_answer):
    # Reference to the game document in Firestore
    # db = firestore.client()
    game_ref = db.collection('games').document(game_id)
    # correct_answer = questions[question_number - 1]['ans']
    # Check if the game exists
    game = game_ref.get()
    
    if game.exists:
        game_data = game.to_dict()
        
        # Initialize Player 1's score
        player1_score = game_data['player1']['score']
        
        # Check if Player 1's answer is correct
        if player1_answer == correct_answer:
            player1_score += 1  # Increment Player 1's score
            print(f"Player 1's answer is correct! New score: {player1_score}")
        
        # Update Player 1's score in Firestore
        game_ref.update({
            'player1.score': player1_score
        })
        
        print(f"Scores updated for game room {game_id}: Player 1: {player1_score}")
    else:
        print(f"Game room with ID {game_id} does not exist")

# update_player1_score("sadasda", 1, 1)