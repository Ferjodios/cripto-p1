import tkinter as tk
from main_window import MainWindow
from login import Login
from signin import SignIn

def main():
    """Funcion main del programa"""
    root = tk.Tk()
    root.title("Untitled game uwu")
    root.geometry("500x500")
    signin_button = tk.Button(root, text = "Registrarte", command=lambda: SignIn(root), height = 5, width = 20 , bg="#1FA463")
    signin_button.place(x=75 , y=175)

    login_button = tk.Button(root, text="Iniciar Sesión", command=lambda: Login(root), height = 5, width = 20, bg="#1FA463")
    login_button.place(x=300, y=175)
    root.mainloop()
    """def abrir_ventana_login():
        main_window.destroy()
        login_window = Login(root, volver_a_main)

    def volver_a_main():
        login_window.destroy()
        main_window.show()

    main_window = MainWindow(root, abrir_ventana_login)
    root.mainloop()"""
    
if __name__ == "__main__":
    main()

