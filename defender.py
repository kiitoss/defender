"""Utilisation de tkinter pour l'interface graphique"""
from tkinter import Tk, Canvas, Button, Label, PhotoImage
import random
import sys
import design
import gameplay




def main():
    """Fonction principale"""
    creation_map()


def click_event(event):
    """Détection du clique de la souris sur le canvas de jeu"""
    pos_grid_x = int(event.x / BLOC_SIZE)
    pos_grid_y = int(event.y / BLOC_SIZE)
    manager_canvas_request("creation", pos_grid_x, pos_grid_y)


def change_speed():
    """Adapte la vitesse de jeu"""
    if GAME_MANAGER["game_speed"] == 1:
        GAME_MANAGER["game_speed"] = 2
    else:
        GAME_MANAGER["game_speed"] = 1
    B_SPEED.config(text="x"+str(GAME_MANAGER.get("game_speed")))


def upgrade_stats():
    """Mise à jour des statistiques du joueur"""
    L_GOLD.config(text="Or: "+str(PLAYER.get("GOLD")))
    L_SCORE.config(text="Score: "+str(PLAYER.get("SCORE")))
    L_LIFE.config(text="Vies: "+str(PLAYER.get("LIFE")))




def manager_canvas_request(action, pos_x=None, pos_y=None):
    """Fonction gérant le canvas de requêtes"""
    if action == "creation":
        if GAME_MANAGER["status_canvas_option"] != "clean":
            clean_canvas_request()

        code_cell = MAP[pos_y][pos_x]
        if code_cell == "x":
            show_remove_obstacle(pos_x, pos_y)
        elif code_cell == 0:
            show_all_defenders(pos_x, pos_y)
        elif code_cell > 0:
            defender_shown = None
            for defender in LIST_OF_DEFENDERS:
                if defender.grid_x == pos_x and defender.grid_y == pos_y:
                    defender_shown = defender
                    break
            if defender_shown is None:
                print("Error: no defender with theses positions")
                return
            show_my_defender(defender_shown)
        else: return

    elif action == "upgrade":
        defender_shown = GAME_MANAGER.get("defender_shown")
        if defender_shown is not None:
            L_KILLED.config(text="Monstres tués: "+str(defender_shown.monster_killed))
            upgrades = DEFENDERS[defender_shown.code].get("upgrades")[defender_shown.lvl - 1]
            min_dead = upgrades.get("min_dead")
            if  min_dead != 0 and defender_shown.monster_killed == min_dead:
                clean_canvas_request()
                show_my_defender(defender_shown)

def clean_canvas_request():
    """Nettoie le canvas des requêtes"""
    status = GAME_MANAGER.get("status_canvas_option")
    list_elements = FRAME_REQUEST.winfo_children()
    for button in list_elements:
        if isinstance(button, Button):
            button.destroy()
    if status == "show_my_defender":
        L_DAMAGE.config(text="")
        L_RANGE.config(text="")
        L_SPEED.config(text="")
        L_KILLED.config(text="")
        L_LVL_MAX.config(text="")

        range_shown = GAME_MANAGER.get("range_shown")
        if range_shown is not None:
            CANVAS.delete(range_shown)
            GAME_MANAGER["range_shown"] = None
        GAME_MANAGER["defender_shown"] = None

    if GAME_MANAGER.get("case_shown") is not None:
        CANVAS.delete(GAME_MANAGER.get("case_shown"))
        GAME_MANAGER["case_shown"] = None
    GAME_MANAGER["status_canvas_option"] = "clean"


def show_all_defenders(pos_x, pos_y):
    """Affiche tous les défenseurs que le joueur peut acheter"""
    GAME_MANAGER["case_shown"] = CANVAS.create_rectangle(
        pos_x*BLOC_SIZE,
        pos_y*BLOC_SIZE,
        (pos_x+1)*BLOC_SIZE,
        (pos_y+1)*BLOC_SIZE,
        width=3,
        outline="black",
        fill="black",
        stipple="gray75",
    )
    for i in range(len(DEFENDERS)):
        btn_defender = Button(
            FRAME_REQUEST,
            text="DEF "+str(i+1),
            command=lambda code=i: creation_defender(code, pos_x, pos_y),
            width=7,
            height=4
        )
        row = int((i * BLOC_SIZE) / STATS_WIDTH)
        col = (i - row*STATS_WIDTH/BLOC_SIZE)
        btn_defender.place(x=col*BLOC_SIZE, y=row*BLOC_SIZE)
    GAME_MANAGER["status_canvas_option"] = "show_all_defenders"


def show_my_defender(defender_shown):
    """Affiche les défenseurs sur lequel le joueur clique ainsi que ses statistiques"""
    GAME_MANAGER["defender_shown"] = defender_shown
    L_DAMAGE.config(text="Attaque: "+str(defender_shown.damages))
    L_RANGE.config(text="Range: "+str(defender_shown.range))
    L_SPEED.config(text="Fréquence de tir: "+str(defender_shown.attack_speed))
    L_KILLED.config(text="Monstres tués: "+str(defender_shown.monster_killed))

    list_upgrades = DEFENDERS[defender_shown.code].get("upgrades")
    max_col = int(STATS_WIDTH / BLOC_SIZE)
    if len(list_upgrades) >= defender_shown.lvl:
        my_defender_upgrades = list_upgrades[defender_shown.lvl - 1]
        min_dead = my_defender_upgrades.get("min_dead")
        price_upgrade = my_defender_upgrades.get("price")
        if min_dead != 0:
            my_text = "prix: "+str(price_upgrade)+"\n Kills > "+str(min_dead)
        else:
            my_text = "prix: "+str(price_upgrade)

        if defender_shown.monster_killed < my_defender_upgrades.get("min_dead"):
            button_state = "disabled"
        else:
            button_state = "normal"

        if my_defender_upgrades.get("evolution"):
            abilities = ["DEGAT", "GLACE", "POISON"]
            max_col = int(STATS_WIDTH / BLOC_SIZE)
            for i, ability in enumerate(abilities):
                col = i*1.5 + ((max_col - len(abilities)) / 6)
                btn_upgrade = Button(
                    FRAME_REQUEST,
                    text=ability+"\n\n"+my_text,
                    command=lambda code=i: transformation_defender(
                        defender_shown,
                        code,
                        my_defender_upgrades),
                    width=10,
                    height=6
                )
                btn_upgrade.place(x=col*BLOC_SIZE, y=180)
                btn_upgrade.config(state=button_state)
        else:
            col = (max_col-2.5) / 2
            btn_upgrade = Button(
                FRAME_REQUEST,
                text="AMELIORER:\n\n"+my_text,
                command=lambda: upgrade_defender(defender_shown, my_defender_upgrades))
            btn_upgrade.config(width=21, height=4)
            btn_upgrade.place(x=col*BLOC_SIZE, y=180)
            btn_upgrade.config(state=button_state)
    else:
        L_LVL_MAX.config(text="LEVEL MAX")
    col = (max_col-2.5) / 2
    btn_sell = Button(
        FRAME_REQUEST,
        text="VENDRE:\n\nprix: "+str(DEFENDERS[defender_shown.code].get("sell_price")),
        command=lambda: sell_defender(defender_shown))
    btn_sell.config(width=21, height=4)
    btn_sell.place(x=col*BLOC_SIZE, y=320)

    GAME_MANAGER["range_shown"] = CANVAS.create_oval(
        defender_shown.center_x-defender_shown.range,
        defender_shown.center_y-defender_shown.range,
        defender_shown.center_x+defender_shown.range,
        defender_shown.center_y+defender_shown.range,
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
    GAME_MANAGER["status_canvas_option"] = "show_my_defender"


def show_remove_obstacle(pos_x, pos_y):
    """Propose au joueur d'effacer l'obstacle"""
    max_col = int(STATS_WIDTH / BLOC_SIZE)
    col = (max_col-2.5) / 2
    btn_remove_obstacle = Button(
        FRAME_REQUEST,
        text="del obstacle",
        command=lambda: remove_obstacle(pos_x, pos_y))
    btn_remove_obstacle.config(width=21, height=4)
    btn_remove_obstacle.place(x=col*BLOC_SIZE, y=180)
    GAME_MANAGER["status_canvas_option"] = "show_remove_obstacle"




def creation_defender(code, grid_x, grid_y):
    """Création d'un défenseur"""
    price = DEFENDERS[code].get("price")
    if PLAYER.get("GOLD") >= price:
        PLAYER["GOLD"] -= price
        MAP[grid_y][grid_x] = 1
        creation_bloc(grid_x, grid_y)
        clean_canvas_request()
        Defender(code, grid_x, grid_y)
        upgrade_stats()


def upgrade_defender(defender, upgrades):
    """Amélioration du défenseur"""
    if PLAYER.get("GOLD") < upgrades.get("price") \
        or defender.monster_killed < upgrades.get("min_dead"):
        return

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
    """Fait évoluer le défenseur en lui donnant un pouvoir"""
    if PLAYER.get("GOLD") < upgrades.get("price") \
        or defender.monster_killed < upgrades.get("min_dead"):
        return

    if code == 0:
        defender.ability = "attack"
        defender.damages += 50
    elif code == 1:
        defender.ability = "freeze"
    elif code == 2:
        defender.ability = "poison"
    defender.body = design.body_creation_defender(CANVAS, defender, (code+1))
    clean_canvas_request()
    upgrade_defender(defender, upgrades)


def sell_defender(defender):
    """Vente du défenseur"""
    PLAYER["GOLD"] += DEFENDERS[defender.code].get("sell_price")
    upgrade_stats()
    # Pour l'instant que le corps des défenseurs est fait en pixel-art et non en GIF:
    for body_part in defender.body:
        CANVAS.delete(body_part)
    # Lorsque les défenseurs auront été changés en GIF:
    # CANVAS.remove(defender.body)
    MAP[defender.grid_y][defender.grid_x] = 0
    creation_bloc(defender.grid_x, defender.grid_y)
    defender.exist = False
    LIST_OF_DEFENDERS.remove(defender)
    clean_canvas_request()

def remove_obstacle(grid_x, grid_y):
    """Suppression de l'obstacle, conversion en case classique"""
    price = GAME_MANAGER.get("price_remove_obstacle")
    if PLAYER.get("GOLD") >= price:
        PLAYER["GOLD"] -= price
        MAP[grid_y][grid_x] = 0
        creation_bloc(grid_x, grid_y)
        clean_canvas_request()
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
    total_wave_size = GAME_MANAGER.get("wave_size") * GAME_MANAGER.get("wave_running")
    if len(LIST_OF_MONSTERS) + len(DEAD_MONSTERS) < total_wave_size:
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
        self.color = monster.get("color")
        self.max_life = monster.get("life")
        self.life = self.max_life
        self.gold = monster.get("gold")
        self.score = monster.get("score")
        self.wait_walk = monster.get("wait_loop_walk")

        self.pos_x = int(len(MAP) / 2) * BLOC_SIZE + BLOC_SIZE / 2 - self.width / 2
        self.pos_y = 0
        self.grid_x = int(len(MAP) / 2)
        self.grid_y = 0
        self.is_alive = True
        self.direction = DOWN

        self.max_frames = monster.get("frames_gif")
        self.frames = [PhotoImage(
            file=monster.get("img"),
            format='gif -index %i' %(i)) for i in range(self.max_frames)]
        self.frame = 0
        self.image = CANVAS.create_image(
            self.pos_x + self.width / 2,
            self.pos_y + self.width / 2,
            image=self.frames[self.frame]
            )
        self.life_bar = design.upgrade_life(CANVAS, self)
        self.before_new_frame = GAME_MANAGER.get("wait_frame_animation")

        self.time_freeze = 0
        self.time_poison = 0
        self.poisoner = None

        LIST_OF_MONSTERS.append(self)
        wave_run = str(len(LIST_OF_MONSTERS)+len(DEAD_MONSTERS))
        wave_max = str(GAME_MANAGER.get("wave_size") * GAME_MANAGER.get("wave_running"))
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

            if ((direction == DOWN and int(middle_y_monster) == int(middle_y_bloc)) \
                or (direction in (LEFT, RIGHT) and int(middle_x_monster) == int(middle_x_bloc))):
                self.analyse_direction()

            self.pos_x += self.direction[0]
            self.pos_y += self.direction[1]
            self.before_new_frame -= 1
            if self.before_new_frame == 0:
                self.before_new_frame = GAME_MANAGER.get("wait_frame_animation")
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
        """Check sur quelle position de la grille se trouve l'ennemie"""
        if self.pos_x > (self.grid_x + 1) * BLOC_SIZE:
            self.grid_x += 1
        if self.pos_x < self.grid_x * BLOC_SIZE:
            self.grid_x -= 1
        if self.pos_y > (self.grid_y + 1) * BLOC_SIZE:
            self.grid_y += 1

    def auto_kill(self):
        """Détruit le monstre"""
        if self.life <= 0:
            PLAYER["GOLD"] += self.gold
            PLAYER["SCORE"] += self.score
            PLAYER["MONSTER_KILLED"] += 1
            L_MONSTER_KILLED.config(text="Monstres tués: "+str(PLAYER.get("MONSTER_KILLED")))
        else:
            PLAYER["LIFE"] -= 1
            if PLAYER["LIFE"] == 0:
                print("Défaite")
                sys.exit()
        upgrade_stats()
        LIST_OF_MONSTERS.remove(self)
        DEAD_MONSTERS.append(self)
        CANVAS.delete(self.life_bar)
        CANVAS.delete(self.image)

        monster_appeared = len(LIST_OF_MONSTERS) + len(DEAD_MONSTERS)
        full_wave_size = GAME_MANAGER.get("wave_running") * GAME_MANAGER.get("wave_size")
        if len(LIST_OF_MONSTERS) == 0 and monster_appeared == full_wave_size:
            DEAD_MONSTERS[:] = []
            GAME_MANAGER["wave_running"] = 0
            B_START_WAVE.config(text="Lancer la vague")
            L_WAVE_RUN.config(text="Avancée de la vague: 0/"+str(GAME_MANAGER.get("wave_size")))
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

        self.exist = True
        self.ability = None
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
        if not self.exist:
            return

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
                if self.ability is not None:
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
        """Lance le pouvoir du défenseur"""
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




# Variables concernant le gameplay (argent, vies, différents défenseurs, monstres...)
MAP = gameplay.MAP
PLAYER = gameplay.PLAYER
GAME_MANAGER = gameplay.GAME_MANAGER
BLOC_SIZE = gameplay.GAME_MANAGER.get("bloc_size")
DEFENDERS = gameplay.DEFENDERS
MONSTERS = gameplay.MONSTERS

# Création des variables adaptées aux paramètres précédents
STATS_WIDTH = 5 * BLOC_SIZE
SCREEN_WIDTH = int((len(MAP[0]) + 5) * BLOC_SIZE)
SCREEN_HEIGHT = int(len(MAP) * BLOC_SIZE)

# Autres variables
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
LIST_OF_MONSTERS = []
DEAD_MONSTERS = []
LIST_OF_DEFENDERS = []




# Création de la fenêtre et des canvas
F = Tk()
F.geometry(str(SCREEN_WIDTH)+"x"+str(SCREEN_HEIGHT))

CANVAS = Canvas(F, width=SCREEN_WIDTH-STATS_WIDTH, height=SCREEN_HEIGHT)
CANVAS.bind("<Button-1>", click_event)
CANVAS.place(x=0, y=0)

FRAME_STATS = Canvas(F, width=STATS_WIDTH, height=SCREEN_HEIGHT / 2, bg="black")
FRAME_STATS.place(x=SCREEN_WIDTH-STATS_WIDTH, y=0)
B_START_WAVE = Button(
    FRAME_STATS,
    text="Lancer la vague",
    width=15,
    command=lambda: creation_wave(random.randrange(len(MONSTERS)), 1))
B_START_WAVE.place(x=15, y=35)
B_SPEED = Button(FRAME_STATS, text="x1", command=change_speed)
B_SPEED.place(x=205, y=35)
L_WAVE_RUN = Label(FRAME_STATS, text="Avancée de la vague: 0/"+str(GAME_MANAGER.get("wave_size")))
L_WAVE_RUN.place(x=15, y=115)
L_SCORE = Label(FRAME_STATS, text="Score: "+str(PLAYER.get("SCORE")))
L_SCORE.place(x=15, y=175)
L_GOLD = Label(FRAME_STATS, text="Or: "+str(PLAYER.get("GOLD")))
L_GOLD.place(x=15, y=235)
L_MONSTER_KILLED = Label(FRAME_STATS, text="Monstres Tués: 0")
L_MONSTER_KILLED.place(x=15, y=295)
L_LIFE = Label(FRAME_STATS, text="Vies: "+str(PLAYER.get("LIFE")))
L_LIFE.place(x=15, y=355)

FRAME_REQUEST = Canvas(F, width=STATS_WIDTH, height=SCREEN_HEIGHT / 2, bg="black")
FRAME_REQUEST.place(x=SCREEN_WIDTH-STATS_WIDTH, y=SCREEN_HEIGHT / 2)
L_DAMAGE = Label(FRAME_REQUEST, text="")
L_DAMAGE.place(x=15, y=25)
L_RANGE = Label(FRAME_REQUEST, text="")
L_RANGE.place(x=STATS_WIDTH/2, y=25)
L_SPEED = Label(FRAME_REQUEST, text="")
L_SPEED.place(x=15, y=105)
L_KILLED = Label(FRAME_REQUEST, text="")
L_KILLED.place(x=STATS_WIDTH/2, y=105)
L_LVL_MAX = Label(FRAME_REQUEST, text="")
L_LVL_MAX.place(x=150, y=225)


for widget in FRAME_STATS.winfo_children() + FRAME_REQUEST.winfo_children():
    if isinstance(widget, Label):
        widget.configure(bg="black", fg="white")

main()
F.mainloop()
