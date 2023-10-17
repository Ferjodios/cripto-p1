import tkinter as tk
import json
from game import Game
from json_match_handler import JsonMatchHandler

class SearchMatch:
    def __init__(self, parent, player_user, player_champ):
        self.player_user = player_user
        self.player_champ = player_champ
        self.games = JsonMatchHandler('json/games.json')

        parent.destroy()
        self.window = tk.Tk()
        self.configure_window()

    def configure_window(self):
        self.window.title("Untitled game uwu")
        self.window.geometry("500x500")
        title_label = tk.Label(self.window, text="¡A jugar!", font=("Helvetica", 20))
        title_label.pack(pady=(80, 40))

        button_font = ("Helvetica", 14)
        game = self.games.have_game_active(self.player_user)
        if game is not None:
            join_game_button = tk.Button(self.window, text="UNIRSE A LA PARTIDA", font=button_font, command=lambda: Game(self.window, game))
            join_game_button.pack(side="left", pady=5)
        else:
            matchmaking_button = tk.Button(self.window, text="CREAR PARTIDA", font=button_font, command=self.crear_partida)
            matchmaking_button.pack(side="left", padx=(60, 10), pady=5)

            search_match_button = tk.Button(self.window, text="BUSCAR PARTIDA", font=button_font, command=self.buscar_partida)
            search_match_button.pack(side="right", padx=(10, 60), pady=5)

    def crear_partida(self):
        new_game = {
            "id_partida": self.games.new_match_id(),
            "id_jugador1": self.player_user,
            "id_jugador2": None,
            "juego_activo": False,
            "datos_juego": {
                "personaje1": self.player_champ,
                "personaje2": None,
                "vida_jugador1": 100,
                "vida_jugador2": None,
                "turno": "Jugador 1"
            }
        }
        self.games.save_new_match(new_game)

    def buscar_partida(self):
        inactive_game = self.games.search_inactive_match()
        if inactive_game is None:
            self.crear_partida
        else:
            inactive_game["juego_activo"] = True
            inactive_game["id_jugador2"] = self.player_user
            inactive_game["datos_juego"]["personaje2"] = self.player_champ
            inactive_game["datos_juego"]["vida_jugador2"] = 100
            self.games.update_game(inactive_game, inactive_game["id_partida"])
            Game(self.window, inactive_game)
