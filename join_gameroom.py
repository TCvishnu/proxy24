from firebase_config import db
def join_game(game_id, player2_name):
    print("reached here bl;a bla adSFGRETH")
    game_ref = db.collection('games').document(game_id)
    
    game = game_ref.get()
    
    if game.exists:
        game_ref.update({
            'player2.name': player2_name,
            'gameState': 'waiting_for_player2'
        })
        print(f"Player 2's name has been updated to {player2_name} in game room {game_id}")
        return True
    else:
        print(f"Game room with ID {game_id} does not exist")
        return False
