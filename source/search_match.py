import tkinter as tk
from tkinter import messagebox
from game import Game
from json_match_handler import JsonMatchHandler
from json_character_handler import JsonCharacterHandler
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

class SearchMatch:
    def __init__(self, parent, player_user, player_champ, player_password):
        self.player_user = player_user
        self.player_champ = player_champ
        self.player_password = player_password
        self.games = JsonMatchHandler('json/games.json')
        self.characterHandler = JsonCharacterHandler('json/characters.json')
        if not self.check_if_already_in_game(parent):
            parent.destroy()
            self.window = tk.Tk()
            self.configure_window()

    def configure_window(self):
        self.window.title("Titanomachy")
        self.window.geometry("500x500")
        self.window.resizable(False, False)
        self.window.configure(bg='#333333')
        title_label = tk.Label(self.window, text="¡A jugar!",bg='#333333', fg="#FF3399", font=("Arial", 30))
        title_label.pack(pady=(80, 40))

        button_font = ("Arial", 16)
        matchmaking_button = tk.Button(self.window, text="CREAR PARTIDA", font=button_font, bg="#FF3399", fg="#FFFFFF", command=self.crear_partida)
        matchmaking_button.pack(side="left", padx=(50, 10), pady=5)

        search_match_button = tk.Button(self.window, text="BUSCAR PARTIDA", font=button_font, bg="#FF3399", fg="#FFFFFF", command=self.buscar_partida)
        search_match_button.pack(side="right", padx=(10, 50), pady=5)

    def check_if_already_in_game(self, parent):
        if self.games.already_in_game(self.player_user):
            game = self.games.have_game_active(self.player_user)
            if game is not None:
                Game(parent, game, self.player_user, self.player_password)
            else:
                messagebox.showinfo("Info", "Aún no se ha encontrado partida, vuelva más tarde")
                parent.destroy()
            return True
        return False
            
    #Aquí tengo que cambiar el formato del json para tener las dos claves publicas como atributos en vez de key        
    def crear_partida(self):
        new_game = {
            "id_partida": self.games.new_match_id(),
            "id_jugador1": self.player_user,
            "id_jugador2": "",
            "juego_activo": False,
            "cripto": {
                "token": "",
                "public_jugador1": self.get_public_password(),
                "public_jugador2": ""
            },
            "datos_juego": {
                "personaje1": self.player_champ,
                "personaje2": None,
                "turno": "Jugador 2"
            },
            "stats1": self.characterHandler.get_stats_by_name(self.player_champ),
            "stats2": {
                "VIDA": 100,
                "DEFENSA": 40,
                "RESISTENCIA": 25, 
                "EVASION": 15, 
                "ATAQUE": 30 
            }
        }
        messagebox.showinfo("Info", "Se ha creado tu partida, vuelva cuando se haya unido alguien")
        self.games.save_new_match(new_game)
        self.window.destroy()

    def buscar_partida(self):
        inactive_game = self.games.search_inactive_match()
        if inactive_game is None:
            self.crear_partida()

        else:
            inactive_game["juego_activo"] = True
            inactive_game["id_jugador2"] = self.player_user
            inactive_game["datos_juego"]["personaje2"] = self.player_champ
            inactive_game["stats2"] = self.characterHandler.get_stats_by_name(self.player_champ)
            inactive_game["cripto"]["public_jugador2"] = self.get_public_password()
            self.games.update_game(inactive_game, inactive_game["id_partida"])
            messagebox.showinfo("Info", "Partida encontrada")
            Game(self.window, inactive_game, self.player_user, self.player_password)

    def get_public_password(self):
        password = self.player_password.encode('utf-8')
        #Generar clave privada
        hashed_password = SHA256.new(password).digest()

        private_key = RSA.import_key(hashed_password)

        #Derivo la clave publica a partir de la privada
        n = private_key.n
        e = private_key.e
        return RSA.construct((n, e))