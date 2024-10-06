import npyscreen

class GameRoomApp(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm("MAIN", MainForm, name="Game Room Application")

class MainForm(npyscreen.ActionForm):
    def create(self):
        self.create_button = self.add(npyscreen.ButtonPress, name="Create a Game Room", when_pressed_function=self.create_game_room)
        self.join_button = self.add(npyscreen.ButtonPress, name="Join a Game Room", when_pressed_function=self.join_game_room)

    def create_game_room(self):
        npyscreen.notify_confirm("Game room created!", title="Game Room")

    def join_game_room(self):
        username_form = UsernameForm(name="Join Game Room")
        username_form.edit() 
        if username_form.username:
            npyscreen.notify_confirm(f"Joining game room as {username_form.username}", title="Joining Game Room")

class UsernameForm(npyscreen.ActionForm):
    def create(self):
        self.username = self.add(npyscreen.TitleText, name="Enter provided username:")
        self.submit_button = self.add(npyscreen.ButtonPress, name="Join", when_pressed_function=self.on_join)

    def on_join(self):
        self.parentApp.setNextForm(None)

if __name__ == "__main__":
    app = GameRoomApp()
    app.run()
