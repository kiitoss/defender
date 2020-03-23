"""
    Fichier python du jeu de tower defense.
    Utilisation de tkinter pour l'interface graphique.
    Utilisation du fichier 'gameplay.py' pour les valeurs numeriques du jeu.
"""
from tkinter import Tk, Canvas, Button, Label, PhotoImage
import random
import sys
import gameplay




def main(code_difficulty):
    """Fonction principale, appellee apres creation de la fenetre et des canvas (tkinter)"""
    creation_all_waves(1)

    initialisation_labels()

    my_map = gameplay.MAPS[code_difficulty]
    creation_map(my_map)

    GAME_MANAGER["game_launched"] = True


def initialisation_labels():
    """Nettoie le canvas principal et configure les labels et les boutons de la fenetre"""
    for element in CANVAS.winfo_children():
        element.destroy()

    B_START_WAVE.place(x=15, y=35)
    B_SPEED.place(x=205, y=35)
    B_QUIT.place(x=305, y=35)
    waves_round = GAME_MANAGER.get("waves_round")
    L_WAVE_RUN.config(text="Avancée de la vague: 0/"+str(waves_round[0][1]))
    L_GOLD.config(text="Or: "+str(PLAYER.get("GOLD")))
    L_LIFE.config(text="Vies: "+str(PLAYER.get("LIFE")))
    L_MONSTER_KILLED.config(text="Monstres Tués: 0")
    L_SCORE.config(text="Score: "+str(PLAYER.get("SCORE")))


def creation_all_waves(coeff_wave):
    """
        Cree toutes les vagues du tour (initialement 12 vagues par tour)
        --> la vie des monstres et l'argent gagne augmente à chaque tour
    """
    full_wave = []
    for wave in GAME_MANAGER.get("waves"):
        wave_parameters = []
        numero_monster = wave[0]
        life_monster = wave[2]
        gold_monster = wave[3]

        monster = ALL_MONSTERS[numero_monster]
        monster["life"] = life_monster * coeff_wave
        monster["gold"] = gold_monster * coeff_wave
        wave_parameters.append(monster)

        for other_parameter in wave[1:]:
            wave_parameters.append(other_parameter)

        full_wave.append(wave_parameters)
    GAME_MANAGER["waves_round"] = full_wave


def on_click(event):
    """Detecte un clique de la souris sur le canvas de jeu et appel les fonctions correspondantes"""
    if GAME_MANAGER.get("game_launched") is False:
        return

    position_x = int(event.x / BLOC_SIZE)
    position_y = int(event.y / BLOC_SIZE)

    if GAME_MANAGER.get("case_shown") is not None:
        CANVAS.delete(GAME_MANAGER.get("case_shown"))
        GAME_MANAGER["case_shown"] = None

    if GAME_MANAGER.get("map")[position_y][position_x] in ("x", 0):
        GAME_MANAGER["case_shown"] = CANVAS.create_rectangle(
            position_x*BLOC_SIZE,
            position_y*BLOC_SIZE,
            (position_x+1)*BLOC_SIZE,
            (position_y+1)*BLOC_SIZE,
            width=3,
            outline="black",
            fill="black",
            stipple="gray75",
        )

    manager_frame_option("creation", position_x, position_y)


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


def upgrade_life(monster):
    """Mise à jour de la jauge de vie des enemies"""
    if monster.life <= monster.max_life / 3:
        color = "red"
    elif monster.life <= monster.max_life / 2:
        color = "orange"
    else:
        color = "green"

    return CANVAS.create_rectangle(
        monster.pos_x,
        monster.pos_y - 10,
        monster.pos_x + monster.width * monster.life / monster.max_life,
        monster.pos_y - 5,
        fill=color
        )




def manager_frame_option(action, pos_x=None, pos_y=None):
    """Gestion des elements a afficher sur FRAME_OPTION"""
    if action == "creation":
        if GAME_MANAGER["status_frame_option"] != "clean":
            clean_frame_option()

        code_cell = GAME_MANAGER.get("map")[pos_y][pos_x]
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
            show_my_defender(defender_shown)
        else: return

    elif action == "upgrade":
        defender_shown = GAME_MANAGER.get("defender_shown")
        if defender_shown is None:
            return
        L_KILLED.config(text="Monstres tués: "+str(defender_shown.monster_killed))

        if len(DEFENDERS[defender_shown.code].get("upgrades")) < defender_shown.lvl:
            return
        upgrades = DEFENDERS[defender_shown.code].get("upgrades")[defender_shown.lvl - 1]
        min_dead = upgrades.get("min_dead")
        if  min_dead != 0 and defender_shown.monster_killed == min_dead:
            clean_frame_option()
            show_my_defender(defender_shown)


def clean_frame_option():
    """Nettoie FRAME_OPTION"""
    status = GAME_MANAGER.get("status_frame_option")
    list_elements = FRAME_OPTION.winfo_children()
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

    GAME_MANAGER["status_frame_option"] = "clean"


def show_all_defenders(pos_x, pos_y):
    """Affiche tous les defenseurs que le joueur peut acheter"""
    my_images = [IMG_TOUR_1, IMG_TOUR_2, IMG_TOUR_D, IMG_TOUR_G, IMG_TOUR_P]
    for numero_defender, defender in enumerate(DEFENDERS):
        btn_defender = Button(
            FRAME_OPTION,
            text="prix: "+str(defender.get("price")),
            image=my_images[numero_defender][0],
            compound="top",
            command=lambda code=numero_defender: creation_defender(code, pos_x, pos_y),
            width=80,
            height=120
        )
        if numero_defender < 2:
            line = 1
            column = numero_defender*1.5+1.1
        else:
            line = 3
            column = numero_defender*1.5 - 2.7
        btn_defender.place(x=column*BLOC_SIZE, y=line*BLOC_SIZE)
    GAME_MANAGER["status_frame_option"] = "show_all_defenders"


def show_my_defender(defender_clicked):
    """Affiche les defenseurs sur lequel le joueur a clique avec ses statistiques"""
    GAME_MANAGER["defender_shown"] = defender_clicked
    L_DAMAGE.config(text="Attaque: "+str(defender_clicked.damages))
    L_RANGE.config(text="Range: "+str(defender_clicked.range))
    L_SPEED.config(text="Fréquence de tir: "+str(defender_clicked.attack_speed))
    L_KILLED.config(text="Monstres tués: "+str(defender_clicked.monster_killed))

    list_upgrades = DEFENDERS[defender_clicked.code].get("upgrades")
    max_col = int(STATS_WIDTH / BLOC_SIZE)
    if len(list_upgrades) >= defender_clicked.lvl:
        my_defender_upgrades = list_upgrades[defender_clicked.lvl - 1]
        min_dead = my_defender_upgrades.get("min_dead")
        price_upgrade = my_defender_upgrades.get("price")
        if min_dead != 0:
            my_text = "prix: "+str(price_upgrade)+"\n Kills > "+str(min_dead)
        else:
            my_text = "prix: "+str(price_upgrade)

        if defender_clicked.monster_killed < my_defender_upgrades.get("min_dead"):
            button_state = "disabled"
        else:
            button_state = "normal"

        if my_defender_upgrades.get("evolution"):
            abilities = ["DEGAT", "GLACE", "POISON"]
            max_col = int(STATS_WIDTH / BLOC_SIZE)
            for i, ability in enumerate(abilities):
                col = i*1.5 + ((max_col - len(abilities)) / 6)
                btn_upgrade = Button(
                    FRAME_OPTION,
                    text=ability+"\n\n"+my_text,
                    command=lambda code=i: transformation_defender(
                        defender_clicked,
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
                FRAME_OPTION,
                text="AMELIORER:\n\n"+my_text,
                command=lambda: upgrade_defender(defender_clicked, my_defender_upgrades))
            btn_upgrade.config(width=21, height=4)
            btn_upgrade.place(x=col*BLOC_SIZE, y=180)
            btn_upgrade.config(state=button_state)
    else:
        L_LVL_MAX.config(text="LEVEL MAX")
    col = (max_col-2.5) / 2
    btn_sell = Button(
        FRAME_OPTION,
        text="VENDRE:\n\nprix: "+str(DEFENDERS[defender_clicked.code].get("sell_price")),
        command=lambda: sell_defender(defender_clicked))
    btn_sell.config(width=21, height=4)
    btn_sell.place(x=col*BLOC_SIZE, y=320)

    GAME_MANAGER["range_shown"] = CANVAS.create_oval(
        defender_clicked.center_x-defender_clicked.range,
        defender_clicked.center_y-defender_clicked.range,
        defender_clicked.center_x+defender_clicked.range,
        defender_clicked.center_y+defender_clicked.range,
        width=3,
        outline="green",
        fill="green",
        stipple="gray25",
    )
    CANVAS.tag_raise(defender_clicked.body)

    GAME_MANAGER["status_frame_option"] = "show_my_defender"


def show_remove_obstacle(pos_x, pos_y):
    """Propose au joueur d'effacer l'obstacle"""
    max_col = int(STATS_WIDTH / BLOC_SIZE)
    col = (max_col-2.5) / 2
    btn_remove_obstacle = Button(
        FRAME_OPTION,
        text="Supprimer obstacle:\nprix: "+str(GAME_MANAGER.get("price_remove_obstacle")),
        command=lambda: remove_obstacle(pos_x, pos_y))
    btn_remove_obstacle.config(width=21, height=4)
    btn_remove_obstacle.place(x=col*BLOC_SIZE, y=180)
    GAME_MANAGER["status_frame_option"] = "show_remove_obstacle"




def creation_defender(code, position_x, position_y):
    """Creation d'un defenseur"""
    if GAME_MANAGER.get("case_shown") is not None:
        CANVAS.delete(GAME_MANAGER.get("case_shown"))
        GAME_MANAGER["case_shown"] = None
    price = DEFENDERS[code].get("price")
    if PLAYER.get("GOLD") >= price:
        PLAYER["GOLD"] -= price
        GAME_MANAGER.get("map")[position_y][position_x] = 1
        creation_bloc(position_x, position_y)
        clean_frame_option()
        Defender(code, position_x, position_y)
        upgrade_stats()
    else:
        clean_frame_option()


def upgrade_defender(defender, upgrades):
    """Amelioration du defenseur"""
    if PLAYER.get("GOLD") < upgrades.get("price") \
        or defender.monster_killed < upgrades.get("min_dead"):
        return

    PLAYER["GOLD"] -= upgrades.get("price")
    defender.damages += upgrades.get("upgrade_damages")
    defender.lvl += 1
    CANVAS.delete(defender.body)
    defender.body = CANVAS.create_image(
        defender.grid_x*BLOC_SIZE+BLOC_SIZE/2,
        defender.grid_y*BLOC_SIZE+BLOC_SIZE/2,
        image=defender.img[defender.lvl - 1]
    )
    defender.range += upgrades.get("upgrade_range")
    defender.attack_speed -= upgrades.get("upgrade_speed")
    if defender.attack_speed < 10:
        defender.attack_speed = 10
    upgrade_stats()
    manager_frame_option("creation", defender.grid_x, defender.grid_y)


def transformation_defender(defender, code, upgrades):
    """Fait évoluer le défenseur en lui donnant un pouvoir"""
    if PLAYER.get("GOLD") < upgrades.get("price") \
        or defender.monster_killed < upgrades.get("min_dead"):
        return

    if code == 0:
        defender.ability = "attack"
        defender.damages += 50
        defender.color = "red"
    elif code == 1:
        defender.ability = "freeze"
        defender.color = "blue"
    elif code == 2:
        defender.ability = "poison"
        defender.color = "green"
    clean_frame_option()
    upgrade_defender(defender, upgrades)


def sell_defender(defender):
    """Vente du defenseur"""
    PLAYER["GOLD"] += DEFENDERS[defender.code].get("sell_price")
    upgrade_stats()
    CANVAS.delete(defender.body)
    GAME_MANAGER.get("map")[defender.grid_y][defender.grid_x] = 0
    creation_bloc(defender.grid_x, defender.grid_y)
    defender.exist = False
    LIST_OF_DEFENDERS.remove(defender)
    clean_frame_option()


def remove_obstacle(grid_x, grid_y):
    """Suppression de l'obstacle, conversion en case classique"""
    price = GAME_MANAGER.get("price_remove_obstacle")
    if PLAYER.get("GOLD") < price:
        return
    if GAME_MANAGER.get("case_shown") is not None:
        CANVAS.delete(GAME_MANAGER.get("case_shown"))
        GAME_MANAGER["case_shown"] = None
    PLAYER["GOLD"] -= price
    GAME_MANAGER.get("map")[grid_y][grid_x] = 0
    creation_bloc(grid_x, grid_y)
    clean_frame_option()
    upgrade_stats()




def creation_map(my_map):
    """Creation de la carte du jeu selon la constante my_map"""
    GAME_MANAGER["map"] = my_map
    for position_y, line in enumerate(my_map):
        for position_x in range(len(line)):
            creation_bloc(position_x, position_y)


def creation_bloc(position_x, position_y):
    """Creation de chaque bloc de la carte"""
    value = GAME_MANAGER.get("map")[position_y][position_x]
    if value == -1:
        CANVAS.create_image(
            position_x*BLOC_SIZE+BLOC_SIZE/2,
            position_y*BLOC_SIZE+BLOC_SIZE/2,
            image=IMG_EMPTY_BLOC
        )

    elif value in ("x", 0):
        CANVAS.create_image(
            position_x*BLOC_SIZE+BLOC_SIZE/2,
            position_y*BLOC_SIZE+BLOC_SIZE/2,
            image=IMG_1_BLOC
        )

    if value == "x":
        CANVAS.create_image(
            position_x*BLOC_SIZE+BLOC_SIZE/2,
            position_y*BLOC_SIZE+BLOC_SIZE/2,
            image=IMG_X_BLOC
        )




def creation_wave(monster, remaining_monsters, click=None):
    """Creation de la vague d'ennemies"""
    if click is not None:
        B_START_WAVE.config(text="Vague suivante")

    waves_round = GAME_MANAGER.get("waves_round")
    total_wave_size = 0
    for i in range(GAME_MANAGER.get("wave_now")):
        total_wave_size += waves_round[i][1]
    if len(LIST_OF_MONSTERS) + len(DEAD_MONSTERS) < total_wave_size and remaining_monsters > 0:
        remaining_monsters -= 1
        Monster(monster)
        if GAME_MANAGER["range_shown"] is not None:
            CANVAS.tag_raise(GAME_MANAGER.get("range_shown"))
            CANVAS.tag_raise(GAME_MANAGER.get("defender_shown").body)
        monster_waiting_time = monster.get("wait_before_new_creation")
        waiting_time = int(monster_waiting_time / GAME_MANAGER.get("game_speed"))
        F.after(waiting_time, lambda: creation_wave(monster, remaining_monsters))


def launch_wave():
    """Lance la creation de la vague d'ennemies"""
    waves_round = GAME_MANAGER.get("waves_round")
    if len(waves_round) <= GAME_MANAGER.get("wave_now"):
        return
    GAME_MANAGER["wave_now"] += 1
    monster = waves_round[GAME_MANAGER.get("wave_now") - 1][0]
    wave_size = waves_round[GAME_MANAGER.get("wave_now") - 1][1]
    creation_wave(monster, wave_size, 1)




class Monster():
    """Creation d'un nouveau monstre"""
    # pylint: disable=too-many-instance-attributes
    def __init__(self, monster):
        self.monster_type = monster
        self.width = monster.get("width")
        self.height = monster.get("height")
        self.max_life = monster.get("life")
        self.life = self.max_life
        self.gold = monster.get("gold")
        self.score = monster.get("score")
        self.wait_walk = monster.get("wait_loop_walk")
        center_map = int(len(GAME_MANAGER.get("map")) / 2) * BLOC_SIZE + BLOC_SIZE / 2
        self.pos_x = center_map - self.width / 2
        self.pos_y = 0
        self.grid_x = int(len(GAME_MANAGER.get("map")) / 2)
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
        self.life_bar = upgrade_life(self)
        self.before_new_frame = GAME_MANAGER.get("wait_frame_animation")

        self.time_freeze = 0
        self.time_poison = 0
        self.poisoner = None

        LIST_OF_MONSTERS.append(self)
        wave_run = str(len(LIST_OF_MONSTERS)+len(DEAD_MONSTERS))
        waves_round = GAME_MANAGER.get("waves_round")
        total_wave_size = 0
        for i in range(GAME_MANAGER.get("wave_now")):
            total_wave_size += waves_round[i][1]
        L_WAVE_RUN.config(text="Avancée de la vague: "+wave_run+"/"+str(total_wave_size))

        self.auto_move()


    def auto_move(self):
        """Deplace le monstre s'il n'est pas freeze et baisse sa vie s'il est empoisonne"""
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
                self.before_new_frame = self.monster_type.get("wait_frame_animation")
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
            self.life_bar = upgrade_life(self)
            if self.life <= 0 and self.is_alive:
                self.poisoner.monster_killed += 1
                CANVAS.delete(self.poisoner.missile)
                self.poisoner.missile = None
                self.is_alive = False
                self.time_poison = 0
            self.time_poison -= self.wait_walk
            if self.time_poison < 0:
                self.time_poison = 0

        if self.grid_y < len(GAME_MANAGER.get("map")) - 1 and self.life > 0:
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
        """Tue le monstre"""
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
        waves_round = GAME_MANAGER.get("waves_round")
        total_wave_size = 0
        for i in range(GAME_MANAGER.get("wave_now")):
            total_wave_size += waves_round[i][1]
        if len(LIST_OF_MONSTERS) == 0 and monster_appeared == total_wave_size:
            DEAD_MONSTERS[:] = []
            prime = 0
            for i in range(GAME_MANAGER.get("wave_now")):
                prime += waves_round[0][4]
                waves_round.remove(waves_round[0])
            GAME_MANAGER["wave_now"] = 0
            PLAYER["GOLD"] += prime
            upgrade_stats()
            B_START_WAVE.config(text="Lancer la vague")
            if len(waves_round) > 0:
                len_wave = waves_round[0][1]
                L_WAVE_RUN.config(text="Avancée de la vague: 0/"+str(len_wave))
            else:
                print("VICTORY: ", (GAME_MANAGER.get("coeff_wave")-1)/4+1)
                GAME_MANAGER["coeff_wave"] += 4
                PLAYER["GOLD"] += (1000 * GAME_MANAGER.get("coeff_wave"))
                upgrade_stats()
                creation_all_waves(GAME_MANAGER.get("coeff_wave"))
        upgrade_stats()


    def analyse_direction(self):
        """Analyse les directions de deplacement possibles"""
        available_position = []
        coord_x = self.grid_x
        coord_y = self.grid_y
        direction = self.direction

        my_map = GAME_MANAGER.get("map")
        if (coord_x - 1 >= 0 and my_map[coord_y][coord_x - 1] == -1 \
            and direction != RIGHT):
            available_position.append(LEFT)
        if (coord_x + 1 < len(my_map[0]) and my_map[coord_y][coord_x + 1] == -1 \
            and direction != LEFT):
            available_position.append(RIGHT)
        if coord_y + 1 < len(my_map) and my_map[coord_y + 1][coord_x] == -1:
            if coord_y == len(my_map) - 2:
                available_position = [DOWN]
            else:
                available_position.append(DOWN)
        if coord_y < len(my_map) - 1:
            self.direction = available_position[random.randrange(len(available_position))]




class Defender():
    """Creation d'un nouveau defenseur"""
    # pylint: disable=too-many-instance-attributes
    def __init__(self, code, grid_x, grid_y):
        defender = DEFENDERS[code]
        self.code = code
        self.width = defender.get("width")
        self.height = defender.get("height")
        self.range = defender.get("range")
        self.price = defender.get("price")
        self.color = defender.get("color")
        self.ability = defender.get("ability")
        self.damages = defender.get("damages")
        self.attack_speed = defender.get("attack_speed")

        self.exist = True
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

        if self.code == 0:
            self.img = IMG_TOUR_1
        elif self.code == 1:
            self.img = IMG_TOUR_2
        elif self.code == 2:
            self.img = IMG_TOUR_D
        elif self.code == 3:
            self.img = IMG_TOUR_G
        elif self.code == 4:
            self.img = IMG_TOUR_P

        self.body = CANVAS.create_image(
            self.grid_x*BLOC_SIZE+BLOC_SIZE/2,
            self.grid_y*BLOC_SIZE+BLOC_SIZE/2,
            image=self.img[0]
        )

        LIST_OF_DEFENDERS.append(self)

        self.auto_attack()


    def auto_attack(self):
        """Gestion de l'auto-attaque du defenseur"""
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
        """Gestion du missile lance par le defenseur"""
        target_is_touched = self.move_missile()

        self.missile = CANVAS.create_oval(
            self.missile_coord[0]-5,
            self.missile_coord[1]-5,
            self.missile_coord[0]+5,
            self.missile_coord[1]+5,
            fill=self.color
        )

        if target_is_touched:
            if self.target.life - self.damages <= 0:
                self.target.life = 0
            else:
                self.target.life -= self.damages
                if self.ability is not None:
                    self.run_ability()

            CANVAS.delete(self.target.life_bar)
            if self.target.life > 0 and self.target.is_alive:
                self.target.life_bar = upgrade_life(self.target)
            if self.target.life == 0 and self.target.is_alive:
                self.monster_killed += 1
                self.target.is_alive = False
                if GAME_MANAGER["defender_shown"] == self:
                    manager_frame_option("upgrade")
            CANVAS.delete(self.missile)
            self.missile = None
            F.after(int(self.attack_speed / GAME_MANAGER.get("game_speed")), self.auto_attack)
        else:
            F.after(1, self.attack)


    def run_ability(self):
        """Lance le pouvoir du défenseur"""
        if random.randrange(100) > 10:
            return
        if self.ability == "poison" and self.target.time_poison == 0:
            self.target.time_poison += 3000
            if self.target.poisoner is None:
                self.target.poisoner = self
        elif self.ability == "freeze" and self.target.time_freeze == 0:
            self.target.time_freeze += 2000


    def move_missile(self):
        """Avance le missile et renvoie True lorsque l'ennemie est touche"""
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
PLAYER = gameplay.PLAYER
GAME_MANAGER = gameplay.GAME_MANAGER
MY_MAP = GAME_MANAGER.get("map")
BLOC_SIZE = gameplay.GAME_MANAGER.get("bloc_size")
ALL_MONSTERS = gameplay.MONSTERS
DEFENDERS = gameplay.DEFENDERS

# Création des variables adaptées aux paramètres précédents
STATS_WIDTH = 5 * BLOC_SIZE
SCREEN_WIDTH = int((len(MY_MAP[0]) + 5) * BLOC_SIZE)
SCREEN_HEIGHT = int(len(MY_MAP) * BLOC_SIZE)

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


CANVAS = Canvas(F, width=SCREEN_WIDTH-STATS_WIDTH, height=SCREEN_HEIGHT, bg="black")
CANVAS.bind("<Button-1>", on_click)
CANVAS.place(x=0, y=0)

B_IZI = Button(
    CANVAS,
    text="Facile",
    width=20,
    height=5,
    command=lambda: main(0))
B_IZI.place(x=350, y=235)

B_MEDIUM = Button(
    CANVAS,
    text="Moyen",
    width=20,
    height=5,
    command=lambda: main(1))
B_MEDIUM.place(x=350, y=345)

B_HARD = Button(
    CANVAS,
    text="Difficile",
    width=20,
    height=5,
    command=lambda: main(2))
B_HARD.place(x=350, y=455)

B_IMPOSSIBLE = Button(
    CANVAS,
    text="Hardcore",
    width=20,
    height=5,
    command=lambda: main(3))
B_IMPOSSIBLE.place(x=350, y=565)


FRAME_STATS = Canvas(F, width=STATS_WIDTH, height=SCREEN_HEIGHT / 2, bg="black")
FRAME_STATS.place(x=SCREEN_WIDTH-STATS_WIDTH, y=0)

B_START_WAVE = Button(
    FRAME_STATS,
    text="Lancer la vague",
    width=15,
    command=launch_wave)
B_START_WAVE.pack_forget()

B_SPEED = Button(FRAME_STATS, text="x1", command=change_speed)
B_SPEED.pack_forget()

B_QUIT = Button(FRAME_STATS, text="QUIT", command=sys.exit)
B_QUIT.pack_forget()

L_WAVE_RUN = Label(FRAME_STATS, text="")
L_WAVE_RUN.place(x=15, y=115)

L_GOLD = Label(FRAME_STATS, text="")
L_GOLD.place(x=15, y=175)

L_LIFE = Label(FRAME_STATS, text="")
L_LIFE.place(x=15, y=235)

L_MONSTER_KILLED = Label(FRAME_STATS, text="")
L_MONSTER_KILLED.place(x=15, y=295)

L_SCORE = Label(FRAME_STATS, text="")
L_SCORE.place(x=15, y=355)


FRAME_OPTION = Canvas(F, width=STATS_WIDTH, height=SCREEN_HEIGHT / 2, bg="black")
FRAME_OPTION.place(x=SCREEN_WIDTH-STATS_WIDTH, y=SCREEN_HEIGHT / 2)

L_DAMAGE = Label(FRAME_OPTION, text="")
L_DAMAGE.place(x=15, y=25)

L_RANGE = Label(FRAME_OPTION, text="")
L_RANGE.place(x=STATS_WIDTH/2, y=25)

L_SPEED = Label(FRAME_OPTION, text="")
L_SPEED.place(x=15, y=105)

L_KILLED = Label(FRAME_OPTION, text="")
L_KILLED.place(x=STATS_WIDTH/2, y=105)

L_LVL_MAX = Label(FRAME_OPTION, text="")
L_LVL_MAX.place(x=150, y=225)


for widget in FRAME_STATS.winfo_children() + FRAME_OPTION.winfo_children():
    if isinstance(widget, Label):
        widget.configure(bg="black", fg="white")


IMG_EMPTY_BLOC = PhotoImage(file='ressources/blocs/bloc_vide.png')
IMG_X_BLOC = PhotoImage(file='ressources/blocs/bloc_x.png')
IMG_1_BLOC = PhotoImage(file='ressources/blocs/bloc_1.png')
IMG_TOUR_1 = [
    PhotoImage(file='ressources/defenders/tour11.png'),
    PhotoImage(file='ressources/defenders/tour12.png'),
    PhotoImage(file='ressources/defenders/tour13.png'),
    PhotoImage(file='ressources/defenders/tour13.png')
]
IMG_TOUR_2 = [
    PhotoImage(file='ressources/defenders/tour21.png'),
    PhotoImage(file='ressources/defenders/tour22.png'),
    PhotoImage(file='ressources/defenders/tour23.png'),
    PhotoImage(file='ressources/defenders/tour23.png')
]
IMG_TOUR_P = [
    PhotoImage(file='ressources/defenders/tourP1.png'),
    PhotoImage(file='ressources/defenders/tourP2.png'),
    PhotoImage(file='ressources/defenders/tourP3.png')
]
IMG_TOUR_G = [
    PhotoImage(file='ressources/defenders/tourG1.png'),
    PhotoImage(file='ressources/defenders/tourG2.png'),
    PhotoImage(file='ressources/defenders/tourG3.png')
]
IMG_TOUR_D = [
    PhotoImage(file='ressources/defenders/tourD1.png'),
    PhotoImage(file='ressources/defenders/tourD2.png'),
    PhotoImage(file='ressources/defenders/tourD3.png')
]


F.mainloop()
