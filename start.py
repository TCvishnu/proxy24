import npyscreen
import time

class PlayerForm(npyscreen.Form):
    """Form for player information input"""
    def create(self):
        self.add(npyscreen.FixedText, value="Welcome to the Two-Player Game!", editable=False)
        self.add(npyscreen.FixedText, value="-" * 30, editable=False)
        
        # Input fields for player usernames and game topic
        self.player1 = self.add(npyscreen.TitleText, name="Player 1 Username:")
        self.player2 = self.add(npyscreen.TitleText, name="Player 2 Username:")
        self.topic = self.add(npyscreen.TitleText, name="Game Topic:")
        
        # Start button
        self.add(npyscreen.ButtonPress, name="Start", when_pressed_function=self.start_game)
        
    def start_game(self):
        """Callback function when the Start button is pressed"""
        self.parentApp.player1 = self.player1.value
        self.parentApp.player2 = self.player2.value
        self.parentApp.topic = self.topic.value
        
        # Switch to the game interface after pressing Start
        self.parentApp.switchForm("GAME")


class GameForm(npyscreen.Form):
    """Form to display the game interface"""
    def create(self):
        self.add(npyscreen.FixedText, value="Game in Progress...", editable=False)
        
        # Display player names and game topic
        self.player1_display = self.add(npyscreen.FixedText, value="")
        self.player2_display = self.add(npyscreen.FixedText, value="")
        self.topic_display = self.add(npyscreen.FixedText, value="")
        
        self.add(npyscreen.FixedText, value="-" * 30, editable=False)
        
    def beforeEditing(self):
        """Update values before the form is shown"""
        self.player1_display.value = f"Player 1: {self.parentApp.player1}"
        self.player2_display.value = f"Player 2: {self.parentApp.player2}"
        self.topic_display.value = f"Topic: {self.parentApp.topic}"
        
    def afterEditing(self):
        """Simulate game progression when leaving the form"""
        self.parentApp.switchForm(None)
        print(f"\n{self.parentApp.player1} vs {self.parentApp.player2} in {self.parentApp.topic} is now in action! Good luck!\n")


class TwoPlayerGameApp(npyscreen.NPSAppManaged):
    """Main Application Class"""
    def onStart(self):
        # Initialize player information variables
        self.player1 = ""
        self.player2 = ""
        self.topic = ""
        
        # Register the forms
        self.addForm("MAIN", PlayerForm)
        self.addForm("GAME", GameForm)


if __name__ == "__main__":
    app = TwoPlayerGameApp()
    app.run()