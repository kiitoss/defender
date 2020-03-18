"""Utilisation de tkinter pour l'interface graphique"""
from tkinter import Tk, Canvas, Button, Label
import random
import sys
import bodies

def main():
    """Fonction principale"""
    creation_map()

def click_event(event):
    """Détection du clique de la souris sur le canvas de jeu"""
    clean_canvas_option()
    pos_grid_x = int(event.x / BLOC_SIZE)
    pos_grid_y = int(event.y / BLOC_SIZE)
    value_cell = MAP[pos_grid_y][pos_grid_x]
    if  value_cell in ("x", 0, 1):
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
    elif code_cell == 0:
        btn_defender_first = Button(
            CAN_OPTIONS,
            text="DEF 1",
            command=lambda: creation_defender(0, pos_x, pos_y))
        btn_defender_first.config(width=7, height=4)
        btn_defender_first.place(x=0, y=0)

        btn_defender_second = Button(
            CAN_OPTIONS,
            text="DEF 2",
            command=lambda: creation_defender(1, pos_x, pos_y))
        btn_defender_second.config(width=7, height=4)
        btn_defender_second.place(x=0, y=BLOC_SIZE)
    elif code_cell > 0:
        my_defender = None
        for defender in LIST_OF_DEFENDERS:
            if defender.grid_x == pos_x and defender.grid_y == pos_y:
                my_defender = defender
                break

        upgrades = DEFENDERS[my_defender.code].get("upgrades")
        if len(upgrades) >= my_defender.lvl:
            my_upgrades = upgrades[my_defender.lvl - 1]
            btn_upgrade = Button(
                CAN_OPTIONS,
                text="UPGRADE \n price: \n"+str(my_upgrades.get("price")),
                command=lambda: upgrade_defender(my_defender, my_upgrades))
        else:
            btn_upgrade = Label(CAN_OPTIONS, text="LVL MAX")
        btn_upgrade.config(width=7, height=4)
        btn_upgrade.place(x=0, y=0)

def upgrade_defender(defender, upgrades):
    """Amélioration des défenseurs"""
    if PLAYER.get("GOLD") >= upgrades.get("price"):
        PLAYER["GOLD"] -= upgrades.get("price")
        defender.range += upgrades.get("upgrade_range")
        defender.damages += upgrades.get("upgrade_damages")
        defender.lvl += 1
    else:
        print("Pas assez de gold")
    clean_canvas_option()

def remove_obstacle(grid_x, grid_y):
    """Suppression de l'obstacle, conversion en case classique"""
    if PLAYER.get("GOLD") >= PRICE_REMOVE_OBSTACLE:
        PLAYER["GOLD"] -= PRICE_REMOVE_OBSTACLE
        MAP[grid_y][grid_x] = 1
        creation_bloc(grid_x, grid_y)
        clean_canvas_option()
        upgrade_stats()

def creation_defender(code, grid_x, grid_y):
    """Création d'un défenseur contre les ennemis"""
    price = DEFENDERS[code].get("price")
    if PLAYER.get("GOLD") >= price:
        PLAYER["GOLD"] -= price
        MAP[grid_y][grid_x] = 1
        creation_bloc(grid_x, grid_y)
        clean_canvas_option()
        Defender(code, grid_x, grid_y)
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
    if value == -1:
        color = "white"
    elif value == 0:
        color = "green"
    elif value == 1:
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

def creation_wave(code, click=None):
    """Création de la vague d'ennemies"""
    if click is not None:
        PLAYER["WAVE_RUNNING"] += 1
        B_START_WAVE.config(text="Vague suivante")
    if len(LIST_OF_MONSTERS) + len(DEAD_MONSTERS) < WAVE_SIZE * PLAYER.get("WAVE_RUNNING"):
        Monster(code)
        F.after(MONSTERS[code].get("wait"), lambda: creation_wave(code))

def run_wave():
    """Lance la création de la vague d'ennemis lors du clique"""
    type_wave = random.randrange(len(MONSTERS))
    creation_wave(type_wave, 1)

class Monster():
    """Création d'un nouveau monstre"""
    # pylint: disable=too-many-instance-attributes
    def __init__(self, code):
        monster = MONSTERS[code]
        self.width = monster.get("width")
        self.height = monster.get("height")
        self.pos_x = int(len(MAP) / 2) * BLOC_SIZE + BLOC_SIZE / 2 - self.width / 2
        self.pos_y = 0
        self.grid_x = int(len(MAP) / 2)
        self.grid_y = 0
        self.color = monster.get("color")
        self.max_life = monster.get("life")
        self.life = self.max_life
        self.body = bodies.body_creation_monster(code, CANVAS, self)
        self.gold = monster.get("gold")
        self.score = monster.get("score")
        self.direction = DOWN

        LIST_OF_MONSTERS.append(self)
        wave_run = str(len(LIST_OF_MONSTERS)+len(DEAD_MONSTERS))
        wave_max = str(WAVE_SIZE * PLAYER.get("WAVE_RUNNING"))
        L_WAVE_RUN.config(text="Avancée de la vague: "+wave_run+"/"+wave_max)

        self.auto_move()


    def auto_move(self):
        """Analyse les chemins possible et déplace le monstre"""
        middle_y_monster = int(self.pos_y + self.height / 2) - 1
        middle_y_bloc = int(self.grid_y * BLOC_SIZE + BLOC_SIZE / 2)
        middle_x_monster = self.pos_x + self.width / 2 - 1
        middle_x_bloc = self.grid_x * BLOC_SIZE + BLOC_SIZE / 2
        direction = self.direction

        if direction == DOWN and int(middle_y_monster) == int(middle_y_bloc):
            self.analyse_direction()
        elif direction in (LEFT, RIGHT) and int(middle_x_monster) == int(middle_x_bloc):
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

        monster_appeared = len(LIST_OF_MONSTERS) + len(DEAD_MONSTERS)
        full_wave_size = PLAYER.get("WAVE_RUNNING") * WAVE_SIZE
        if len(LIST_OF_MONSTERS) == 0 and monster_appeared == full_wave_size:
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

        if coord_x - 1 >= 0 and MAP[coord_y][coord_x - 1] == -1 and direction != RIGHT:
            available_position.append(LEFT)
        if coord_x + 1 < len(MAP[0]) and MAP[coord_y][coord_x + 1] == -1 and direction != LEFT:
            available_position.append(RIGHT)
        if coord_y + 1 < len(MAP) and MAP[coord_y + 1][coord_x] == -1:
            if coord_y == len(MAP) - 2:
                available_position = [DOWN]
            else:
                available_position.append(DOWN)
        if coord_y < len(MAP) - 1:
            self.direction = available_position[random.randrange(len(available_position))]

class Defender():
    """Création d'un nouveau défenseur"""
    # pylint: disable=too-many-instance-attributes
    def __init__(self, code, grid_x, grid_y):
        defender = DEFENDERS[code]
        self.code = code
        self.width = defender.get("width")
        self.height = defender.get("height")
        self.range = defender.get("range")
        self.price = defender.get("price")
        self.color = defender.get("color")
        self.damages = defender.get("damages")

        self.lvl = 1
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.center_x = grid_x * BLOC_SIZE + BLOC_SIZE / 2
        self.center_y = grid_y * BLOC_SIZE + BLOC_SIZE / 2
        self.pos_x = self.center_x - self.width / 2
        self.pos_y = self.center_y - self.height / 2
        self.target = None
        self.missile = None
        self.missile_coord = []
        self.monster_killed = 0
        c_x = self.center_x
        c_y = self.center_y
        s_r = self.range
        CANVAS.create_oval(c_x-s_r, c_y-s_r, c_x+s_r, c_y+s_r, outline="green")

        self.body = bodies.body_creation_defender(code, CANVAS, self)

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
        target_is_touched = self.move_missile()

        self.missile = CANVAS.create_rectangle(
            self.missile_coord[0],
            self.missile_coord[1],
            self.missile_coord[0] + 10,
            self.missile_coord[1] + 10,
            fill="blue"
        )

        if target_is_touched:
            if self.target.life - self.damages <= 0:
                self.target.life = 0
            else:
                self.target.life -= self.damages

            CANVAS.delete(self.target.body[0])
            if self.target.life > 0:
                self.target.body[0] = bodies.upgrade_life(CANVAS, self.target)
            if self.target == 0:
                self.monster_killed += 1
            CANVAS.delete(self.missile)
            self.missile = None
            F.after(1000, self.auto_attack)
        else:
            F.after(1, self.attack)

    def move_missile(self):
        """Avance le missile et renvoie True lorsque l'ennemie est touché"""
        if self.missile is None:
            self.missile_coord = [self.center_x, self.center_y]
        else:
            CANVAS.delete(self.missile)
            if self.missile_coord[0] < self.target.pos_x:
                self.missile_coord[0] += 1
            elif self.missile_coord[0] > self.target.pos_x:
                self.missile_coord[0] -= 1

            if self.missile_coord[1] < self.target.pos_y:
                self.missile_coord[1] += 1
            elif self.missile_coord[1] > self.target.pos_y:
                self.missile_coord[1] -= 1

            if (self.missile_coord[0] >= self.target.pos_x) \
                and (self.missile_coord[0] <= self.target.pos_x + self.target.width) \
                and (self.missile_coord[1] >= self.target.pos_y) \
                and (self.missile_coord[1] <= self.target.pos_y + self.target.height):
                return True
        return False

# Paramètres
# -1: chemin pour les enemies
# 0: case vide
# 1-9: défenseurs alliés
# 'x': case objet à démolir avant de pouvoir construire
MAP = [
    [0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1],
    [-1, 0, "x", "x", 0, "x", 0, "x", "x", 0, -1],
    [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1],
    [-1, 0, "x", "x", 0, "x", 0, "x", "x", 0, -1],
    [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0]
]
BLOC_SIZE = 80

PLAYER = {
    "GOLD": 20000,
    "SCORE": 0,
    "LIFE": 1000,
    "MONSTER_KILLED": 0,
    "WAVE_RUNNING": 0
}

LENGTH_OPTIONS = 1
LENGTH_STATS = 5

PRICE_REMOVE_OBSTACLE = 2000

DEFENDERS = [
    # DEFENDER 1
    {
        "width": BLOC_SIZE / 2,
        "height": BLOC_SIZE / 2,
        "damages": 1,
        "range": BLOC_SIZE * 2,
        "price": 100,
        "color": "black",
        "upgrades": [
            {
                "price": 100,
                "upgrade_range": BLOC_SIZE,
                "upgrade_damages": 2
            }
        ]
    },

    # DEFENDER 2
    {
        "width": BLOC_SIZE,
        "height": BLOC_SIZE,
        "damages": 2,
        "range": BLOC_SIZE * 3,
        "price": 200,
        "color": "blue",
        "upgrades": [
            {
                "price": 100,
                "upgrade_range": BLOC_SIZE,
                "upgrade_damages": 2
            }
        ]
    }
]

MONSTERS = [
    # MONSTER 1
    {
        "width": BLOC_SIZE / 3,
        "height": BLOC_SIZE / 3,
        "color": "red",
        "life": 2,
        "gold": 10,
        "score": 5,
        "wait": 800
    },

    # MONSTER 2
    {
        "width": BLOC_SIZE / 2,
        "height": BLOC_SIZE / 2,
        "color": "blue",
        "life": 3,
        "gold": 20,
        "score": 15,
        "wait": 1000
    },

    # MONSTER 3
    {
        "width": BLOC_SIZE,
        "height": BLOC_SIZE,
        "color": "green",
        "life": 5,
        "gold": 40,
        "score": 30,
        "wait": 2000
    }
]

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
B_START_WAVE = Button(CAN_STATS, text="Lancer la vague", command=run_wave)
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
