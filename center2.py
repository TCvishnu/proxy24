import npyscreen
import time
import requests
import json
from create_gameroom import start_game
from join_gameroom import join_game
from timeralso import QuizApp
from increment_score_player2 import update_player2_score

# Function to call Gemini API and get the text
def send_gemini_request(api_key, prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
    
    headers = {
        'Content-Type': 'application/json',
    }

    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }

    # Send POST request
    response = requests.post(url, headers=headers, data=json.dumps(data))

    # Return the response in JSON format if available
    if response.status_code == 200:
        response_data = response.json()
        return response_data['candidates'][0]['content']['parts'][0]['text']
    else:
        return f"Error: {response.status_code} - {response.text}"

def calculate_accuracy(correct, userstring):
    correct_length = len(correct)
    userstring = userstring + ' ' * (correct_length - len(userstring))  # Pad user string for comparison
    matches = 0
    for i in range(correct_length):
        if correct[i] == userstring[i]:
            matches += 1
    accuracy = (matches / correct_length) * 100
    return accuracy

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
        self.addForm("TYPING_TEST", SpeedTrackingForm, name="Typing Speed Test")  # New form for typing test

class MainForm(npyscreen.ActionForm):
    def create(self):
        y, x = self.useable_space()
        center_x = int((x - 20) / 2)
        center_y = int(y / 3) 

        self.create_button = self.add(npyscreen.ButtonPress, name="Create a Game Room", when_pressed_function=self.create_game_room, relx=center_x, rely=center_y)
        self.join_button = self.add(npyscreen.ButtonPress, name="Join a Game Room", when_pressed_function=self.join_game_room, relx=center_x, rely=center_y + 2)
        self.typing_test_button = self.add(npyscreen.ButtonPress, name="Start Typing Test", when_pressed_function=self.start_typing_test, relx=center_x, rely=center_y + 4)

    def create_game_room(self):
        self.parentApp.switchForm("PLAYER")

    def join_game_room(self):
        self.parentApp.switchForm("USERNAME")

    def start_typing_test(self):
        self.parentApp.switchForm("TYPING_TEST")

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

        self.gameRoomID_display = self.add(npyscreen.FixedText, value="", relx=center_x, rely=center_y + 12)

    def start_the_game(self):
        self.parentApp.player1 = self.player1.value
        self.parentApp.topic = self.topic.value
        question_count = self.noOfQns.value
        
        game_id = start_game(question_count, self.parentApp.topic, self.parentApp.player1)
        
        self.gameRoomID_display.value = f"Game Room ID: {game_id}"
        self.display()
        
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

# Speed Tracking Form
class SpeedTrackingForm(npyscreen.ActionForm):
    def create(self):
        self.start_time = None
        self.end_time = None
        self.typing_text = ""

        self.start_button = self.add(npyscreen.ButtonPress, name="Start Typing", when_pressed_function=self.start_typing)

        self.typing_area = self.add(npyscreen.MultiLineEdit, 
                                    max_height=10, 
                                    value="", 
                                    name="Type Here",
                                    scroll_exit=True)
        self.typing_area.editable = True
        self.typing_area.when_key_pressed = self.on_key_press  # Change here

        self.text_display = self.add(npyscreen.TitleText, name="Text to Type:", value="", editable=False)
        self.result_box = self.add(npyscreen.TitleText, name="Results:", value="", editable=False)

        self.add(npyscreen.FixedText, value="Press Enter after typing to end.")

    def start_typing(self):
        prompt = "Generate a short text to test typing speed."
        api_key = "AIzaSyBhUr1FEJIzWWNXo9KXuFZ39h4Qeq2692U"  # Replace with your actual API key
        self.typing_text = send_gemini_request(api_key, prompt)

        if not self.typing_text.startswith("Error"):
            self.text_display.value = self.typing_text
            self.typing_area.value = ""
            self.result_box.value = ""
            self.display()

            self.start_time = time.time()
            self.end_time = None  # Reset end time when starting a new typing test
        else:
            npyscreen.notify_confirm("Failed to get typing text.", title="Error")

    def on_key_press(self, key):
        if key in (npyscreen.PGUP, npyscreen.PGDN, npyscreen.KEY_ENTER):  # Check for Enter key
            if self.typing_area.value and self.end_time is None:  # Only calculate if there is input
                self.end_time = time.time()
                elapsed_time = self.end_time - self.start_time
                
                user_input = self.typing_area.value
                accuracy = calculate_accuracy(self.typing_text, user_input)
                self.result_box.value = f"Time: {elapsed_time:.2f} seconds\nAccuracy: {accuracy:.2f}%"
                
                self.display()
        
        # Pass the key press to the MultiLineEdit to handle normal behavior
        self.typing_area.value = self.typing_area.value  # This keeps the current value intact
        self.typing_area.editable = True  # Ensures the typing area is still editable
        return super().on_key_press(key)  # Call the parent method

# Start the application
if __name__ == "__main__":
    app = GameRoomApp()
    app.run()


# Start the application
if __name__ == "__main__":
    app = GameRoomApp()
    app.run()
