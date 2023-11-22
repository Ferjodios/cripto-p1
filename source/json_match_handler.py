import json
from cryptography.fernet import Fernet

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import pkcs1_15
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes

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
        # Generar y guardar el hash en security.json
        self.generate_and_save_hash('json/games.json')
            
    def generate_and_save_hash(self, filename):
        """Generar y guardar el hash del archivo en security.json"""
        with open('json/security.json') as security_file:
            security_data = json.load(security_file)

        # Generar hash del archivo
        with open(filename, 'rb') as file:
            file_hash = hashes.Hash(hashes.SHA256(), backend=default_backend())
            file_hash.update(file.read())
            hash_value = file_hash.finalize().hex()

        # Actualizar o agregar la entrada en security.json
        found = False
        for entry in security_data["security"]:
            if entry["file"] == filename:
                entry["hash"] = hash_value
                found = True
                break

        if not found:
            security_data["security"].append({"file": filename, "hash": hash_value})

        # Guardar los cambios en security.json
        with open('json/security.json', 'w') as security_file:
            json.dump(security_data, security_file, indent=4)

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
    
    def atacar_y_cambiar_turno(self, game, ataque, soy_jugador1, player_password):
        game = self.encriptar_ataque(ataque, game, soy_jugador1)
        game = self.change_turn(game, soy_jugador1)
        game = self.sign_attack(game, soy_jugador1, player_password)
        self.update_game(game, game["id_partida"])
        return game
    
    def sign_attack(self, game, soy_jugador1, player_password):
        password_utf = player_password.encode('utf-8')
        #Generar clave privada
        hashed_password = SHA256.new(password_utf).digest()
        passphrase_str = hashed_password.hex()

        #Dependiendo de si soy jugador 1 o 2, saco una clave privada u otra
        if soy_jugador1:
            pk_pem = game["cripto_signature"]["private_jugador1"]
        else:
            pk_pem = game["cripto_signature"]["private_jugador2"]

        #Descifro la clave privada con la contraseña del usuario
        private_key = RSA.import_key(pk_pem, passphrase=passphrase_str)
        
        token = bytes.fromhex(game["cripto"]["token"])
        #Genero la firma con la clave pública
        signature = pkcs1_15.new(private_key).sign(SHA256.new(token))
        game["cripto_signature"]["signature"] = signature.hex()

        return game

    #Encripto el ataque de forma simétrica
    def encriptar_ataque(self, ataque, game, soy_jugador1):
        key = Fernet.generate_key()
        f = Fernet(key)
        token = f.encrypt(ataque.encode('utf-8'))

        game["cripto"]["token"] = token.hex()
        return self.encriptar_key_asimetrico(key, game, soy_jugador1)

    #encripto la key de forma asimétrica
    def encriptar_key_asimetrico(self, key, game, soy_jugador1):
        if soy_jugador1:
            public_key_pem = game["cripto"]["public_jugador2"]
        else:
            public_key_pem = game["cripto"]["public_jugador1"]
        
        public_key = RSA.import_key(public_key_pem)
        encryptor = PKCS1_OAEP.new(public_key)
        encrypted_key = encryptor.encrypt(key)
        game["cripto"]["key"] = encrypted_key.hex()
        return game

    def change_turn(self, game, soy_jugador1):
        if soy_jugador1:
            game["datos_juego"]["turno"] = "Jugador 2"
        else:
            game["datos_juego"]["turno"] = "Jugador 1"
        return game

    def get_attack_from_token(self, game, key):
        if game["cripto"]["token"] != "":
            #Descifro el ataque que esetaba cifrado de forma simétrica
            token = bytes.fromhex(game["cripto"]["token"])
            f = Fernet(key)
            return f.decrypt(token).decode('utf-8')
        else:
            return ""

    def get_attack_from_token_asimetrico(self, game, player_password, soy_jugador1):
        if game["cripto_signature"]["signature"] != "":
            self.verify_attack(game, soy_jugador1)
        if game["cripto"]["key"] != "":
            password_utf = player_password.encode('utf-8')
            #Generar clave privada
            hashed_password = SHA256.new(password_utf).digest()
            passphrase_str = hashed_password.hex()

            #Dependiendo de si soy jugador 1 o 2, saco una clave privada u otra
            if soy_jugador1:
                pk_pem = game["cripto"]["private_jugador1"]
            else:
                pk_pem = game["cripto"]["private_jugador2"]

            #Descifro la clave privada con la contraseña del usuario
            private_key = RSA.import_key(pk_pem, passphrase=passphrase_str)

            decryptor = PKCS1_OAEP.new(private_key)
            #Desencripto con la privada la key para poder desencriptar el ataque
            token_key = decryptor.decrypt(bytes.fromhex(game["cripto"]["key"]))
            return self.get_attack_from_token(game, token_key)
        else:
            return ""
        
    def verify_attack(self, game, soy_jugador1):
        if soy_jugador1:
            public_key_pem = game["cripto"]["public_jugador2"]
        else:
            public_key_pem = game["cripto"]["public_jugador1"]
        try:
            public_key = RSA.import_key(public_key_pem)
            token = bytes.fromhex(game["cripto"]["token"])
            signature = bytes.fromhex(game["cripto_signature"]["signature"])
            pkcs1_15.new(public_key).verify(SHA256.new(token), signature)
            print("La firma coincide con el token.")
            return True
        except Exception as e:
            #print(f"La firma no coincide con el token: {e}")
            return False

    def delete_game(self, game_id):
        for partida in self.data:
            if partida["id_partida"] == game_id:
                self.data.remove(partida)
        self.save()