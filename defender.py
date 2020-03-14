"""Utilisation de tkinter pour l'interface graphique"""
from tkinter import Tk, Canvas
import threading
# import random

def main():
    """Fonction principale"""
    creation_map()
    creation_monster(LIST_OF_MONSTERS)
    print(LIST_OF_MONSTERS)

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

def creation_monster(list_of_monsters):
    """Création d'un nouveau monstre"""
    if list_of_monsters is None:
        list_of_monsters = []

    new_monster = Monster()
    list_of_monsters.append(new_monster)

class Monster():
    """Création d'un nouveau monstre"""
    def __init__(self):
        self.pos_x = int(len(MAP) / 2) * BLOC_SIZE
        self.pos_y = 0
        self.color = "blue"
        self.body = [
            CANVAS.create_rectangle(
                self.pos_x,
                self.pos_y,
                self.pos_x + BLOC_SIZE/2,
                self.pos_y + BLOC_SIZE/2,
                fill=self.color
            ),
            CANVAS.create_rectangle(
                self.pos_x + BLOC_SIZE/2,
                self.pos_y + BLOC_SIZE / 2,
                self.pos_x + BLOC_SIZE,
                self.pos_y + BLOC_SIZE,
                fill=self.color
            )
        ]
        self.direction = DOWN
        self.auto_move()

    def move(self, delta_x, delta_y):
        """Déplace le monstre"""
        self.pos_x += delta_x
        self.pos_y += delta_y
        for body_part in self.body:
            print(body_part)
            CANVAS.move(body_part, self.pos_x, self.pos_y)

    def auto_move(self):
        """Analyse les chemins possible et déplace le monstre"""
        threading.Timer(1.0, self.auto_move).start()
        print(self.direction[0])


# Paramètres
MAP = [
    [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1]
]
BLOC_SIZE = 50

# Création des variables selon les paramètres originaux
SCREEN_WIDTH = int(len(MAP[0]) * BLOC_SIZE)
SCREEN_HEIGHT = int(len(MAP) * BLOC_SIZE)

# Autres variables
LIST_OF_MONSTERS = []
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (0, 1)

# Création de la fenêtre
F = Tk()
F.geometry(str(SCREEN_WIDTH)+"x"+str(SCREEN_HEIGHT))
CANVAS = Canvas(F, width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
CANVAS.pack()
main()
F.mainloop()
