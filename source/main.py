import tkinter as tk
from main_window import MainWindow
from login import LogIn
from signin import SignIn

def main():
    """Funcion main del programa"""
    root = tk.Tk()
    root.title("Untitled game uwu")
    root.geometry("500x500")

    title_label = tk.Label(root, text="Untitled Pokemon-like Game", font=("Helvetica", 20))
    title_label.pack(pady=(80, 40))

    button_font = ("Helvetica", 14)
    signin_button = tk.Button(root, text="Registrarse", font=button_font, command=lambda: SignIn(root))
    signin_button.pack(side="left", padx=(80, 10), pady=5)

    login_button = tk.Button(root, text="Iniciar Sesión", font=button_font, command=lambda: LogIn(root))
    login_button.pack(side="right", padx=(10, 80), pady=5)
    
    """
    signin_button = tk.Button(root, text = "Registrarte", command=lambda: SignIn(root), height = 5, width = 20 , bg="#1FA463")
    signin_button.place(x=75 , y=175)12

    login_button = tk.Button(root, text="Iniciar Sesión", command=lambda: Login(root), height = 5, width = 20, bg="#1FA463")
    login_button.place(x=300, y=175)
    """
    root.mainloop()
    
if __name__ == "__main__":
    main()

