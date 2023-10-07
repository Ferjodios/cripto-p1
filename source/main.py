import tkinter as tk
from main_window import MainWindow
from login import Login
from signin import SignIn

def main():
    '''
    main_window = tk.Tk()
    main_window.title("Untitled game uwu")
    LabelTitle = tk.Label(main_window, text="Untitled game uwu")
    LabelTitle.pack()
    main_window.geometry("500x500")

    SignInButton = tk.Button(main_window, text="Resgistrarse", command=lambda: SignIn(main_window))
    SignInButton.pack()

    LogInButton = tk.Button(main_window, text="Iniciar sesión", command=lambda: LogIn(main_window))
    LogInButton.pack()

    main_window.mainloop()'''

    root = tk.Tk()
    root.title("Untitled game uwu")
    root.geometry("500x500")

    def abrir_ventana_login():
        main_window.destroy()
        login_window = Login(root, volver_a_main)

    def volver_a_main():
        login_window.destroy()
        main_window.show()

    main_window = MainWindow(root, abrir_ventana_login)
    root.mainloop()
    
main()

