import npyscreen
from create_gameroom import start_game
from join_gameroom import join_game
from timeralso import QuizApp
from increment_score_player2 import update_player2_score

questions = [
    {"question": "What is 2+2?", "answer": "4"},
    {"question": "What is the capital of France?", "answer": "Paris"},
    {"question": "What color is the sky?", "answer": "Blue"}
]

class GameRoomApp(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm("MAIN", MainForm, name="Game Room Application")
        self.addForm("PLAYER", PlayerForm, name="Player Information")
        self.addForm("GAME", GameForm, name="Game in Progress")
        self.addForm("USERNAME", UsernameForm, name="Join Game Room")

class MainForm(npyscreen.ActionForm):
    def create(self):
        y, x = self.useable_space()
        center_x = int((x - 20) / 2)
        center_y = int(y / 3)

        self.create_button = self.add(npyscreen.ButtonPress, name="Create a Game Room", when_pressed_function=self.create_game_room, relx=center_x, rely=center_y)
        self.join_button = self.add(npyscreen.ButtonPress, name="Join a Game Room", when_pressed_function=self.join_game_room, relx=center_x, rely=center_y + 2)

    def create_game_room(self):
        self.parentApp.switchForm("PLAYER")

    def join_game_room(self):
        self.parentApp.switchForm("USERNAME")

class UsernameForm(npyscreen.ActionForm):
    def create(self):
        y, x = self.useable_space()
        center_x = int((x - 40) / 2) 
        center_y = int(y / 4)

        self.username = self.add(npyscreen.TitleText, name="Enter your username:", relx=center_x, rely=center_y, max_width=100, max_height=5)

        self.gameRoomID = self.add(npyscreen.TitleText, name="Enter Game Room ID:", relx=center_x, rely=center_y + 2, max_width=100, max_height=5)
        self.submit_button = self.add(npyscreen.ButtonPress, name="Join", when_pressed_function=self.on_join, relx=center_x, rely=center_y + 5)
        self.back_button = self.add(npyscreen.ButtonPress, name="Back", when_pressed_function=self.go_back, relx=center_x, rely=center_y + 7)

    def on_join(self):
        player2_name = self.username.value
        game_id = self.gameRoomID.value
        print(game_id)

        if join_game(game_id, player2_name):
            # npyscreen.notify_confirm(f"Successfully joined game room {game_id} as {player2_name}!", title="Success")
            # self.parentApp.switchForm("MAIN")  # Switch back to the main form or another appropriate form
            quiz_app = QuizApp(questions, 1, game_id)
            quiz_app.run()
        else:
            npyscreen.notify_confirm(f"Failed to join game room {game_id}.", title="Error")

    def go_back(self):
        self.parentApp.switchForm("MAIN")


class PlayerForm(npyscreen.Form):
    def create(self):
        y, x = self.useable_space()
        center_x = int((x - 40) / 2)
        center_y = int(y / 4)

        self.add(npyscreen.FixedText, value="Welcome to the Two-Player Game!", editable=False, relx=center_x, rely=center_y, max_width=40)
        self.player1 = self.add(npyscreen.TitleText, name="Enter your Username:", relx=center_x, rely=center_y + 2, max_width=100, max_height=3)
        self.topic = self.add(npyscreen.TitleText, name="Game Topic:", relx=center_x, rely=center_y + 4, max_width=100, max_height=3)
        self.noOfQns = self.add(npyscreen.TitleText, name="Number of Questions:", relx=center_x, rely=center_y + 6, max_width=100, max_height=3)

        self.start_button = self.add(npyscreen.ButtonPress, name="Start", when_pressed_function=self.start_the_game, relx=center_x, rely=center_y + 8)
        self.back_button = self.add(npyscreen.ButtonPress, name="Back", when_pressed_function=self.go_back, relx=center_x, rely=center_y + 10)

        self.gameRoomID_display = self.add(npyscreen.FixedText, value="", relx=center_x, rely=center_y + 12)  # For displaying Game Room ID

    def start_the_game(self):
        self.parentApp.player1 = self.player1.value
        self.parentApp.topic = self.topic.value
        question_count = self.noOfQns.value
        
        game_id = start_game(question_count, self.parentApp.topic, self.parentApp.player1)
        
        self.gameRoomID_display.value = f"Game Room ID: {game_id}"
        self.display()
        
    
    # Switch to the quiz app
        quiz_app = QuizApp(questions, 0, game_id)
        quiz_app.run()

    def go_back(self):
        self.parentApp.switchForm("MAIN")

class GameForm(npyscreen.Form):
    def create(self):
        y, x = self.useable_space()
        center_x = int((x - 40) / 2)
        center_y = int(y / 4)

        self.add(npyscreen.FixedText, value="Game in Progress...", editable=False, relx=center_x, rely=center_y, max_width=40)
        
        self.player1_display = self.add(npyscreen.FixedText, value="", relx=center_x, rely=center_y + 2)
        self.topic_display = self.add(npyscreen.FixedText, value="", relx=center_x, rely=center_y + 6)
        
        self.add(npyscreen.FixedText, value="-" * 30, editable=False, relx=center_x, rely=center_y + 8)
        
    def beforeEditing(self):
        self.player1_display.value = f"Player 1: {self.parentApp.player1}"
        self.topic_display.value = f"Topic: {self.parentApp.topic}"
        
    def afterEditing(self):
        self.parentApp.switchForm(None)

if __name__ == "__main__":
    app = GameRoomApp()
    app.run()
