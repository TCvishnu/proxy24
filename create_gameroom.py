from firebase_config import db
from datetime import datetime
from utility import questions



def start_game(question_count,topic,player1):
    timer_duration = 30
    game_id = str(datetime.now().timestamp()) # Timer in seconds

    # db = firestore.client()

    # Create a new game in Firestore
    db.collection('gamesDB').document(game_id).set({
        'player1': {'name': player1, 'score': 0},
        'player2': {'name': "", 'score': 0},
        'currentTurn': 'player1',
        'gameState': 'active',
        # 'questions': questions,
        'currentQuestionIndex': 0,
        'timer': timer_duration,
        'topic': topic,
        "questions": questions
    })

    return game_id