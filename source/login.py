import tkinter as tk
from tkinter import messagebox
from json_user_handler import JsonUserHandler
from search_match import SearchMatch
from character_chooser import CharacterChooser

class LogIn:
	
	def __init__(self, parent):
		parent.destroy()
		self.user = None
		self.password = None
		self.register = JsonUserHandler()
		self.window = tk.Tk()
		self.show_interface()
		self.window.mainloop()

	def input_handler(self, username_entry, password_entry):
		"""Funcion que comprueba si el log in se encuentra en el json"""
		self.user = username_entry.get()
		self.password = password_entry.get()
		if self.register.user_exists(self.user):
			salt = self.register.get_salt_from_user(self.user)
			if self.register.get_password_from_user(self.user) == self.register.hash_password(self.password, salt):
				if self.register.get_character_from_user(self.user) == None:
					messagebox.showinfo("Info", "Falta elegir personaje")
					CharacterChooser(self.window, self.user, self.register.get_password_from_user(self.user))
				else:
					messagebox.showinfo("Info", "Usuario logeado correctamente")
					SearchMatch(self.window, self.user, self.register.get_character_from_user(self.user), self.register.get_password_from_user(self.user))
			else:
				messagebox.showerror("Error", "Contraseña incorrecta")
		else:
			messagebox.showerror("Error", "El usuario no existe")

	def show_interface(self):
		"""Funcion que muestra la interfaz"""
		self.window.title("Titanomachy")
		self.window.geometry("500x500")
		self.window.resizable(False, False)
		self.window.configure(bg='#333333')

		# Creamos un frame y lo metemos los widgets en el frame
		frame = tk.Frame(bg='#333333')

		# Creamos los widgets
		login_label = tk.Label(frame, text="Iniciar Sesion", bg='#333333', fg="#FF3399", font=("Arial", 30))
		username_label = tk.Label(frame, text="Username", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
		username_entry = tk.Entry(frame, font=("Arial", 16))
		password_entry = tk.Entry(frame, show="*", font=("Arial", 16))
		password_label = tk.Label(frame, text="Password", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
		login_button = tk.Button(frame, text="Login", bg="#FF3399", fg="#FFFFFF", font=("Arial", 16), command=lambda: self.input_handler(username_entry, password_entry))

		# Colocamos los widgets en el frame
		login_label.grid(row=0, column=0, columnspan=2, sticky="news", pady=40)
		username_label.grid(row=1, column=0)
		username_entry.grid(row=1, column=1, pady=20)
		password_label.grid(row=2, column=0)
		password_entry.grid(row=2, column=1, pady=20)
		login_button.grid(row=3, column=0, columnspan=2, pady=30)
		frame.pack()