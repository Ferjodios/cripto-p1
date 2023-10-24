import tkinter as tk
from tkinter import PhotoImage
from tkinter import messagebox
from json_match_handler import JsonMatchHandler
from json_character_handler import JsonCharacterHandler
import random

class Game:
    def __init__(self, parent, game_data, user):
        self.game_data = game_data
        self.match_handler = JsonMatchHandler('json/games.json')
        self.character_handler = JsonCharacterHandler('json/characters.json')
        self.game_already_done = False
        self.show_window = True
        self.text_box = "Es tu turno"
        self.set_character_attributes(user)
        self.check_turn()
        if self.es_mi_turno:
            self.check_stats(parent)
            self.check_last_attack()
        if self.show_window:
            parent.destroy()
            self.window = tk.Tk()
            self.configure_window()

    def configure_window(self):
        self.window.title("Untitled game uwu")
        self.window.geometry("600x400")
        ataques = self.character_data["ataques"]

        # Crear la caja con texto arriba a la izquierda
        caja_texto = tk.Frame(self.window, bd=2, relief=tk.SUNKEN)
        caja_texto.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Crear un texto amplio en la caja de texto
        texto_amplio = tk.Text(caja_texto, height=5, width=40)
        texto_amplio.insert(tk.END, self.text_box)
        texto_amplio.pack()

        caja1 = tk.Frame(self.window, bd=2, relief=tk.SUNKEN)
        caja1.pack(side=tk.BOTTOM, fill=tk.X, expand=True)

        boton_ataque1 = tk.Button(caja1, text=ataques[0], command=lambda: self.atacar(ataques[0]))
        boton_ataque2 = tk.Button(caja1, text=ataques[1], command=lambda: self.atacar(ataques[1]))
        boton_ataque3 = tk.Button(caja1, text=ataques[2], command=lambda: self.atacar(ataques[2]))
        boton_ataque4 = tk.Button(caja1, text=ataques[3], command=lambda: self.atacar(ataques[3]))

        boton_ataque1.grid(row=0, column=0)
        boton_ataque2.grid(row=0, column=1)
        boton_ataque3.grid(row=1, column=0)
        boton_ataque4.grid(row=1, column=1)

        boton_salir = tk.Button(caja1, text="Salir", command=lambda: self.window.destroy())
        boton_salir.grid(row=0, column=4)

        #Personaje propio
        imagen_personaje_propio = PhotoImage(file="media/" + self.self_character.lower() + "/" + self.self_character.lower() + "_back.png")
        imagen_personaje_propio = imagen_personaje_propio.subsample(2)
        imagen_personaje_propio_label = tk.Label(self.window, image=imagen_personaje_propio)
        imagen_personaje_propio_label.pack(side=tk.LEFT)

        # Crear un label con la vida del personaje propio encima de la imagen
        vida_label_propio = tk.Label(self.window, text="Vida: " + str(self.self_stats["VIDA"]) + "/100")
        vida_label_propio.pack(side=tk.LEFT)

        #Personaje enemigo
        caja_enemigo = tk.Frame(self.window, bd=2, relief=tk.SUNKEN)
        caja_enemigo.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        imagen_personaje_enemigo = PhotoImage(file="media/" + self.enemy_character.lower() + "/" + self.enemy_character.lower() + "_front.png")
        imagen_personaje_enemigo = imagen_personaje_enemigo.subsample(2)
        imagen_personaje_enemigo_label = tk.Label(caja_enemigo, image=imagen_personaje_enemigo)
        imagen_personaje_enemigo_label.pack()

        vida_enemigo_label = tk.Label(caja_enemigo, text="Vida: " + str(self.enemy_stats["VIDA"]) + "/100")
        vida_enemigo_label.pack()

        self.window.mainloop()
    
    def check_stats(self, parent):
        if self.enemy_stats["VIDA"] == 0:
            messagebox.showinfo("Info", "Ganaste la partida ¡Felicidades!")
            self.end_game(parent)

        if self.enemy_stats["DEFENSA"] >= 100:
            self.enemy_stats["DEFENSA"] -= 200
            self.enemy_stats["RESISTENCIA"] -= 200

    def atacar(self, nombre_ataque):
        if not self.es_mi_turno:
            messagebox.showinfo("Info", "No es tu turno, espera a que la otra persona también juegue")
            self.window.destroy()
        elif self.game_already_done:
            messagebox.showinfo("Info", "Ya acabó el juego, espera a que tu rival vea la victoria para empezar una nueva partida")
            self.window.destroy()
        else:
            self.game_data = self.match_handler.atacar_y_cambiar_turno(self.game_data, nombre_ataque, self.soy_jugador1)
            messagebox.showinfo("Info", "Has atacado, vuelve cuando la otra persona ya haya jugado")
            self.window.destroy()

    def check_last_attack(self):
        ataque = self.match_handler.get_atack_from_token(self.game_data).upper()
        self.game_data["cripto"]["key"] = ""
        self.game_data["cripto"]["token"] = ""
        if ataque != "":
            tipo_ataque = self.enemy_data[ataque]["TIPO"]
            if tipo_ataque == "CURACION":
                if random.randint(0, 100) <= self.enemy_data[ataque]["PRECISION"]:
                    self.enemy_stats["VIDA"] += self.enemy_data[ataque]["DANO"] + self.enemy_stats["ATAQUE"]
                    if self.enemy_stats["VIDA"] >= 100:
                        self.enemy_stats["VIDA"] = 100
                    self.text_box = "Es tu turno, el enemigo se ha curado " + str(self.enemy_data[ataque]["DANO"] + self.enemy_stats["ATAQUE"]) + " puntos de vida"
                else:
                    self.text_box = "Es tu turno, el enemigo falló su ataque"

            elif random.randint(0, 100) <= self.enemy_data[ataque]["PRECISION"] - self.self_stats["EVASION"]:
                if tipo_ataque == "FISICO":
                    daño_teórico = self.enemy_data[ataque]["DANO"] + self.enemy_stats["ATAQUE"]
                    daño = daño_teórico - self.self_stats["DEFENSA"]
                    self.self_stats["VIDA"] -= daño
                    if self.self_stats["VIDA"] <= 0:
                        self.self_stats["VIDA"] = 0
                        self.text_box = "Has perdido, espera a que tu rival vea la victoria para empezar una nueva partida"
                        self.game_already_done = True
                    else:
                        self.text_box = "Es tu turno, te quitaron " + str(daño) + " puntos de vida"

                elif tipo_ataque == "MEJORA ATAQUE":
                    self.enemy_stats["ATAQUE"] += self.enemy_data[ataque]["DANO"]
                    self.text_box = "Es tu turno, el enemigo mejoró su ataque"
                
                elif tipo_ataque == "MEJORA EVASION":
                    self.enemy_stats["EVASION"] += self.enemy_data[ataque]["DANO"]
                    self.text_box = "Es tu turno, el enemigo mejoró su evasión"
                
                elif tipo_ataque == "MEJORA DEFENSA":
                    self.enemy_stats["DEFENSA"] += self.enemy_data[ataque]["DANO"]
                    self.enemy_stats["RESISTENCIA"] += self.enemy_data[ataque]["DANO"]
                    self.text_box = "Es tu turno, el enemigo mejoró sus defensas"
                
                elif tipo_ataque == "MAGICO":
                    daño_teórico = self.enemy_data[ataque]["DANO"] + self.enemy_stats["ATAQUE"]
                    daño = daño_teórico - self.self_stats["RESISTENCIA"]
                    self.self_stats["VIDA"] -= daño
                    if self.self_stats["VIDA"] <= 0:
                        self.self_stats["VIDA"] = 0
                        self.text_box = "Has perdido, espera a que tu rival vea la victoria para empezar una nueva partida"
                        self.game_already_done = True
                    else:
                        self.text_box = "Es tu turno, te quitaron " + str(daño) + " puntos de vida"
                
                elif tipo_ataque == "DEFENSA":
                    self.enemy_stats["DEFENSA"] += 200
                    self.enemy_stats["RESISTENCIA"] += 200
            else: 
                self.text_box = "Es tu turno, el enemigo falló su ataque"
        self.save_info()

    def check_turn(self):
        if self.soy_jugador1:
            self.es_mi_turno = self.game_data["datos_juego"]["turno"] == "Jugador 1"
        else:
            self.es_mi_turno = self.game_data["datos_juego"]["turno"] == "Jugador 2"
        if not self.es_mi_turno:
            messagebox.showinfo("Info", "No es tu turno aún, espera a que la otra persona juegue")
            self.text_box = "No es tu turno"

    
    def set_character_attributes(self, user):
        self.soy_jugador1 = user == self.game_data["id_jugador1"]

        if (self.soy_jugador1):
            self.self_character = self.game_data["datos_juego"]["personaje1"]
            self.self_stats = self.game_data["stats1"]
            self.enemy_character = self.game_data["datos_juego"]["personaje2"]
            self.enemy_stats = self.game_data["stats2"]
        else:
            self.self_character = self.game_data["datos_juego"]["personaje2"]
            self.self_stats = self.game_data["stats2"]
            self.enemy_character = self.game_data["datos_juego"]["personaje1"]
            self.enemy_stats = self.game_data["stats1"]

        self.character_data = self.character_handler.get_character_by_name(self.self_character)
        self.enemy_data = self.character_handler.get_character_by_name(self.enemy_character)

    def end_game(self, parent):
        self.text_box = "Juego terminado, has ganado la partida"
        self.match_handler.delete_game(self.game_data["id_partida"])
        parent.destroy()
        self.show_window = False
    
    def save_info(self):
        if self.soy_jugador1:
            self.game_data["stats1"] = self.self_stats
            self.game_data["stats2"] = self.enemy_stats
        else:
            self.game_data["stats1"] = self.enemy_stats
            self.game_data["stats2"] = self.self_stats
        if self.game_already_done:
            self.match_handler.change_turn(self.game_data, self.soy_jugador1)
            if self.soy_jugador1:
                self.game_data["id_jugador1"] = ""
            else:
                self.game_data["id_jugador2"] = ""
        self.match_handler.update_game(self.game_data, self.game_data["id_partida"])