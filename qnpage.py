import npyscreen
import time
import threading
import signal
import sys

class GameForm(npyscreen.Form):
    def create(self):
        self.question_number = 1
        self.total_questions = 5
        self.player_score = 0
        self.opponent_score = 0

        self.timer = self.add(npyscreen.TitleText, name="Time Remaining:", value="60", editable=False)
        self.question_text = self.add(npyscreen.TitleText, name=f"Question {self.question_number}:", value="What is 2 + 2?", editable=False)
        self.answer_input = self.add(npyscreen.TitleText, name="Your Answer:", value="", editable=True)
        self.question_info = self.add(npyscreen.TitleText, name="Progress:", value=f"Question {self.question_number} of {self.total_questions}", editable=False)

        self.player_score_field = self.add(npyscreen.TitleText, name="You:", value=str(self.player_score), editable=False)
        self.opponent_score_field = self.add(npyscreen.TitleText, name="Opponent:", value=str(self.opponent_score), editable=False)

        self.timer_thread = threading.Thread(target=self.start_timer)
        self.timer_thread.daemon = True  # Allow thread to close on exit
        self.timer_thread.start()

    def start_timer(self):
        for remaining in range(60, -1, -1):
            time.sleep(1)
            self.timer.value = str(remaining)
            self.display()

        npyscreen.notify_confirm('Time is up! Please submit your answer.', title='Time Up')

    def afterEditing(self):
        answer = self.answer_input.value
        
        if answer == "4":
            self.player_score += 1
        


        self.player_score_field.value = str(self.player_score)
        self.opponent_score_field.value = str(self.opponent_score)
        self.display()

        npyscreen.notify_confirm(f'Your answer is: {answer}\nYou: {self.player_score} | Opponent: {self.opponent_score}', title='Answer Submitted')
        
        if self.question_number < self.total_questions:
            self.question_number += 1
            self.question_text.value = f"What is 2 + {self.question_number}?"  # Example placeholder question
            self.question_info.value = f"Question {self.question_number} of {self.total_questions}"
            self.answer_input.value = ""  # Clear the previous answer
        else:
            npyscreen.notify_confirm(f'Game Over!\nFinal Score - You: {self.player_score} | Opponent: {self.opponent_score}', title='Game Over')
            self.parentApp.setNextForm(None)

class GameApp(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm('MAIN', GameForm)

def signal_handler(sig, frame):
    sys.exit(0)  # Exit cleanly

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)

    app = GameApp()
    app.run()
