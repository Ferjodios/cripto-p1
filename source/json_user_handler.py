import json
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class JsonUserHandler:
	def __init__(self):
		self.data = {}

	def load_data(self):
		"""Funcion que carga los datos del json"""
		with open('json/users.json') as json_file:
			self.data = json.load(json_file)
	
	def save(self):
		# Guardar los datos en el archivo JSON
		with open('json/users.json', 'w') as json_file:
			json.dump(self.data, json_file, indent=4)
		# Generar y guardar el hash en security.json
		self.generate_and_save_hash('json/users.json')
	
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

	def check_hashes(self):
		"""Verifica y actualiza los hashes en security.json si hay cambios en los archivos"""
		with open('json/security.json') as security_file:
			security_data = json.load(security_file)

		for entry in security_data["security"]:
			filename = entry["file"]
			stored_hash = entry["hash"]

			try:
				with open(filename, 'rb') as file:
					file_hash = hashes.Hash(hashes.SHA256(), backend=default_backend())
					file_hash.update(file.read())
					current_hash = file_hash.finalize().hex()

				if current_hash != stored_hash:
				# Si el hash actual es diferente al almacenado, actualiza el hash
					entry["hash"] = current_hash
					print(f"Se ha detectado un cambio en {filename}.")
			except (FileNotFoundError, json.decoder.JSONDecodeError):
				print(f"Error al verificar {filename}. Puede que el archivo no exista o no sea un JSON válido.")


	def hash_password(self, password, salt):
		"""Funcion que aplica una funcion hash a la contraseña"""
		password = password.encode()
		kdf = PBKDF2HMAC(
			algorithm=hashes.SHA256(),
			length=32,
			salt=salt,
			iterations=100000,
		)
		pswd_hashed = kdf.derive(password)
		return pswd_hashed.hex()
	
	def save_data(self, user, password):
		"""Funcion que guarda los datos en el json"""
		# Agregar el nuevo usuario a la lista de usuarios
		self.load_data()
		#hash password and save
		salt = os.urandom(16)
		password = self.hash_password(password, salt)
		salt_hex = salt.hex()
		new_user = {"user": user, "password": password, "salt": salt_hex, "character": None}
		self.data.setdefault("Client Register", []).append(new_user)
		self.save()


	def save_character(self, my_user, my_character):
		"""Funcion que guarda el personaje en el json"""
		self.load_data()
		for user in self.data["Client Register"]:
			if user["user"] == my_user:
				user["character"] = my_character
				self.save()
				return True
		return False
	
	def user_exists(self, username):
		"""Funcion que comprueba si el usuario existe"""
		#deberia hacer un try catch?
		self.load_data()
		if "Client Register" in self.data:
			for user in self.data["Client Register"]:
				if user["user"] == username:
					return True
		return False
	
	def find_user(self, my_user):
		"""Funcion que encuentra el usuario"""
		self.load_data()
		if "Client Register" in self.data:
			for user in self.data["Client Register"]:
				if user["user"] == my_user:
					return True
		return False
	
	def get_password_from_user(self, my_user):
		"""Funcion que devuelve la contraseña del usuario"""
		self.load_data()
		if "Client Register" in self.data:
			for user in self.data["Client Register"]:
				if user["user"] == my_user:
					return user["password"]
		return False
	
	def get_salt_from_user(self, my_user):
		"""Funcion que devuelve la salt del usuario"""
		self.load_data()
		if "Client Register" in self.data:
			for user in self.data["Client Register"]:
				if user["user"] == my_user:
					return bytes.fromhex(user["salt"])
		return False
	
	def get_character_from_user(self, my_user):
		"""Funcion que devuelve el personaje del usuario"""
		self.load_data()
		if "Client Register" in self.data:
			for user in self.data["Client Register"]:
				if user["user"] == my_user:
					return user["character"]
		return False