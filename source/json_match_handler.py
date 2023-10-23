import json
from cryptography.fernet import Fernet

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
                return juego
        return None
    
    def update_game(self, new_game, game_id):
        for i, juego in enumerate(self.data):
            if juego["id_partida"] == game_id:
                self.data[i] = new_game
                self.save()
                return True
        return False
    
    def already_in_game(self, id):
        for partida in self.data:
            if partida["id_jugador1"] == id or partida["id_jugador2"] == id:
                return True
        return False
    
    def atacar_y_cambiar_turno(self, game, ataque, soy_jugador1):
        game = self.encriptar_ataque(ataque, game)
        game = self.change_turn(game, soy_jugador1)
        self.update_game(game, game["id_partida"])
        return game

    def encriptar_ataque(self, ataque, game):
        key = Fernet.generate_key()
        f = Fernet(key)
        token = f.encrypt(ataque.encode('utf-8'))

        game["cripto"]["token"] = token.hex()
        game["cripto"]["key"] = key.hex()
        return game
    
    def change_turn(self, game, soy_jugador1):
        if soy_jugador1:
            game["datos_juego"]["turno"] = "Jugador 2"
        else:
            game["datos_juego"]["turno"] = "Jugador 1"
        return game

    def get_atack_from_token(self, game):
        if game["cripto"]["key"] != "":
            key = bytes.fromhex(game["cripto"]["key"])
            token = bytes.fromhex(game["cripto"]["token"])
            f = Fernet(key)
            return f.decrypt(token).decode('utf-8')
        else:
            return ""
    
    def delete_game(self, game_id):
        for partida in self.data:
            if partida["id_partida"] == game_id:
                self.data.remove(partida)