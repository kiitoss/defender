"""Utilisation de tkinter pour l'interface graphique"""
from tkinter import Tk, Canvas, Button, Label
import random
import sys

def main():
    """Fonction principale"""
    creation_map()

def click_event(event):
    """Détection du clique de la souris sur le canvas de jeu"""
    clean_canvas_option()
    pos_grid_x = int(event.x / BLOC_SIZE)
    pos_grid_y = int(event.y / BLOC_SIZE)
    value_cell = MAP[pos_grid_y][pos_grid_x]
    if  value_cell in ("x", 1):
        create_options(pos_grid_x, pos_grid_y, value_cell)

def upgrade_stats():
    """Mise à jour des statistiques du joueur"""
    L_GOLD.config(text="Or: "+str(PLAYER.get("GOLD")))
    L_SCORE.config(text="Score: "+str(PLAYER.get("SCORE")))
    L_LIFE.config(text="Vies: "+str(PLAYER.get("LIFE")))

def clean_canvas_option():
    """Supprime tous les boutons du canvas options"""
    children = CAN_OPTIONS.winfo_children()
    for child in children:
        child.destroy()

def create_options(pos_x, pos_y, code_cell):
    """Affiche les options possibles suite à un clic sur une case du jeu"""
    # La taille du bouton dépend du caractère du bouton, ici un texte (pour l'instant)
    # Donc la taille ne correspond pas à la taille d'un bloc
    if code_cell == "x":
        btn_remove_obstacle = Button(
            CAN_OPTIONS,
            text="del obstacle",
            command=lambda: remove_obstacle(pos_x, pos_y))
        btn_remove_obstacle.config(width=7, height=4)
        btn_remove_obstacle.place(x=0, y=0)
    elif code_cell == 1:
        btn_defender = Button(
            CAN_OPTIONS,
            text="DEF 1",
            command=lambda: creation_defender(0, pos_x, pos_y))
        btn_defender.config(width=7, height=4)
        btn_defender.place(x=0, y=0)


def remove_obstacle(grid_x, grid_y):
    """Suppression de l'obstacle, conversion en case classique"""
    print('Suppression obstacle en position: x=', grid_x, " y=", grid_y)
    MAP[grid_y][grid_x] = 1
    creation_bloc(grid_x, grid_y)
    clean_canvas_option()

def creation_defender(code, grid_x, grid_y):
    """Création d'un défenseur contre les ennemis"""
    if PLAYER.get("GOLD") >= PRICE_DEFENDERS[code]:
        PLAYER["GOLD"] -= PRICE_DEFENDERS[code]
        MAP[grid_y][grid_x] = 2
        creation_bloc(grid_x, grid_y)
        clean_canvas_option()
        Defender(grid_x, grid_y)
        upgrade_stats()

def creation_map():
    """Création de la carte du jeu selon la constante MAP"""
    for pos_y, line in enumerate(MAP):
        for pos_x in range(len(line)):
            creation_bloc(pos_x, pos_y)

def creation_bloc(grid_x, grid_y):
    """Création de chaque bloc constituant la carte"""
    value = MAP[grid_y][grid_x]
    color = "white"
    if value == 0:
        color = "white"
    elif value == 1:
        color = "green"
    elif value == 2:
        color = "red"
    elif value == "x":
        color = "black"

    CANVAS.create_rectangle(
        grid_x * BLOC_SIZE,
        grid_y * BLOC_SIZE,
        (grid_x+1) * BLOC_SIZE,
        (grid_y+1) * BLOC_SIZE,
        fill=color
    )

def creation_wave(code=None):
    """Création de la vague d'ennemies"""
    if code is not None:
        PLAYER["WAVE_RUNNING"] += 1
    if len(LIST_OF_MONSTERS) == 0:
        B_START_WAVE.config(text="Vague suivante")
    if len(LIST_OF_MONSTERS) + len(DEAD_MONSTERS) < WAVE_SIZE * PLAYER.get("WAVE_RUNNING"):
        Monster()
        F.after(1000, creation_wave)

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
                self.pos_x + self.width / 4,
                self.pos_y,
                self.pos_x + 3 * self.width / 4,
                self.pos_y + self.height / 4,
                fill=self.color
            ),
            CANVAS.create_rectangle(
                self.pos_x + self.width/ 8,
                self.pos_y + self.height / 4,
                self.pos_x + 7 * self.width / 8,
                self.pos_y + self.height,
                fill=self.color
            ),
            CANVAS.create_rectangle(
                self.pos_x,
                self.pos_y + 3 * self.height / 8,
                self.pos_x + self.width / 8,
                self.pos_y + self.height,
                fill=self.color
            ),
            CANVAS.create_rectangle(
                self.pos_x + 7 * self.width / 8,
                self.pos_y + 3 * self.height / 8,
                self.pos_x + self.width,
                self.pos_y + self.height,
                fill=self.color
            )
        ]
        self.life = 3
        self.gold = 20
        self.score = 15
        self.direction = DOWN

        LIST_OF_MONSTERS.append(self)
        wave_run = str(len(LIST_OF_MONSTERS)+len(DEAD_MONSTERS))
        wave_max = str(WAVE_SIZE * PLAYER.get("WAVE_RUNNING"))
        L_WAVE_RUN.config(text="Avancée de la vague: "+wave_run+"/"+wave_max)

        self.auto_move()


    def auto_move(self):
        """Analyse les chemins possible et déplace le monstre"""
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

        self.adapt_on_grid()

        if self.grid_y < len(MAP) - 1 and self.life > 0:
            F.after(20, self.auto_move)
        else:
            self.auto_kill()

    def adapt_on_grid(self):
        """Check sur quelles positions de la grille se trouve l'ennemie"""
        if self.pos_x > (self.grid_x + 1) * BLOC_SIZE:
            self.grid_x += 1
        if self.pos_x < self.grid_x * BLOC_SIZE:
            self.grid_x -= 1
        if self.pos_y > (self.grid_y + 1) * BLOC_SIZE:
            self.grid_y += 1

    def auto_kill(self):
        """Auto-détruit l'objet Monster"""
        if self.life <= 0:
            PLAYER["GOLD"] += self.gold
            PLAYER["SCORE"] += self.score
            PLAYER["MONSTER_KILLED"] += 1
            L_MONSTER_KILLED.config(text="Monstres tués: "+str(PLAYER.get("MONSTER_KILLED")))
        else:
            PLAYER["LIFE"] -= 1
            upgrade_stats()
            if PLAYER["LIFE"] == 0:
                print("Défaite")
                sys.exit()

        LIST_OF_MONSTERS.remove(self)
        DEAD_MONSTERS.append(self)
        for body_part in self.body:
            CANVAS.delete(body_part)

        if len(LIST_OF_MONSTERS) == 0:
            DEAD_MONSTERS[:] = []
            PLAYER["WAVE_RUNNING"] = 0
            B_START_WAVE.config(text="Lancer la vague")
            L_WAVE_RUN.config(text="Avancée de la vague: 0/"+str(WAVE_SIZE))
        upgrade_stats()

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

class Defender():
    """Création d'un nouveau défenseur"""
    # pylint: disable=too-many-instance-attributes
    def __init__(self, grid_x, grid_y):
        self.width = BLOC_SIZE / 2
        self.height = BLOC_SIZE / 2
        self.center_x = grid_x * BLOC_SIZE + BLOC_SIZE / 2
        self.center_y = grid_y * BLOC_SIZE + BLOC_SIZE / 2
        self.pos_x = self.center_x - self.width / 2
        self.pos_y = self.center_y - self.height / 2
        self.target = None
        self.missile = None
        self.missile_coord = []
        self.range = BLOC_SIZE * 2
        self.price = PRICE_DEFENDERS[0]
        self.color = "black"
        self.body = [
            CANVAS.create_rectangle(
                self.pos_x + self.width / 4,
                self.pos_y,
                self.pos_x + 3 * self.width / 4,
                self.pos_y + self.height / 4,
                fill=self.color
            ),
            CANVAS.create_rectangle(
                self.pos_x + self.width/ 8,
                self.pos_y + self.height / 4,
                self.pos_x + 7 * self.width / 8,
                self.pos_y + self.height,
                fill=self.color
            ),
            CANVAS.create_rectangle(
                self.pos_x,
                self.pos_y + 3 * self.height / 8,
                self.pos_x + self.width / 8,
                self.pos_y + self.height,
                fill=self.color
            ),
            CANVAS.create_rectangle(
                self.pos_x + 7 * self.width / 8,
                self.pos_y + 3 * self.height / 8,
                self.pos_x + self.width,
                self.pos_y + self.height,
                fill=self.color
            )
        ]
        c_x = self.center_x
        c_y = self.center_y
        s_r = self.range
        CANVAS.create_oval(c_x-s_r, c_y-s_r, c_x+s_r, c_y+s_r, outline="green")

        LIST_OF_DEFENDERS.append(self)
        self.auto_attack()

    def auto_attack(self):
        """Gestion de l'auto-attaque des défenseurs"""
        if self.target is None:
            for monster in LIST_OF_MONSTERS:
                delta_x_left_carre = (monster.pos_x - self.center_x) ** 2
                delta_x_right_carre = (monster.pos_x + monster.width - self.center_x) ** 2
                delta_y_top_carre = (monster.pos_y - self.center_y) ** 2
                delta_y_bot_carre = (monster.pos_y + monster.height - self.center_y) ** 2
                d_top_left = (delta_x_left_carre + delta_y_top_carre) ** 0.5
                d_top_right = (delta_x_right_carre + delta_y_top_carre) ** 0.5
                d_bot_left = (delta_x_left_carre + delta_y_bot_carre) ** 0.5
                d_bot_right = (delta_x_right_carre + delta_y_bot_carre) ** 0.5

                distance = d_top_left
                for element in [d_top_right, d_bot_left, d_bot_right]:
                    if element < distance:
                        distance = element

                if  distance <= self.range:
                    self.target = monster
                    break
            F.after(10, self.auto_attack)
        else:
            delta_x_left_carre = (self.target.pos_x - self.center_x) ** 2
            delta_x_right_carre = (self.target.pos_x + self.target.width - self.center_x) ** 2
            delta_y_top_carre = (self.target.pos_y - self.center_y) ** 2
            delta_y_bot_carre = (self.target.pos_y + self.target.height - self.center_y) ** 2
            d_top_left = (delta_x_left_carre + delta_y_top_carre) ** 0.5
            d_top_right = (delta_x_right_carre + delta_y_top_carre) ** 0.5
            d_bot_left = (delta_x_left_carre + delta_y_bot_carre) ** 0.5
            d_bot_right = (delta_x_right_carre + delta_y_bot_carre) ** 0.5

            distance = d_top_left
            for element in [d_top_right, d_bot_left, d_bot_right]:
                if element < distance:
                    distance = element
            if distance > self.range:
                self.target = None
                F.after(10, self.auto_attack)
            else:
                if self.target.life > 0:
                    self.attack()
                else:
                    self.target = None
                    F.after(10, self.auto_attack)

    def attack(self):
        """Gestion du missile lancé par le défenseur"""
        touch_x = False
        touch_y = False
        if self.missile is None:
            self.missile_coord = [self.center_x, self.center_y]
        else:
            CANVAS.delete(self.missile)
            if self.missile_coord[0] < self.target.pos_x:
                self.missile_coord[0] += 1
            elif self.missile_coord[0] > self.target.pos_x:
                self.missile_coord[0] -= 1
            else:
                touch_x = True

            if self.missile_coord[1] < self.target.pos_y:
                self.missile_coord[1] += 1
            elif self.missile_coord[1] > self.target.pos_y:
                self.missile_coord[1] -= 1
            else:
                touch_y = True

        self.missile = CANVAS.create_rectangle(
            self.missile_coord[0],
            self.missile_coord[1],
            self.missile_coord[0] + 10,
            self.missile_coord[1] + 10,
            fill="blue"
        )

        if touch_x and touch_y:
            self.target.life -= 1
            CANVAS.delete(self.missile)
            self.missile = None
            F.after(1000, self.auto_attack)
        else:
            F.after(1, self.attack)

# Paramètres
# 0: chemin pour les enemies
# 1: case vide
# 2-9: défenseurs alliés
# 'x': case objet à démolir avant de pouvoir construire
MAP = [
    [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, "x", "x", 1, "x", 1, "x", "x", 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, "x", "x", 1, "x", 1, "x", "x", 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1]
]
BLOC_SIZE = 80

PLAYER = {
    "GOLD": 200,
    "SCORE": 0,
    "LIFE": 1,
    "MONSTER_KILLED": 0,
    "WAVE_RUNNING": 0
}
PRICE_DEFENDERS = [100]
LENGTH_OPTIONS = 1
LENGTH_STATS = 5

# Création des variables selon les paramètres originaux
STATS_WIDTH = LENGTH_STATS * BLOC_SIZE
OPTIONS_WIDTH = LENGTH_OPTIONS * BLOC_SIZE
SCREEN_WIDTH = int((len(MAP[0]) + LENGTH_OPTIONS + LENGTH_STATS) * BLOC_SIZE)
SCREEN_HEIGHT = int(len(MAP) * BLOC_SIZE)

# Autres variables
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
LIST_OF_MONSTERS = []
WAVE_SIZE = 20
DEAD_MONSTERS = []
LIST_OF_DEFENDERS = []

# Création de la fenêtre et des canvas
F = Tk()
F.geometry(str(SCREEN_WIDTH)+"x"+str(SCREEN_HEIGHT))

CANVAS = Canvas(F, width=SCREEN_WIDTH-STATS_WIDTH-OPTIONS_WIDTH, height=SCREEN_HEIGHT)
CANVAS.bind("<Button-1>", click_event)
CANVAS.place(x=0, y=0)

CAN_OPTIONS = Canvas(F, width=OPTIONS_WIDTH, height=SCREEN_HEIGHT, bg="black")
CAN_OPTIONS.place(x=SCREEN_WIDTH-STATS_WIDTH-OPTIONS_WIDTH, y=0)

CAN_STATS = Canvas(F, width=STATS_WIDTH, height=SCREEN_HEIGHT, bg="black")
CAN_STATS.place(x=SCREEN_WIDTH-STATS_WIDTH, y=0)
B_START_WAVE = Button(CAN_STATS, text="Lancer la vague", command=lambda: creation_wave(1))
B_START_WAVE.place(x=15, y=15)
L_WAVE_RUN = Label(CAN_STATS, text="Avancée de la vague: 0/"+str(WAVE_SIZE), bg="black", fg="white")
L_WAVE_RUN.place(x=15, y=45)
L_SCORE = Label(CAN_STATS, text="Score: "+str(PLAYER.get("SCORE")), bg="black", fg="white")
L_SCORE.place(x=15, y=75)
L_GOLD = Label(CAN_STATS, text="Or: "+str(PLAYER.get("GOLD")), bg="black", fg="white")
L_GOLD.place(x=15, y=105)
L_MONSTER_KILLED = Label(CAN_STATS, text="Monstres Tués: 0", bg="black", fg="white")
L_MONSTER_KILLED.place(x=15, y=135)
L_LIFE = Label(CAN_STATS, text="Vies: "+str(PLAYER.get("LIFE")), bg="black", fg="white")
L_LIFE.place(x=15, y=165)

main()
F.mainloop()
