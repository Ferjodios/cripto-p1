import json
import tkinter as tk
from tkinter import messagebox
from json_user_handler import JsonUserHandler
from PIL import Image, ImageTk
from search_match import SearchMatch

class CharacterChooser:
	def __init__(self, previous_window, user):
		previous_window.destroy()
		self.user = user
		self.window = tk.Tk()
		self.imagenes = []
		self.selected_character = None
		self.register = JsonUserHandler()
		self.show_interface()
		self.window.mainloop()



	def seleccionar_personaje(self, imagen, personajes, ataques_entries, nombre_entry):
		# Actualiza los campos de texto con la información del personaje seleccionado
		info = personajes[imagen]
		nombre_entry.delete(0, tk.END)
		nombre_entry.insert(0, info["nombre"])
		for i, ataque_entry in enumerate(ataques_entries):
			ataque_entry.delete(0, tk.END)
			if i < len(info["ataques"]):
				ataque_entry.insert(0, info["ataques"][i])
		self.selected_character = info["nombre"]
	
	def load_character(self):
		"""Funcion que carga el personaje en el json"""
		if self.register.save_character(self.user, self.selected_character):
			messagebox.showinfo("Info", "Personaje guardado correctamente")
			self.window.destroy()
		else:
			messagebox.showerror("Error", "El usuario no existe")

	def load_character_and_play(self):
		"""Funcion que carga el personaje en el json"""
		if self.register.save_character(self.user, self.selected_character):
			messagebox.showinfo("Info", "Personaje guardado correctamente")
			SearchMatch(self.window, self.user, self.selected_character)
		else:
			messagebox.showerror("Error", "El usuario no existe")

	def show_interface(self):
		self.window.title("Character Chooser")
		self.window.geometry("780x600")
		self.window.configure(bg='#333333')

		with open("json/characters.json") as f:
			personajes = json.load(f)
		
		# Crea el título 
		titulo = tk.Label(self.window, text="Elige un personaje", bg='#333333', fg="#FF3399", font=("Arial", 30))
		titulo.place(x=220, y=20)

		
		nombre_label = tk.Label(self.window, text="Nombre del personaje: ",  bg='#333333', fg="#FF3399", font=("Arial", 16))
		nombre_label.place(x=20, y=120)
		nombre_entry = tk.Entry(self.window, bg='#333333', fg="white", font=("Arial", 16))
		nombre_entry.place(x=20, y=160)

		# Carga las imágenes y crea los botones de imagen
		for i, imagen in enumerate(personajes.keys()):
			img = Image.open(f"media/{imagen}")
			img = img.resize((120, 200))
			img_tk = ImageTk.PhotoImage(img)
			self.imagenes.append(img_tk)
			boton = tk.Button(self.window, image=img_tk, bg='#333333', command=lambda imagen=imagen: self.seleccionar_personaje(imagen, personajes, ataques_entries, nombre_entry))
			boton.place(x=20 + i*150, y=200)

		ataques_label = tk.Label(self.window, text="Ataques del personaje: ",  bg='#333333', fg="#FF3399", font=("Arial", 16))
		ataques_label.place(x=60, y=440)

		ataques_entries = [tk.Entry(self.window, bg='#333333', fg="white", font=("Arial", 16)) for _ in range(4)]
		for i, ataque_entry in enumerate(ataques_entries):
			if i % 2 == 0:
				ataque_entry.place(x=60, y=480 + i*20)
			else:
				ataque_entry.place(x=440, y=480 + (i-1)*20)

		continuar_button = tk.Button(self.window, text="Finalizar", bg="#FF3399", fg="#FFFFFF", font=("Arial", 20), command=self.load_character)
		continuar_button.place(x=340, y=140)
		continuar_y_jugar_button = tk.Button(self.window, text="Buscar Partida", bg="#FF3399", fg="#FFFFFF", font=("Arial", 20), command=self.load_character_and_play)
		continuar_y_jugar_button.place(x=540, y=140)

		# mandamos alerta sobre que hacer
		messagebox.showinfo("Info", "Elige un personaje, para ello clicka sobre la imagen del personaje que quieras elegir")