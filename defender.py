"""Utilisation de tkinter pour l'interface graphique"""
from tkinter import Tk, Canvas, Button, Label, PhotoImage
import random
import sys
import design

def main():
    """Fonction principale"""
    creation_map()

def click_event(event):
    """Détection du clique de la souris sur le canvas de jeu"""
    clean_canvas_option()
    pos_grid_x = int(event.x / BLOC_SIZE)
    pos_grid_y = int(event.y / BLOC_SIZE)
    value_cell = MAP[pos_grid_y][pos_grid_x]
    if  value_cell in ("x", -1, 0, 1):
        clean_canvas_stat_defender()
    if value_cell != -1:
        create_options(pos_grid_x, pos_grid_y, value_cell)

def upgrade_stats():
    """Mise à jour des statistiques du joueur"""
    L_GOLD.config(text="Or: "+str(PLAYER.get("GOLD")))
    L_SCORE.config(text="Score: "+str(PLAYER.get("SCORE")))
    L_LIFE.config(text="Vies: "+str(PLAYER.get("LIFE")))

def show_stats_defender(defender):
    """Affiche les statistiques relative au défenseur targetté"""
    L_DAMAGE.config(text="Attaque: "+str(defender.damages))
    L_RANGE.config(text="Range: "+str(defender.range))
    L_SPEED.config(text="Fréquence de tir: "+str(defender.attack_speed))
    L_KILLED.config(text="Monstres tués: "+str(defender.monster_killed))

    SCREEN_ITEMS["DEFENDER_PRINT"] = defender
    if SCREEN_ITEMS["STAT_DEFENDER_VISIBLE"] is False:
        SCREEN_ITEMS["RANGE_MONSTER"] = CANVAS.create_oval(
            defender.center_x-defender.range,
            defender.center_y-defender.range,
            defender.center_x+defender.range,
            defender.center_y+defender.range,
            width=3,
            outline="green",
            fill="green",
            stipple="gray25",
        )

        for body_part in SCREEN_ITEMS.get("DEFENDER_PRINT").body:
            CANVAS.tag_raise(body_part)
    SCREEN_ITEMS["STAT_DEFENDER_VISIBLE"] = True

def clean_canvas_option():
    """Supprime tous les boutons du canvas options"""
    children = CAN_OPTIONS.winfo_children()
    for child in children:
        child.destroy()

def clean_canvas_stat_defender():
    """Efface le canvas affichant les statistiques du défenseur targetté"""
    L_DAMAGE.config(text="")
    L_RANGE.config(text="")
    L_SPEED.config(text="")
    L_KILLED.config(text="")
    SCREEN_ITEMS["STAT_DEFENDER_VISIBLE"] = False
    CANVAS.delete(SCREEN_ITEMS.get("RANGE_MONSTER"))
    SCREEN_ITEMS["RANGE_MONSTER"] = None
    SCREEN_ITEMS["DEFENDER_PRINT"] = None

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
        for i in range(len(DEFENDERS)):
            Button(
                CAN_OPTIONS,
                text="DEF "+str(i+1),
                command=lambda code=i: creation_defender(code, pos_x, pos_y),
                width=7,
                height=4
            ).place(x=0, y=i * BLOC_SIZE)
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

        clean_canvas_stat_defender()
        show_stats_defender(my_defender)

def upgrade_defender(defender, upgrades):
    """Amélioration des défenseurs"""
    if PLAYER.get("GOLD") >= upgrades.get("price") \
        and defender.monster_killed >= upgrades.get("min_dead"):
        if upgrades.get("upgrade_ability") != 0:
            defender_transformation(defender, upgrades)
        else:
            defender_lvl_up(defender, upgrades)
    else:
        if PLAYER.get("GOLD") < upgrades.get("price"):
            print("Pas assez de gold")
        else:
            print("pas assez tué de monstres")
        clean_canvas_option()
        create_options(defender.grid_x, defender.grid_y, defender.lvl - 1)

def defender_lvl_up(defender, upgrades):
    """Augmente le level des défenseurs"""
    PLAYER["GOLD"] -= upgrades.get("price")
    defender.damages += upgrades.get("upgrade_damages")
    defender.lvl += 1
    defender.range += upgrades.get("upgrade_range")
    defender.attack_speed -= upgrades.get("upgrade_speed")
    if defender.attack_speed < 1:
        defender.attack_speed = 1
    clean_canvas_stat_defender()
    show_stats_defender(defender)
    clean_canvas_option()
    create_options(defender.grid_x, defender.grid_y, defender.lvl - 1)

def defender_transformation(defender, upgrades):
    """Donne le pouvoir au défenseur"""
    clean_canvas_option()
    lvl_ability = upgrades.get("upgrade_ability")
    if lvl_ability == 1:
        Button(
            CAN_OPTIONS,
            text="DEGAT",
            command=lambda: transformation(defender, 0, upgrades),
            width=7,
            height=4
        ).place(x=0, y=0)
        Button(
            CAN_OPTIONS,
            text="GLACE",
            command=lambda: transformation(defender, 1, upgrades),
            width=7,
            height=4
        ).place(x=0, y=BLOC_SIZE)
        Button(
            CAN_OPTIONS,
            text="POISON",
            command=lambda: transformation(defender, 2, upgrades),
            width=7,
            height=4
        ).place(x=0, y=BLOC_SIZE*2)
    else:
        if defender.ability == "attack":
            defender.damages += lvl_ability * 100
        defender.ability_lvl += 1
        defender_lvl_up(defender, upgrades)

def transformation(defender, code, upgrades):
    """Donne le don au défenseur"""
    if code == 0:
        defender.ability = "attack"
        defender.damages += 50
    elif code == 1:
        defender.ability = "freeze"
    elif code == 2:
        defender.ability = "poison"
    defender.ability_lvl += 1
    defender_lvl_up(defender, upgrades)

def remove_obstacle(grid_x, grid_y):
    """Suppression de l'obstacle, conversion en case classique"""
    if PLAYER.get("GOLD") >= PRICE_REMOVE_OBSTACLE:
        PLAYER["GOLD"] -= PRICE_REMOVE_OBSTACLE
        MAP[grid_y][grid_x] = 0
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
    if value in ("x", 0):
        design.draw_bloc(value, CANVAS, BLOC_SIZE, grid_x * BLOC_SIZE, grid_y * BLOC_SIZE)

def creation_wave(code, click=None):
    """Création de la vague d'ennemies"""
    if click is not None:
        PLAYER["WAVE_RUNNING"] += 1
        B_START_WAVE.config(text="Vague suivante")
    if len(LIST_OF_MONSTERS) + len(DEAD_MONSTERS) < WAVE_SIZE * PLAYER.get("WAVE_RUNNING"):
        Monster(code)
        if SCREEN_ITEMS["RANGE_MONSTER"] is not None:
            CANVAS.tag_raise(SCREEN_ITEMS.get("RANGE_MONSTER"))
            for body_part in SCREEN_ITEMS.get("DEFENDER_PRINT").body:
                CANVAS.tag_raise(body_part)
        F.after(MONSTERS[code].get("wait_before_new_creation"), lambda: creation_wave(code))

def run_wave():
    """Lance la création de la vague d'ennemis lors du clique"""
    type_wave = random.randrange(len(MONSTERS))
    creation_wave(type_wave, 1)

class Monster():
    """Création d'un nouveau monstre"""
    # pylint: disable=too-many-instance-attributes
    def __init__(self, code):
        monster = MONSTERS[code]
        self.code = code
        self.width = monster.get("width")
        self.height = monster.get("height")
        self.pos_x = int(len(MAP) / 2) * BLOC_SIZE + BLOC_SIZE / 2 - self.width / 2
        self.pos_y = 0
        self.grid_x = int(len(MAP) / 2)
        self.grid_y = 0
        self.color = monster.get("color")
        self.max_life = monster.get("life")
        self.life = self.max_life
        self.is_alive = True
        self.gold = monster.get("gold")
        self.score = monster.get("score")
        self.wait_walk = monster.get("wait_loop_walk")
        self.direction = DOWN
        self.max_frames = monster.get("frames_gif")
        self.frames = [PhotoImage(
            file='monster.gif',
            format='gif -index %i' %(i)) for i in range(self.max_frames)]
        self.frame = 0
        self.image = CANVAS.create_image(
            self.pos_x + self.width / 2,
            self.pos_y + self.width / 2,
            image=self.frames[self.frame]
            )
        self.life_bar = design.upgrade_life(CANVAS, self)
        self.before_new_frame = 10

        self.time_freeze = 0
        self.time_poison = 0
        self.poisoner = None

        LIST_OF_MONSTERS.append(self)
        wave_run = str(len(LIST_OF_MONSTERS)+len(DEAD_MONSTERS))
        wave_max = str(WAVE_SIZE * PLAYER.get("WAVE_RUNNING"))
        L_WAVE_RUN.config(text="Avancée de la vague: "+wave_run+"/"+wave_max)

        self.auto_move()


    def auto_move(self):
        """Analyse les chemins possible et déplace le monstre"""
        if self.time_freeze == 0:
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
            self.before_new_frame -= 1
            if self.before_new_frame == 0:
                self.before_new_frame = 10
                self.frame += 1
                if self.frame >= self.max_frames:
                    self.frame = 0
                CANVAS.itemconfig(self.image, image=self.frames[self.frame])
            CANVAS.move(self.image, self.direction[0], self.direction[1])
            CANVAS.move(self.life_bar, self.direction[0], self.direction[1])
            self.adapt_on_grid()
        else:
            self.time_freeze -= self.wait_walk
            if self.time_freeze < 0:
                self.time_freeze = 0

        if self.time_poison > 0:
            self.life -= int((self.poisoner.damages/ self.poisoner.attack_speed) * (self.wait_walk))
            CANVAS.delete(self.life_bar)
            self.life_bar = design.upgrade_life(CANVAS, self)
            if self.life <= 0 and self.is_alive:
                self.poisoner.monster_killed += 1
                CANVAS.delete(self.poisoner.missile)
                self.poisoner.missile = None
                self.is_alive = False
                self.time_poison = 0
            self.time_poison -= self.wait_walk
            if self.time_poison < 0:
                self.time_poison = 0

        if self.grid_y < len(MAP) - 1 and self.life > 0:
            F.after(self.wait_walk, self.auto_move)
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
        CANVAS.delete(self.life_bar)
        CANVAS.delete(self.image)

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
        self.attack_speed = defender.get("attack_speed")

        self.ability = None
        self.ability_lvl = 0

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

        self.body = design.body_creation_defender(CANVAS, self)

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
                if self.ability_lvl > 0:
                    self.run_ability()

            CANVAS.delete(self.target.life_bar)
            if self.target.life > 0:
                self.target.life_bar = design.upgrade_life(CANVAS, self.target)
            if self.target.life == 0 and self.target.is_alive:
                self.monster_killed += 1
                self.target.is_alive = False
                if SCREEN_ITEMS["DEFENDER_PRINT"] == self:
                    show_stats_defender(self)
            CANVAS.delete(self.missile)
            self.missile = None
            F.after(self.attack_speed, self.auto_attack)
        else:
            F.after(1, self.attack)

    def run_ability(self):
        """Lance le sort du défenseur"""
        if random.randrange(100) < 10:
            if self.ability == "poison" and self.target.time_poison == 0:
                self.target.time_poison += 3000
                if self.target.poisoner is None:
                    self.target.poisoner = self
                print("poison")
            elif self.ability == "freeze" and self.target.time_freeze == 0:
                self.target.time_freeze += 2000
                print("freeze")

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
    [0, 0, 0, 0, "x", -1, "x", 0, 0, 0, 0],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, 0, 0, 0, "x", 0, "x", 0, 0, 0, -1],
    [-1, 0, "x", "x", 0, "x", 0, "x", "x", 0, -1],
    [-1, 0, 0, 0, "x", 0, "x", 0, 0, 0, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1],
    [-1, 0, "x", "x", 0, "x", 0, "x", "x", 0, -1],
    [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0]
]
BLOC_SIZE = 80

PLAYER = {
    "GOLD": 250000,
    "SCORE": 0,
    "LIFE": 100,
    "MONSTER_KILLED": 0,
    "WAVE_RUNNING": 0
}

SCREEN_ITEMS = {
    "STAT_DEFENDER_VISIBLE": False,
    "RANGE_MONSTER": None,
    "DEFENDER_PRINT": None
}

LENGTH_OPTIONS = 1
LENGTH_STATS = 5

PRICE_REMOVE_OBSTACLE = 2000



# Tarifs / point bonus:
# 2 * attack:
# 1 * range:
# 1 * attack speed:

# 40x + 100y = 100
# attack: 2
# range: 0.5
# attack_speed:
#   5000 - 1000: 0.05

DEFENDERS = [
    # DEFENDER 1
    {
        "width": BLOC_SIZE / 1.35,
        "height": BLOC_SIZE,
        "damages": 20,
        "range": BLOC_SIZE * 1.5,
        "attack_speed": 1000,
        "price": 100,
        "color": "black",
        "upgrades": [
            {
                "price": 80,
                "min_dead": 0,
                "upgrade_range": BLOC_SIZE * 0.2,
                "upgrade_damages": 10,
                "upgrade_speed": 100,
                "upgrade_ability": 0
            },
            {
                "price": 100,
                "min_dead": 0,
                "upgrade_range": BLOC_SIZE * 0.2,
                "upgrade_damages": 20,
                "upgrade_speed": 100,
                "upgrade_ability": 0
            },
            {
                "price": 150,
                "min_dead": 50,
                "upgrade_range": BLOC_SIZE * 0.2,
                "upgrade_damages": 50,
                "upgrade_speed": 100,
                "upgrade_ability": 1
            },
            {
                "price": 250,
                "min_dead": 0,
                "upgrade_range": BLOC_SIZE * 0.5,
                "upgrade_damages": 100,
                "upgrade_speed": 150,
                "upgrade_ability": 2
            },
            {
                "price": 1000,
                "min_dead": 200,
                "upgrade_range": BLOC_SIZE * 0.5,
                "upgrade_damages": 200,
                "upgrade_speed": 150,
                "upgrade_ability": 3
            }
        ]
    },

    # DEFENDER 2
    {
        "width": BLOC_SIZE / 1.35,
        "height": BLOC_SIZE,
        "damages": 50,
        "range": BLOC_SIZE * 2,
        "attack_speed": 1000,
        "price": 250,
        "color": "blue",
        "upgrades": [
            {
                "price": 200,
                "min_dead": 0,
                "upgrade_range": BLOC_SIZE * 0.2,
                "upgrade_damages": 10,
                "upgrade_speed": 100
            },
            {
                "price": 250,
                "min_dead": 0,
                "upgrade_range": BLOC_SIZE * 0.2,
                "upgrade_damages": 20,
                "upgrade_speed": 100
            },
            {
                "price": 350,
                "min_dead": 50,
                "upgrade_range": BLOC_SIZE * 0.2,
                "upgrade_damages": 50,
                "upgrade_speed": 100
            },
            {
                "price": 500,
                "min_dead": 0,
                "upgrade_range": BLOC_SIZE * 0.5,
                "upgrade_damages": 100,
                "upgrade_speed": 150
            },
            {
                "price": 2500,
                "min_dead": 200,
                "upgrade_range": BLOC_SIZE * 0.5,
                "upgrade_damages": 200,
                "upgrade_speed": 150
            }
        ]
    },
]

MONSTERS = [
    # MONSTER 1
    {
        "width": 80,
        "height": 80,
        "color": "red",
        # "life": 60,
        "life": 1000,
        "gold": 7,
        "score": 5,
        "wait_before_new_creation": 2000,
        "wait_loop_walk": 20,
        "frames_gif": 9
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
WAVE_SIZE = 1
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

CAN_STATS = Canvas(F, width=STATS_WIDTH, height=SCREEN_HEIGHT / 2, bg="black")
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

CAN_STATS_DEFENDER = Canvas(F, width=STATS_WIDTH, height=SCREEN_HEIGHT / 2, bg="black")
CAN_STATS_DEFENDER.place(x=SCREEN_WIDTH-STATS_WIDTH, y=SCREEN_HEIGHT / 2)
L_DAMAGE = Label(CAN_STATS_DEFENDER, text="", bg="black", fg="white")
L_DAMAGE.place(x=15, y=15)
L_RANGE = Label(CAN_STATS_DEFENDER, text="", bg="black", fg="white")
L_RANGE.place(x=15, y=45)
L_SPEED = Label(CAN_STATS_DEFENDER, text="", bg="black", fg="white")
L_SPEED.place(x=15, y=75)
L_KILLED = Label(CAN_STATS_DEFENDER, text="", bg="black", fg="white")
L_KILLED.place(x=15, y=105)




# scale_w = new_width/old_width
# scale_h = new_height/old_height

# NON FONCTIONNEL (affiche mais ne bouge pas)
# CANVAS.pack(expand = YES, fill = BOTH)
# scale_w = 2
# scale_h = 2
# img = PhotoImage(file="mon_image.gif").zoom(scale_w, scale_h)
# CANVAS.create_image(10, 10, anchor=NW, image=img)

main()
F.mainloop()
