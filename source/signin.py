import tkinter as tk
from tkinter import messagebox
import re
from json_user_handler import JsonUserHandler
from character_chooser import CharacterChooser

class SignIn:
	def __init__(self, previous_window):
		previous_window.destroy()
		self.user = None
		self.password = None
		self.register = JsonUserHandler()
		self.window = tk.Tk()
		self.show_interface() 
		self.window.mainloop()
		
	def input_handler(self, username_entry, password_entry):
		"""Funcion que comprueba el formato de Sing in es correcto y lo guarda en un json"""
		self.user = username_entry.get()
		self.password = password_entry.get()
		if self.user_handler() and self.password_handler():	
			self.register.save_data(self.user, self.password)
			messagebox.showinfo("Info", "Usuario registrado correctamente")
			CharacterChooser(self.window, self.user)
			
		
	def show_interface(self):
		"""Funcion que muestra la interfaz"""
		self.window.title("Sign In")
		self.window.geometry("500x500")
		self.window.resizable(False, False)
		self.window.configure(bg='#333333')
		
		# Creamos un frame y lo metemos los widgets en el frame
		frame = tk.Frame(bg='#333333')

		# Creamos los widgets
		login_label = tk.Label(frame, text="Registro", bg='#333333', fg="#FF3399", font=("Arial", 30))
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

	def user_handler(self):
		"""Funcion que comprueba si el usuario cumple el formato o ya exsite"""
		if self.user is None:
			messagebox.showerror("Error", "El usuario no puede estar vacio")
			return False
		elif len(self.user) == 0:
			messagebox.showerror("Error", "El usuario no puede estar vacio")
			return False
		else:
			if self.register.user_exists(self.user):
				messagebox.showerror("Error", "El usuario ya existe")
				return False
			return True

	def password_handler(self):
		"""Funcion que comprueba si la contraseña cumple el formato"""
		if self.password is None:
			messagebox.showerror("Error", "La contraseña no puede estar vacia")
			return False
		elif len(self.password) == 0:
			messagebox.showerror("Error", "La contraseña no puede estar vacia")
			return False
		regex = re.compile(r'^(?=.*[0-9])(?=.*[!@#$%^&])(?=.*[A-Z])[a-zA-Z0-9!@#$%^&]{6,16}$')
		if not regex.fullmatch(str(self.password)):
			messagebox.showerror("Error", "La contraseña debe tener entre 6 y 16 caracteres, al menos una letra mayúscula, un número y un caracter especial")
			return False
		return True
