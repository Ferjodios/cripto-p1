import tkinter as tk

class LogIn(tk.Toplevel): #te he cambiado el nombre de la clase pa q las clases esten en camelcase
    def __init__(self, parent):
        parent.destroy()
        self.title("Login")
        
        # Widgets
        tk.Label(self, text="Username:").grid(row=0, column=0)
        self.username_entry = tk.Entry(self)
        self.username_entry.grid(row=0, column=1)
        
        tk.Label(self, text="Password:").grid(row=1, column=0)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.grid(row=1, column=1)
        
        tk.Button(self, text="Login", command=self.login).grid(row=2, column=0, columnspan=2)
        
    def login(self):
        # TODO: Add logic to validate credentials
        self.destroy()