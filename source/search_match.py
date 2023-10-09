import tkinter as tk
import json
from game import Game

class SearchMatch:
    def __init__(self, parent, player_id):
        self.player_id = player_id
        self.game = None
        self.datos = self.abrir_json("json/games.json")

        parent.destroy()
        self.window = tk.Tk()
        self.configure_window()

    def configure_window(self):
        self.window.title("Untitled game uwu")
        self.window.geometry("500x500")
        title_label = tk.Label(self.window, text="¡A jugar!", font=("Helvetica", 20))
        title_label.pack(pady=(80, 40))

        button_font = ("Helvetica", 14)
        self.game = self.have_game_active()
        if self.game is not None:
            join_game_button = tk.Button(self.window, text="UNIRSE A LA PARTIDA", font=button_font, command=lambda: Game(self.window, self.game))
            join_game_button.pack(side="left", pady=5)
        else:
            matchmaking_button = tk.Button(self.window, text="CREAR PARTIDA", font=button_font, command=self.crear_partida())
            matchmaking_button.pack(side="left", padx=(80, 10), pady=5)

            search_match_button = tk.Button(self.window, text="BUSCAR PARTIDA", font=button_font, command=self.buscar_partida())
            search_match_button.pack(side="right", padx=(10, 80), pady=5)

    def crear_partida(self):
        pass

    def buscar_partida(self):
        pass


    def abrir_json(self, archivo):
        try:
            with open(archivo, 'r') as archivo:
                datos = json.load(archivo)
            return datos
        except FileNotFoundError:
            print(f"El archivo '{archivo}' no se encontró.")
            return None
        except json.JSONDecodeError:
            print(f"El archivo '{archivo}' no contiene un formato JSON válido.")
            return None
        
    def have_game_active(self):
        for partida in self.datos:
            if partida["juego_activo"] and (self.player_id == partida["id_jugador1"] or self.player_id == partida["id_jugador2"]):
                return partida
        return None