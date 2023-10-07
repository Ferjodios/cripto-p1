import tkinter as tk

class MainWindow:
    def __init__(self, root, abrir_ventana_login):
        self.root = root
        self.abrir_ventana_login = abrir_ventana_login
        
        self.frame = tk.Frame(root)
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        self.label = tk.Label(self.frame, text="Ventana Principal")
        self.label.pack(pady=20)
        
        self.btn_login = tk.Button(self.frame, text="Login", command=self.abrir_ventana_login)
        self.btn_login.pack(pady=10)
    
    def show(self):
        self.frame.pack()
