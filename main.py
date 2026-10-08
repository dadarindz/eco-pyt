# Projet appli météo

import tkinter as tk

from constants import *
from menu import *

# Window et Canvas Tkinter
# Ces variables globales permettent d'éviter que le garbage collector ne les efface
window = None
canvas = None

# ----------------------------------------------------------------------
# Programme principal
# ----------------------------------------------------------------------

def main():
    global window, canvas

    # Fenêtre non redimensionnable, avec un titre
    window = tk.Tk()
    window.title("Météo")
    window.resizable(False, False)

    # Canvas sur lequel on dessine tous les écrans
    canvas = tk.Canvas(window, width = WIDTH, height = HEIGHT)
    canvas.pack()

    load_background(canvas)
    draw_welcome_screen(window, canvas)
    window.mainloop()


if __name__ == "__main__":
    main()
