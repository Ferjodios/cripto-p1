import tkinter as tk

class SignIn:
	def __init__(self, previous_window):
		previous_window.destroy()
		self.user = None
		self.password = None
		self.window = tk.Tk()
		self.input_handler()
		
	def input_handler(self):
		"""Funcion que crea la interfaz y maneja los inputs"""
		self.show_interface()

	def show_interface(self):
		"""Funcion que muestra la interfaz"""
		self.window.title("Sign In")
		self.window.geometry("500x500")
		info = tk.Label(self.window, text="Registro", bg='#49A')
		info.config(font=("Arial", 25))
		info.place(x=200 , y=25)
		self.window.configure(background='#49A')
		# Crear campos para el nombre de usuario y la contraseña
		username_label = tk.Label(self.window, text="Nombre de usuario:")
		username_label.place(x=50, y=100)
		self.username_entry = tk.Entry(self.window)
		self.username_entry.place(x=200, y=100)

		password_label = tk.Label(self.window, text="Contraseña:")
		password_label.place(x=50, y=150)
		self.password_entry = tk.Entry(self.window, show="*")
		self.password_entry.place(x=200, y=150)

		# Crear botón de registro
		register_button = tk.Button(self.window, text="Registrarse", command=self.register)
		register_button.place(x=200, y=200)

		self.window.configure(background='#49A')
		self.window.mainloop()
