import json
from tkinter import messagebox
import os
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class JsonMatchHandler:
    def __init__(self, file):
        self.data = []
        self.file = file
        self.load_data(self.file)

    def load_data(self, file):
        """Funcion que carga los datos del json"""
        with open(file) as json_file:
            self.data = json.load(json_file)

    def save(self):
        # Guardar los datos en el archivo JSON
        with open(self.file, 'w') as json_file:
            json.dump(self.data, json_file, indent=4)

    def have_game_active(self, player_id):
        for partida in self.data:
            if partida["juego_activo"] and (player_id == partida["id_jugador1"] or player_id == partida["id_jugador2"]):
                return partida
        return None

    def new_match_id(self):
        if not self.data:
            return 1
        ultima_partida = max(self.data, key=lambda x: x["id_partida"])
        return ultima_partida["id_partida"] + 1
    
    def save_new_match(self, new_game):
        self.data.append(new_game)
        self.save()

    def search_inactive_match(self):
        for juego in self.data:
            if juego.get("juego_activo") is False:
                juego["id_partida"] = True
                return juego
        return None
    
    def update_game(self, new_game, game_id):
        for i, juego in enumerate(self.data):
            if juego["id_partida"] == game_id:
                self.data[i] = new_game
                self.save()
                return True
        return False