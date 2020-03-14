"""Utilisation de tkinter pour l'interface graphique"""
from tkinter import Tk, Canvas

def main():
    """Fonction principale"""
    creation_map()

def creation_map():
    """Créé la carte du jeu selon la constante MAP"""
    for pos_y, line in enumerate(MAP):
        for pos_x, value in enumerate(line):
            if value == 0:
                CANVAS.create_rectangle(
                    pos_x * BLOC_SIZE,
                    pos_y * BLOC_SIZE,
                    (pos_x+1) * BLOC_SIZE,
                    (pos_y+1) * BLOC_SIZE,
                    fill="red"
                )

# Paramètres
MAP = [
    [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0],
    [0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]
BLOC_SIZE = 50

# Création des variables selon les paramètres originaux
SCREEN_WIDTH = int(len(MAP[0]) * BLOC_SIZE)
SCREEN_HEIGHT = int(len(MAP) * BLOC_SIZE)

# Création de la fenêtre
F = Tk()
F.geometry(str(SCREEN_WIDTH)+"x"+str(SCREEN_HEIGHT))
CANVAS = Canvas(F, width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
CANVAS.pack()
main()
F.mainloop()
