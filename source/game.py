import tkinter as tk
from tkinter import PhotoImage

class Game:
    def __init__(self, parent, game_data):
        self.game_data = game_data

        parent.destroy()
        self.window = tk.Tk()
        self.configure_window()

    def configure_window(self):
        self.window.title("Untitled game uwu")
        self.window.geometry("600x400")

        # Crear la caja con texto arriba a la izquierda
        caja_texto = tk.Frame(self.window, bd=2, relief=tk.SUNKEN)
        caja_texto.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Crear un texto amplio en la caja de texto
        texto_amplio = tk.Text(caja_texto, height=5, width=40)
        texto_amplio.insert(tk.END, "¡Un Pokémon salvaje apareció!")
        texto_amplio.pack()

        caja1 = tk.Frame(self.window, bd=2, relief=tk.SUNKEN)
        caja1.pack(side=tk.BOTTOM, fill=tk.X, expand=True)

        boton_ataque1 = tk.Button(caja1, text="Ataque 1")
        boton_ataque2 = tk.Button(caja1, text="Ataque 2")
        boton_ataque3 = tk.Button(caja1, text="Ataque 3")
        boton_ataque4 = tk.Button(caja1, text="Ataque 4")

        boton_ataque1.grid(row=0, column=0)
        boton_ataque2.grid(row=0, column=1)
        boton_ataque3.grid(row=1, column=0)
        boton_ataque4.grid(row=1, column=1)

        boton_salir = tk.Button(caja1, text="Salir")
        boton_salir.grid(row=0, column=4)

        #Personaje propio
        imagen_personaje_propio = PhotoImage(file="media/inti/inti_back.png")
        imagen_personaje_propio = imagen_personaje_propio.subsample(2)
        imagen_personaje_propio_label = tk.Label(self.window, image=imagen_personaje_propio)
        imagen_personaje_propio_label.pack(side=tk.LEFT)

        # Crear un label con la vida del personaje propio encima de la imagen
        vida_label_propio = tk.Label(self.window, text="Vida: 100/100")
        vida_label_propio.pack(side=tk.LEFT)

        #Personaje enemigo
        caja_enemigo = tk.Frame(self.window, bd=2, relief=tk.SUNKEN)
        caja_enemigo.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        imagen_personaje_enemigo = PhotoImage(file="media/inti/inti_front.png")
        imagen_personaje_enemigo = imagen_personaje_enemigo.subsample(2)
        imagen_personaje_enemigo_label = tk.Label(caja_enemigo, image=imagen_personaje_enemigo)
        imagen_personaje_enemigo_label.pack()

        vida_enemigo_label = tk.Label(caja_enemigo, text="Vida: 100/100")
        vida_enemigo_label.pack()

        self.window.mainloop()

    