import tkinter as tk
from login import LogIn
from signin import SignIn

def main():
	"""Funcion main del programa"""
	root = tk.Tk()
	root.title("Titanomachy")
	root.geometry("500x500")
	root.resizable(False, False)
	root.configure(bg='#333333')

	# Creamos un frame y lo metemos los widgets en el frame
	frame = tk.Frame(bg='#333333')

	# Creamos los widgets
	title_label = tk.Label(frame, text="TITANOMACHY", bg='#333333', fg="#FF3399", font=("Arial", 30))
	signin_button = tk.Button(frame, text="Registrarse", bg="#FF3399", fg="#FFFFFF", font=("Arial", 16), command=lambda: SignIn(root))
	login_button = tk.Button(frame, text="Iniciar Sesion", bg="#FF3399", fg="#FFFFFF", font=("Arial", 16), command=lambda: LogIn(root))

	# Colocamos los widgets en el frame
	title_label.grid(row=0, column=0, columnspan=2, sticky="news", pady=80)
	signin_button.grid(row=5, column=0, pady=90)
	login_button.grid(row=5, column=1, pady=90)
	frame.pack()
	root.mainloop()

if __name__ == "__main__":
    main()
