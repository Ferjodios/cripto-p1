import tkinter as tk

class Game:
    def __init__(self, parent, game_data):
        self.game_data = game_data

        parent.destroy()
        self.window = tk.Tk()
        self.configure_window()

    def configure_window():
        pass