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
    pos_grid_x = int(event.x / BLOC_SIZE)
    pos_grid_y = int(event.y / BLOC_SIZE)
    manager_canvas_request("creation", pos_grid_x, pos_grid_y)

def change_speed():
    """Adapte la vitesse lors d'un clique"""
    if GAME_MANAGER["game_speed"] == 1:
        GAME_MANAGER["game_speed"] = 2
    else:
        GAME_MANAGER["game_speed"] = 1
    B_SPEED.config(text="x"+str(GAME_MANAGER.get("game_speed")))

def clean_canvas_request():
    """Nettoie le canvas où s'affichent les propositions"""
    status = GAME_MANAGER.get("status_canvas_option")
    # if status in ("show_all_defenders", "show_remove_obstacle"):
    list_elements = CAN_REQUEST.winfo_children()
    for element in list_elements:
        if isinstance(element, Button):
            element.destroy()
    if status == "show_my_defender":
        L_DAMAGE.config(text="")
        L_RANGE.config(text="")
        L_SPEED.config(text="")
        L_KILLED.config(text="")
        L_LVL_MAX.config(text="")

    range_shown = GAME_MANAGER.get("range_shown")
    if range_shown is not None:
        CANVAS.delete(range_shown)
        range_shown = None

    GAME_MANAGER["status_canvas_option"] = "clean"

def manager_canvas_request(action, pos_x=None, pos_y=None):
    """Fonction gérant le canvas de requêtes"""
    if action == "creation" and (pos_x is None or pos_y is None):
        print("Error: argument missing")
        return

    if action == "creation":
        if GAME_MANAGER["status_canvas_option"] != "clean":
            clean_canvas_request()

        code_cell = MAP[pos_y][pos_x]
        if code_cell == "x":
            next_draw = "show_remove_obstacle"
        elif code_cell == 0:
            next_draw = "show_all_defenders"
        elif code_cell > 0:
            next_draw = "show_my_defender"
            defender_shown = None
            for defender in LIST_OF_DEFENDERS:
                if defender.grid_x == pos_x and defender.grid_y == pos_y:
                    defender_shown = defender
                    break
            if defender_shown is None:
                print("Error: no defender with theses positions")
                return
        elif code_cell == -1:
            return
        else:
            print("Error: cellule code not understandable")
            return


        if next_draw == "show_all_defenders":
            for i in range(len(DEFENDERS)):
                Button(
                    CAN_REQUEST,
                    text="DEF "+str(i+1),
                    command=lambda code=i: creation_defender(code, pos_x, pos_y),
                    width=7,
                    height=4
                ).place(x=0, y=i * BLOC_SIZE)

        elif next_draw == "show_my_defender":
            if defender_shown is None:
                print('Error: Aucun défenseur envoyé en paramètre')
                return

            GAME_MANAGER["defender_shown"] = defender_shown
            L_DAMAGE.config(text="Attaque: "+str(defender_shown.damages))
            L_RANGE.config(text="Range: "+str(defender_shown.range))
            L_SPEED.config(text="Fréquence de tir: "+str(defender_shown.attack_speed))
            L_KILLED.config(text="Monstres tués: "+str(defender_shown.monster_killed))

            list_upgrades = DEFENDERS[defender_shown.code].get("upgrades")
            if len(list_upgrades) >= defender_shown.lvl:
                my_defender_upgrades = list_upgrades[defender_shown.lvl - 1]
                btn_upgrade = Button(
                    CAN_REQUEST,
                    text="UPGRADE \n price: \n"+str(my_defender_upgrades.get("price")),
                    command=lambda: upgrade_defender(defender_shown, my_defender_upgrades))
                btn_upgrade.config(width=7, height=4)
                btn_upgrade.place(x=0, y=0)
            else:
                L_LVL_MAX.config(text="LVL MAX")


            GAME_MANAGER["range_shown"] = CANVAS.create_oval(
                defender.center_x-defender.range,
                defender.center_y-defender.range,
                defender.center_x+defender.range,
                defender.center_y+defender.range,
                width=3,
                outline="green",
                fill="green",
                stipple="gray25",
            )

            # Pour l'instant que le corps des défenseurs est fait en pixel-art et non en GIF:
            for body_part in defender_shown.body:
                CANVAS.tag_raise(body_part)

            # Lorsque les défenseurs auront été changés en GIF:
            # CANVAS.tag_raise(defender_shown.body)

        elif next_draw == "show_remove_obstacle":
            btn_remove_obstacle = Button(
                CAN_REQUEST,
                text="del obstacle",
                command=lambda: remove_obstacle(pos_x, pos_y))
            btn_remove_obstacle.config(width=7, height=4)
            btn_remove_obstacle.place(x=0, y=0)

        GAME_MANAGER["status_canvas_option"] = next_draw

    elif action == "upgrade":
        defender_shown = GAME_MANAGER["defender_shown"]
        if defender_shown is None:
            print("Error: no defender in memory")
            return
        L_KILLED.config(text="Monstres tués: "+str(defender_shown.monster_killed))


def upgrade_stats():
    """Mise à jour des statistiques du joueur"""
    L_GOLD.config(text="Or: "+str(PLAYER.get("GOLD")))
    L_SCORE.config(text="Score: "+str(PLAYER.get("SCORE")))
    L_LIFE.config(text="Vies: "+str(PLAYER.get("LIFE")))


def upgrade_defender(defender, upgrades, evolution_done=False):
    """Amélioration des défenseurs"""
    if PLAYER.get("GOLD") < upgrades.get("price") \
        or defender.monster_killed < upgrades.get("min_dead"):
        clean_canvas_request()
        return

    if upgrades.get("evolution") and evolution_done is False:
        abilities = ["DEGAT", "GLACE", "POISON"]
        for i in range(3):
            Button(
                CAN_REQUEST,
                text=abilities[i],
                command=lambda code=i: transformation_defender(defender, code, upgrades),
                width=7,
                height=4
            ).place(x=0, y=i*BLOC_SIZE)
    else:
        PLAYER["GOLD"] -= upgrades.get("price")
        defender.damages += upgrades.get("upgrade_damages")
        defender.lvl += 1
        defender.range += upgrades.get("upgrade_range")
        defender.attack_speed -= upgrades.get("upgrade_speed")
        if defender.attack_speed < 10:
            defender.attack_speed = 10
        upgrade_stats()
        manager_canvas_request("creation", defender.grid_x, defender.grid_y)


def transformation_defender(defender, code, upgrades):
    """Donne le don au défenseur"""
    if code == 0:
        defender.ability = "attack"
        defender.damages += 50
    elif code == 1:
        defender.ability = "freeze"
    elif code == 2:
        defender.ability = "poison"
    defender.body = design.body_creation_defender(CANVAS, defender, (code+1))
    clean_canvas_request()
    upgrade_defender(defender, upgrades, True)



def remove_obstacle(grid_x, grid_y):
    """Suppression de l'obstacle, conversion en case classique"""
    if PLAYER.get("GOLD") >= PRICE_REMOVE_OBSTACLE:
        PLAYER["GOLD"] -= PRICE_REMOVE_OBSTACLE
        MAP[grid_y][grid_x] = 0
        creation_bloc(grid_x, grid_y)
        clean_canvas_request()
        upgrade_stats()

def creation_defender(code, grid_x, grid_y):
    """Création d'un défenseur contre les ennemis"""
    price = DEFENDERS[code].get("price")
    if PLAYER.get("GOLD") >= price:
        PLAYER["GOLD"] -= price
        MAP[grid_y][grid_x] = 1
        creation_bloc(grid_x, grid_y)
        clean_canvas_request()
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
        GAME_MANAGER["wave_running"] += 1
        B_START_WAVE.config(text="Vague suivante")
    if len(LIST_OF_MONSTERS) + len(DEAD_MONSTERS) < WAVE_SIZE * GAME_MANAGER.get("wave_running"):
        Monster(code)
        if GAME_MANAGER["range_shown"] is not None:
            CANVAS.tag_raise(GAME_MANAGER.get("range_shown"))
            # Pour l'instant que le corps des défenseurs est fait en pixel-art et non en GIF:
            for body_part in GAME_MANAGER.get("defender_shown").body:
                CANVAS.tag_raise(body_part)
            # Lorsque les défenseurs auront été changés en GIF:
            # CANVAS.tag_raise(defender_shown.body)
        monster_waiting_time = MONSTERS[code].get("wait_before_new_creation")
        waiting_time = int(monster_waiting_time / GAME_MANAGER.get("game_speed"))
        F.after(waiting_time, lambda: creation_wave(code))

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
        wave_max = str(WAVE_SIZE * GAME_MANAGER.get("wave_running"))
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
            F.after(int(self.wait_walk / GAME_MANAGER.get("game_speed")), self.auto_move)
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
        full_wave_size = GAME_MANAGER.get("wave_running") * WAVE_SIZE
        if len(LIST_OF_MONSTERS) == 0 and monster_appeared == full_wave_size:
            DEAD_MONSTERS[:] = []
            GAME_MANAGER["wave_running"] = 0
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
        self.monster_killed = 999990

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
                if GAME_MANAGER["defender_shown"] == self:
                    manager_canvas_request("upgrade")
            CANVAS.delete(self.missile)
            self.missile = None
            F.after(int(self.attack_speed / GAME_MANAGER.get("game_speed")), self.auto_attack)
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
    "MONSTER_KILLED": 0
}

GAME_MANAGER = {
    "status_canvas_option": "clean",
    "game_speed": 1,
    "defender_shown": None,
    "range_shown": None,
    "wave_running": 0
}

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
            },
            {
                "price": 100,
                "min_dead": 0,
                "upgrade_range": BLOC_SIZE * 0.2,
                "upgrade_damages": 20,
                "upgrade_speed": 100,
            },
            {
                "price": 150,
                "min_dead": 50,
                "upgrade_range": BLOC_SIZE * 0.2,
                "upgrade_damages": 50,
                "upgrade_speed": 100,
                "evolution": True
            },
            {
                "price": 250,
                "min_dead": 0,
                "upgrade_range": BLOC_SIZE * 0.5,
                "upgrade_damages": 100,
                "upgrade_speed": 150,
            },
            {
                "price": 1000,
                "min_dead": 200,
                "upgrade_range": BLOC_SIZE * 0.5,
                "upgrade_damages": 200,
                "upgrade_speed": 150,
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
        "life": 60,
        "gold": 7,
        "score": 5,
        "wait_before_new_creation": 2000,
        "wait_loop_walk": 20,
        "frames_gif": 9
    }
]

# Création des variables selon les paramètres originaux
STATS_WIDTH = LENGTH_STATS * BLOC_SIZE
SCREEN_WIDTH = int((len(MAP[0]) + LENGTH_STATS) * BLOC_SIZE)
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

CANVAS = Canvas(F, width=SCREEN_WIDTH-STATS_WIDTH, height=SCREEN_HEIGHT)
CANVAS.bind("<Button-1>", click_event)
CANVAS.place(x=0, y=0)

CAN_STATS = Canvas(F, width=STATS_WIDTH, height=SCREEN_HEIGHT / 2, bg="black")
CAN_STATS.place(x=SCREEN_WIDTH-STATS_WIDTH, y=0)
B_START_WAVE = Button(
    CAN_STATS,
    text="Lancer la vague",
    command=lambda: creation_wave(random.randrange(len(MONSTERS)), 1))
B_START_WAVE.place(x=15, y=15)
B_SPEED = Button(CAN_STATS, text="x1", command=change_speed)
B_SPEED.place(x=205, y=15)
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

CAN_REQUEST = Canvas(F, width=STATS_WIDTH, height=SCREEN_HEIGHT / 2, bg="black")
CAN_REQUEST.place(x=SCREEN_WIDTH-STATS_WIDTH, y=SCREEN_HEIGHT / 2)
L_DAMAGE = Label(CAN_REQUEST, text="", bg="black", fg="white")
L_DAMAGE.place(x=15, y=15)
L_RANGE = Label(CAN_REQUEST, text="", bg="black", fg="white")
L_RANGE.place(x=15, y=45)
L_SPEED = Label(CAN_REQUEST, text="", bg="black", fg="white")
L_SPEED.place(x=15, y=75)
L_KILLED = Label(CAN_REQUEST, text="", bg="black", fg="white")
L_KILLED.place(x=15, y=105)
L_LVL_MAX = Label(CAN_REQUEST, text="", bg="black", fg="white")
L_LVL_MAX.place(x=15, y=135)



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
