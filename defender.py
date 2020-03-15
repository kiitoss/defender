"""Utilisation de tkinter pour l'interface graphique"""
from tkinter import Tk, Canvas
# import threading
import random

def main():
    """Fonction principale"""
    creation_map()
    creation_monster(LIST_OF_MONSTERS)

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
    """Création du premier monstre"""
    if list_of_monsters is None:
        list_of_monsters = []

    Monster()

class Monster():
    """Création d'un nouveau monstre"""
    # pylint: disable=too-many-instance-attributes
    def __init__(self):
        self.width = BLOC_SIZE / 2
        self.height = BLOC_SIZE / 2
        self.pos_x = int(len(MAP) / 2) * BLOC_SIZE + BLOC_SIZE / 2 - self.width / 2
        self.pos_y = 0
        self.grid_x = int(len(MAP) / 2)
        self.grid_y = 0
        self.color = "blue"
        self.body = [
            CANVAS.create_rectangle(
                self.pos_x,
                self.pos_y,
                self.pos_x + self.width / 2,
                self.pos_y + self.height / 2,
                fill=self.color
            ),
            CANVAS.create_rectangle(
                self.pos_x + self.width / 2,
                self.pos_y + self.height / 2,
                self.pos_x + self.width,
                self.pos_y + self.height,
                fill=self.color
            )
        ]
        self.direction = DOWN

        LIST_OF_MONSTERS.append(self)

        self.auto_move()


    def auto_move(self):
        """Analyse les chemins possible et déplace le monstre"""
        # self.timer = threading.Timer(0.05, self.auto_move)
        # self.timer.start()

        middle_y_monster = int(self.pos_y + self.height / 2)
        middle_y_bloc = int(self.grid_y * BLOC_SIZE + BLOC_SIZE / 2)
        middle_x_monster = self.pos_x + self.width / 2
        middle_x_bloc = self.grid_x * BLOC_SIZE + BLOC_SIZE / 2
        direction = self.direction

        if direction == DOWN and middle_y_monster == middle_y_bloc:
            self.analyse_direction()
        elif (direction in (LEFT, RIGHT) and middle_x_monster == middle_x_bloc):
            self.analyse_direction()

        self.pos_x += self.direction[0]
        self.pos_y += self.direction[1]
        for body_part in self.body:
            CANVAS.move(body_part, self.direction[0], self.direction[1])

        if self.pos_x > (self.grid_x + 1) * BLOC_SIZE:
            self.grid_x += 1
        if self.pos_x < self.grid_x * BLOC_SIZE:
            self.grid_x -= 1
        if self.pos_y > (self.grid_y + 1) * BLOC_SIZE:
            self.grid_y += 1

        if LIST_OF_MONSTERS[-1] == self:
            if self.pos_y > self.height and len(LIST_OF_MONSTERS + DEAD_MONSTERS) < WAVE_SIZE:
                creation_monster(LIST_OF_MONSTERS)

        if self.grid_y < len(MAP):
            F.after(20, self.auto_move)

    def analyse_direction(self):
        """Analyse les changements potentiels de direction"""
        available_position = []
        coord_x = self.grid_x
        coord_y = self.grid_y
        direction = self.direction

        if coord_x - 1 >= 0 and MAP[coord_y][coord_x - 1] == 0 and direction != RIGHT:
            available_position.append(LEFT)
        if coord_x + 1 < len(MAP[0]) and MAP[coord_y][coord_x + 1] == 0 and direction != LEFT:
            available_position.append(RIGHT)
        if coord_y + 1 < len(MAP) and MAP[coord_y + 1][coord_x] == 0:
            if coord_y == len(MAP) - 2:
                available_position = [DOWN]
            else:
                available_position.append(DOWN)

        if coord_y < len(MAP) - 1:
            self.direction = available_position[random.randrange(len(available_position))]
        else:
            # self.timer.cancel()
            LIST_OF_MONSTERS.remove(self)
            DEAD_MONSTERS.append(self)

# Paramètres
MAP = [
    [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1]
]
BLOC_SIZE = 50

# Création des variables selon les paramètres originaux
SCREEN_WIDTH = int(len(MAP[0]) * BLOC_SIZE)
SCREEN_HEIGHT = int(len(MAP) * BLOC_SIZE)

# Autres variables
LIST_OF_MONSTERS = []
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
WAVE_SIZE = 10
DEAD_MONSTERS = []



# Création de la fenêtre
F = Tk()
F.geometry(str(SCREEN_WIDTH)+"x"+str(SCREEN_HEIGHT))
CANVAS = Canvas(F, width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
CANVAS.pack()
main()
F.mainloop()
