import json
from tkinter import messagebox

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
	
	def save_data(self, user, password):
		"""Funcion que guarda los datos en el json"""
		# Agregar el nuevo usuario a la lista de usuarios
		self.load_data()
		new_user = {"user": user, "password": password, "character": None}
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