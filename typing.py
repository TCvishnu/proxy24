import npyscreen
import time
import requests
import json

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

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        response_data = response.json()
        return response_data['candidates'][0]['content']['parts'][0]['text']
    else:
        return f"Error: {response.status_code} - {response.text}"

def calculate_accuracy(correct, userstring):
    correct_length = len(correct)
    userstring = userstring + ' ' * (correct_length - len(userstring))
    matches = 0
    for i in range(correct_length):
        if correct[i] == userstring[i]:
            matches += 1
    accuracy = (matches / correct_length) * 100
    return accuracy

class SpeedTrackingApp(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm('MAIN', SpeedTrackingForm, name="Typing Speed Tracker")

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
        self.typing_area.when_cursor_moved = self.on_text_changed

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
            self.result_box.value = "Started typing..."
        else:
            self.result_box.value = f"Error: {self.typing_text}"

        self.display()

    def on_text_changed(self):
        if self.start_time is None and self.typing_area.value:
            self.start_time = time.time()

        if self.typing_area.value and self.typing_area.value[-1] == '\n':
            self.end_typing()

    def end_typing(self):
        if self.start_time:
            self.end_time = time.time()
            time_taken = self.end_time - self.start_time
            text = self.typing_area.value.rstrip('\n')
            word_count = len(text.split())
            char_count = len(text)

            minutes = time_taken / 60
            wpm = word_count / minutes if minutes > 0 else 0
            cpm = char_count / minutes if minutes > 0 else 0
            
            accuracy = calculate_accuracy(self.typing_text, text)  # Calculate accuracy

            self.result_box.value = (f"Time Taken: {time_taken:.2f} seconds\n"
                                     f"WPM: {wpm:.2f}\n"
                                     f"CPM: {cpm:.2f}\n"
                                     f"Accuracy: {accuracy:.2f}%")
        else:
            self.result_box.value = "You need to start typing first."
        
        self.display()

# if __name__ == "__main__":
#     app = SpeedTrackingApp()
#     app.run()