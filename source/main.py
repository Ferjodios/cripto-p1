import tkinter as tk

def main():
    root = tk.Tk()
    root.title("EL gei de David")
    label = tk.Label(root, text="¡Hola, Tkinter!")
    label.pack()
    root.geometry("500x500")
    def mostrar_mensaje():
        label.config(text="¡Hola desde el botón!")

    button = tk.Button(root, text="Haz clic", command=mostrar_mensaje)
    button.pack()
    root.mainloop()
    
main()

