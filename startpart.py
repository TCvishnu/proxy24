import npyscreen
import asyncio
from create_gameroom import start_game

class MainApp(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm("MAIN", MainForm)
        self.addForm("CREATE_ROOM", CreateRoomForm)
        self.addForm("JOIN_ROOM", JoinRoomForm)

class MainForm(npyscreen.Form):
    def create(self):
        self.add(npyscreen.ButtonPress, name="Create a Game Room", when_pressed=self.goto_create_room)
        self.add(npyscreen.ButtonPress, name="Join a Game Room", when_pressed=self.goto_join_room)

    def goto_create_room(self):
        self.parentApp.switchForm("CREATE_ROOM")

    def goto_join_room(self):
        self.parentApp.switchForm("JOIN_ROOM")

class CreateRoomForm(npyscreen.Form):
    def create(self):
        self.username = self.add(npyscreen.TitleText, name="Username:")
        self.topic = self.add(npyscreen.TitleText, name="Topic:")
        self.num_questions = self.add(npyscreen.TitleText, name="Number of Questions:")
        self.start_button = self.add(npyscreen.ButtonPress, name="Start", when_pressed=self.start_game)

    def start_game(self):
        username = self.username.value
        topic = self.topic.value
        num_questions = self.num_questions.value

        # Check if the input fields are filled
        if not username or not topic or not num_questions:
            npyscreen.notify_confirm("Please fill in all fields.")
            return

        # Schedule the async function to run
        asyncio.create_task(self.create_room(username, topic, int(num_questions)))

    async def create_room(self, username, topic, num_questions):
        # Call the async function to start the game
        game_room_id = await start_game(username, topic, num_questions)
        npyscreen.notify_confirm(f"Game Room Created! ID: {game_room_id}")
        self.parentApp.switchForm("MAIN")  # Go back to the main menu


class JoinRoomForm(npyscreen.Form):
    def create(self):
        self.username = self.add(npyscreen.TitleText, name="Username:")
        self.game_room_id = self.add(npyscreen.TitleText, name="Game Room ID:")
        self.join_button = self.add(npyscreen.ButtonPress, name="Join", when_pressed=self.join_game)

    def join_game(self):
        username = self.username.value
        game_room_id = self.game_room_id.value
        npyscreen.notify_confirm(f"Joining Game Room ID: {game_room_id} as {username}")
        self.parentApp.switchForm("MAIN")  # Go back to the main menu

if __name__ == "__main__":
    app = MainApp()
    app.run()
