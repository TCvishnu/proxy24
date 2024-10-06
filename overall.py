import npyscreen
import threading
import time

class QuizApp(npyscreen.NPSAppManaged):
    def __init__(self, questions):
        super().__init__()
        self.questions = questions
        self.current_question_index = 0
        self.user_score = 0
        self.opponent_score = 0
        self.timer = 60
        self.timer_running = True
        self.timer_thread = None
        self.gameRoomID_display = None  # Placeholder for game room ID display

    def onStart(self):
        self.addForm("MAIN", QuizForm, name="Quiz Game")
        
        # For demonstration, we'll set the game ID here
        game_id = "12345"  # Example game ID
        self.gameRoomID_display = f"Game Room ID: {game_id}"  # Set the game room ID
        print(self.gameRoomID_display)  # Print the game room ID to check if it's set
        
        # Start the game if gameRoomID_display is set
        if self.gameRoomID_display:
            self.start_game()  # Start the game if the room ID is displayed

    def start_game(self):
        self.current_question_index = 0  # Reset question index for new game
        self.user_score = 0
        self.opponent_score = 0
        self.timer = 60
        self.timer_running = True
        self.run()  # Start the app

class QuizForm(npyscreen.ActionForm):
    def create(self):
        self.app = self.parentApp

        self.user_score_widget = self.add(npyscreen.FixedText, value=f"Your score: {self.app.user_score} pts", editable=False)
        self.opponent_score_widget = self.add(npyscreen.FixedText, value=f"Opponent score: {self.app.opponent_score} pts", editable=False)

        self.timer_widget = self.add(npyscreen.FixedText, value=f"Timer: {self.app.timer} seconds", editable=False)

        self.question_widget = self.add(npyscreen.FixedText, value=self.get_current_question(), editable=False)

        self.answer_input = self.add(npyscreen.TitleText, name="Your Answer:", value="", editable=True)

        total_questions = len(self.app.questions)
        self.qn_number_widget = self.add(npyscreen.FixedText, value=f"Question {self.app.current_question_index + 1}/{total_questions}", editable=False)

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
        else:
            npyscreen.notify_confirm("Quiz Complete!", title="End")
            self.app.timer_running = False  # Stop the timer when the quiz ends
            self.editing = False

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

if __name__ == "__main__":
    questions = [
        {"question": "What is 2+2?", "answer": "4"},
        {"question": "What is the capital of France?", "answer": "Paris"},
        {"question": "What color is the sky?", "answer": "Blue"}
    ]

    app = QuizApp(questions)
    app.run()
