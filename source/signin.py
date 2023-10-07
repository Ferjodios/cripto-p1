import tkinter as tk

class SignIn:
    def __init__(self, previous_window):
        signin_window = tk.Toplevel(previous_window)
        signin_window.title("Registro")
        signin_window.geometry("500x500")

        volver_button = tk.Button(signin_window, text="Volver", command=signin_window.destroy)
        volver_button.pack()

        signin_window.mainloop()