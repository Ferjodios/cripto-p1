import tkinter as tk

class Login:

    def __init__(self, root, volver_a_main):
        self.root = root
        self.volver_a_main = volver_a_main
        
        self.frame = tk.Frame(root)
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        self.label = tk.Label(self.frame, text="Ventana de Login")
        self.label.pack(pady=20)
        
        self.btn_volver = tk.Button(self.frame, text="Volver a Main", command=self.volver_a_main)
        self.btn_volver.pack(pady=10)

    def prueba():
        pass