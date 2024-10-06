import npyscreen
import threading
import time
from firebase_config import db

def update_player2_score(game_id, scoree):
    # Reference to the game document in Firestore

    # db = firestore.client()
    game_ref = db.collection('gamesDB').document(game_id)
    
    # Check if the game exists
    game = game_ref.get()
    scoree = int(scoree)
    
    if game.exists:
        game_data = game.to_dict()
        
        # Initialize Player 2's score
        player2_score = game_data['player2']['score']
        
        # Check if Player 2's answer is correct
        # if player2_answer == correct_answer:
        #     player2_score += 1  # Increment Player 2's score
            # print(f"Player 2's answer is correct! New score: {player2_score}")
        
        # Update Player 2's score in Firestore
        game_ref.update({
            'player2.score': 1
        })
        
        print(f"Scores updated for game room {game_id}: Player 2: {player2_score}")
        return True
    else:
        # print(f"Game room with ID {game_id} does not exist")
        return False


class QuizApp(npyscreen.NPSAppManaged):
    def __init__(self, questions, playerNumber, game_id):
        super().__init__()
        self.questions = questions
        self.current_question_index = 0
        self.user_score = 0
        self.opponent_score = 0
        self.timer = 60
        self.game_id = game_id
        self.playerNumber = playerNumber 
        self.timer_running = True
        self.timer_thread = None

    def onStart(self):
        self.addForm("MAIN", QuizForm, name="Quiz Game", playerNumber=self.playerNumber, game_id=self.game_id)

    def switch_to_results(self):
        self.addForm("RESULTS", ResultsForm, name="Quiz Results", playerNumber=self.playerNumber, game_id=self.game_id, user_score=self.user_score)
        self.switchForm("RESULTS")

class QuizApp1(npyscreen.NPSAppManaged):
    def __init__(self, questions, playerNumber, game_id):
        super().__init__()
        self.questions = questions
        self.current_question_index = 0
        self.user_score = 0
        self.opponent_score = 0
        self.timer = 60
        self.game_id = game_id
        self.playerNumber = playerNumber 
        self.timer_running = True
        self.timer_thread = None

    def onStart(self):
        self.addForm("MAIN", QuizForm, name="Quiz Game", playerNumber=self.playerNumber, game_id=self.game_id)

    def switch_to_results(self):
        self.addForm("RESULTS", ResultsForm, name="Quiz Results", playerNumber=self.playerNumber, game_id=self.game_id, user_score=self.user_score)
        self.switchForm("RESULTS")


class QuizForm(npyscreen.ActionForm):
    def create(self):
        self.app = self.parentApp
        self.game_id = self.app.game_id
        self.playerNumber = self.app.playerNumber

        # Display Player Number
        self.player_number_widget = self.add(npyscreen.FixedText, value=f"Player Number: {self.playerNumber}", editable=False)

        # Display Game ID
        self.game_id_widget = self.add(npyscreen.FixedText, value=f"Game ID: {self.game_id}", editable=False)

        self.user_score_widget = self.add(npyscreen.FixedText, value=f"Your score: {self.app.user_score} pts", editable=False)
        self.opponent_score_widget = self.add(npyscreen.FixedText, value=f"Opponent score: {self.app.opponent_score} pts", editable=False)

        self.timer_widget = self.add(npyscreen.FixedText, value=f"Timer: {self.app.timer} seconds", editable=False)

        self.question_widget = self.add(npyscreen.FixedText, value=self.get_current_question(), editable=False)

        self.answer_input = self.add(npyscreen.TitleText, name="Your Answer:", value="", editable=True)

        total_questions = len(self.app.questions)
        self.qn_number_widget = self.add(npyscreen.FixedText, value=f"Question {self.app.current_question_index + 1}/{total_questions}", editable=False)

        # Button for navigating to results
        self.results_button = self.add(npyscreen.ButtonPress, name="See Results", when_pressed_function=self.go_to_results, hidden=True)

    def get_current_question(self):
        return f"Question: {self.app.questions[self.app.current_question_index]['question']}"

    def next_question(self):
        self.app.current_question_index += 1
        if self.app.current_question_index < len(self.app.questions):
            self.app.timer = 60
            self.question_widget.value = self.get_current_question()
            self.qn_number_widget.value = f"Question {self.app.current_question_index + 1}/{len(self.app.questions)}"
            self.answer_input.value = ''
            self.answer_input.display()
            self.question_widget.display()
            self.qn_number_widget.display()
            self.results_button.hidden = True  # Hide results button
        else:

            self.results_button.hidden = False  # Show results button
            self.results_button.display()

    def go_to_results(self):
        if increment_score_player2("1728178076.826021",4):
            # npyscreen.notify_confirm(f"Successfully joined game room {game_id} as {player2_name}!", title="Success")
            # self.parentApp.switchForm("MAIN")  # Switch back to the main form or another appropriate form
            # quiz_app1 = QuizApp1(questions, 1, game_id)
            # quiz_app1.run()
            pass
        else:
            npyscreen.notify_confirm(f"Failed to join game room {game_id}.", title="Error")


    def on_ok(self):
        user_answer = self.answer_input.value.strip().lower()  # Corrected reference to the input field
        correct_answer = self.app.questions[self.app.current_question_index]['answer'].lower()

        if user_answer == correct_answer:
            self.app.user_score += 1
            self.user_score_widget.value = f"Your score: {self.app.user_score} pts"
            self.user_score_widget.display()  # Update and refresh score
            self.next_question()
        else:
            npyscreen.notify_confirm("Incorrect, try again!", title="Incorrect")

    def on_cancel(self):
        self.app.timer_running = False
        self.editing = False

    def beforeEditing(self):
        self.app.timer_running = True
        self.start_timer()

    def start_timer(self):
        if self.app.timer_thread and self.app.timer_thread.is_alive():
            self.app.timer_running = False
            self.app.timer_thread.join()

        self.app.timer_running = True

        def timer_thread():
            while self.app.timer > 0 and self.app.timer_running:
                time.sleep(1)
                self.app.timer -= 1
                self.timer_widget.value = f"Timer: {self.app.timer} seconds"
                self.timer_widget.display()
            if self.app.timer == 0:
                npyscreen.notify_confirm("Time's up!", title="Time's up")
                self.app.timer_running = False
                self.editing = False

        self.app.timer_thread = threading.Thread(target=timer_thread, daemon=True)
        self.app.timer_thread.start()


class ResultsForm(npyscreen.ActionForm):
    def create(self):
        update_player2_score("1728178076.826021", 1)
        
        self.app = self.parentApp
        self.playerNumber = self.app.playerNumber
        self.game_id = self.app.game_id
        self.user_score = self.app.user_score


        self.final_score_widget = self.add(npyscreen.FixedText, value=f"Your final score: {self.user_score} pts", editable=False)
        
        # Button to navigate back to main or other page
        self.submit_button = self.add(npyscreen.ButtonPress, name="Continue", when_pressed_function=self.on_continue)

    def on_continue(self):
        # Functionality for the continue button can go here.
        # Example: Return to the main menu or reset the game.
        npyscreen.notify_confirm("Thank you for playing!", title="Quiz Complete")
        self.parentApp.switchForm("MAIN")  # or any other form you want to switch to

