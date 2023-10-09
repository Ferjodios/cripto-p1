import tkinter as tk
import json
from game import Game

class SearchMatch:
    def __init__(self, parent, player_data):
        self.player_data = player_data
        self.games_file = "json/games.json"
        self.games = self.abrir_json(self.games_file)

        parent.destroy()
        self.window = tk.Tk()
        self.configure_window()

    def configure_window(self):
        self.window.title("Untitled game uwu")
        self.window.geometry("500x500")
        title_label = tk.Label(self.window, text="¡A jugar!", font=("Helvetica", 20))
        title_label.pack(pady=(80, 40))

        button_font = ("Helvetica", 14)
        game = self.have_game_active()
        if game is not None:
            join_game_button = tk.Button(self.window, text="UNIRSE A LA PARTIDA", font=button_font, command=lambda: Game(self.window, game))
            join_game_button.pack(side="left", pady=5)
        else:
            matchmaking_button = tk.Button(self.window, text="CREAR PARTIDA", font=button_font, command=self.crear_partida())
            matchmaking_button.pack(side="left", padx=(80, 10), pady=5)

            search_match_button = tk.Button(self.window, text="BUSCAR PARTIDA", font=button_font, command=self.buscar_partida())
            search_match_button.pack(side="right", padx=(10, 80), pady=5)

    def crear_partida(self):
        new_game = {
            "id_partida": len(self.games) + 1,
            "id_jugador1": self.player_data["id"],
            "id_jugador2": None,
            "juego_activo": False,
            "datos_juego": {
                "personaje1": self.player_data["personaje"],
                "personaje2": None,
                "vida_jugador1": self.player_data["vida"],
                "vida_jugador2": None,
                "turno": "Jugador 1"
            }
        }
        self.games.append(new_game)
        self.guardar_partida_json(self.games_file)

    def buscar_partida(self):
        for game in self.games:
            if not game["juego_activo"]:
                game["juego_activo"] = True
                game["id_jugador2"] = self.player_data["id"]
                game["datos_juego"]["personaje2"] = self.player_data["personaje"]
                game["datos_juego"]["vida_jugador2"] = self.player_data["vida"]
                self.guardar_partida_json(self.games_file)
                Game(self.window, game)
            else:
                print("No hay ninguna partida activa, crea alguna primero")
        


    def abrir_json(self, archivo):
        try:
            with open(archivo, 'r') as file:
                datos = json.load(file)
            return datos
        except FileNotFoundError:
            print(f"El archivo '{file}' no se encontró.")
            return None
        except json.JSONDecodeError:
            print(f"El archivo '{file}' no contiene un formato JSON válido.")
            return None
        
    def have_game_active(self):
        for partida in self.games:
            if partida["juego_activo"] and (self.player_data["id"] == partida["id_jugador1"] or self.player_data["id"] == partida["id_jugador2"]):
                return partida
        return None
    
    def guardar_partida_json(self, archivo):
        with open(archivo, 'w') as file:
            json.dump(self.games, file, indent=4)