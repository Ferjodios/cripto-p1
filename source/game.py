import tkinter as tk
from tkinter import messagebox
from json_match_handler import JsonMatchHandler
from json_character_handler import JsonCharacterHandler
from PIL import Image, ImageTk
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
        self.window.title("Titanomachy")
        self.window.geometry("600x480")
        self.window.resizable(False, False)
        self.window.configure(bg='#333333')
        ataques = self.character_data["ataques"]

        #Imagen de fondo
        """bg_image = Image.open(f"media/fondo_dnd.png")
        bg_image_tk = ImageTk.PhotoImage(bg_image)
        bg_label = tk.Label(self.window, image=bg_image_tk)
        bg_label.place(x=0, y=0, relheight=1, relwidth=1)"""

        #Caja con texto de información
        label_texto = tk.Label(self.window, text=self.text_box, width=35, height=4, font=("Arial", 13), wraplength=280, justify="left")
        label_texto.place(x=20, y=20)

        #Caja de abajo con los botones
        caja1 = tk.Frame(self.window, height=105, width=580, bg='#333333', highlightbackground="black", highlightthickness=2)
        caja1.place(x=10, y=370)

        boton_ataque1 = tk.Button(caja1, text=ataques[0], command=lambda: self.atacar(ataques[0]), width=25, height=2)
        boton_ataque2 = tk.Button(caja1, text=ataques[1], command=lambda: self.atacar(ataques[1]), width=25, height=2)
        boton_ataque3 = tk.Button(caja1, text=ataques[2], command=lambda: self.atacar(ataques[2]), width=25, height=2)
        boton_ataque4 = tk.Button(caja1, text=ataques[3], command=lambda: self.atacar(ataques[3]), width=25, height=2)

        boton_ataque1.place(x=5, y=5)
        boton_ataque2.place(x=5, y=55)
        boton_ataque3.place(x=200, y=5)
        boton_ataque4.place(x=200, y=55)

        boton_salir = tk.Button(caja1, text="SALIR", command=lambda: self.window.destroy(), width=15, height=3)
        boton_salir.place(x=420, y=22)

        #Personaje propio
        img_self_champ = Image.open(f"media/" + self.self_character.lower() + "/" + self.self_character.lower() + "_back.png")
        img_self_champ = img_self_champ.resize((120, 200))
        img_self_champ_tk = ImageTk.PhotoImage(img_self_champ)
        img_self_champ_label = tk.Label(self.window, image=img_self_champ_tk, bg='#333333')
        img_self_champ_label.place(x=80, y=160)

        # Label con la vida del personaje propio encima de la imagen
        ps_self_label = tk.Label(self.window, text="PS: " + str(self.self_stats["VIDA"]) + "/100", font=("Arial", 16), bg='#333333', foreground="white")
        ps_self_label.place(x=85, y=125)

        #Personaje enemigo
        img_enemy_champ = Image.open(f"media/" + self.enemy_character.lower() + "/" + self.enemy_character.lower() + "_front.png")
        img_enemy_champ = img_enemy_champ.resize((120, 200))
        img_enemy_champ_tk = ImageTk.PhotoImage(img_enemy_champ)
        img_enemy_champ_label = tk.Label(self.window, image=img_enemy_champ_tk, bg='#333333')
        img_enemy_champ_label.place(x=420, y=50)

        ps_enemy_label = tk.Label(self.window, text="PS: " + str(self.enemy_stats["VIDA"]) + "/100", font=("Arial", 16), bg='#333333', foreground="white")
        ps_enemy_label.place(x=420, y=260)

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
            messagebox.showinfo("Info", "Ya acabó el juego, vuelve a iniciar sesión para jugar de nuevo")
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
                    self.enemy_stats["VIDA"] += self.enemy_data[ataque]["DANO"]
                    if self.enemy_stats["VIDA"] >= 100:
                        self.enemy_stats["VIDA"] = 100
                    self.text_box = "Es tu turno, el enemigo se ha curado " + str(self.enemy_data[ataque]["DANO"] + self.enemy_stats["ATAQUE"]) + " puntos de vida"
                else:
                    self.text_box = "Es tu turno, el enemigo falló su ataque"

            elif random.randint(0, 100) <= self.enemy_data[ataque]["PRECISION"] - self.self_stats["EVASION"]:
                if tipo_ataque == "FISICO":
                    daño_teórico = self.enemy_data[ataque]["DANO"] + self.enemy_stats["ATAQUE"]
                    daño = daño_teórico - self.self_stats["DEFENSA"]
                    if daño < 0:
                        daño = 0
                    self.self_stats["VIDA"] -= daño
                    if self.self_stats["VIDA"] <= 0:
                        self.self_stats["VIDA"] = 0
                        self.text_box = "Has perdido, vuelve a iniciar sesión para jugar de nuevo"
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
                    if daño < 0:
                        daño = 0
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