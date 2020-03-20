"""Toutes les valeurs concernant le gameplay du jeu sont ici"""

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
    "case_shown": None,
    "price_remove_obstacle": 2000,
    "wave_size": 0,
    "bloc_size": 80,
    "wait_frame_animation": 10,
    "waves": [[0, 20], [1, 10]],
    "wave_now": 0
}

BLOC_SIZE = GAME_MANAGER.get("bloc_size")

DEFENDERS = [
    {
        "width": BLOC_SIZE / 1.35,
        "height": BLOC_SIZE,
        "damages": 20,
        "range": BLOC_SIZE * 1.5,
        "attack_speed": 1000,
        "price": 100,
        "color": "black",
        "sell_price": 20,
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
                "min_dead": 150,
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
        "sell_price": 40,
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
    }
]



MONSTERS = [
    # PIEUVRE
    {
        "width": 72,
        "height": 80,
        "color": "red",
        "life": 60,
        "gold": 7,
        "score": 5,
        "wait_before_new_creation": 1500,
        "wait_loop_walk": 20,
        "img": "ressources/monsters/pieuvre.gif",
        "frames_gif": 5,
        "wait_frame_animation": 7
    },
    # BOULE
    {
        "width": 56,
        "height": 80,
        "color": "red",
        "life": 60,
        "gold": 7,
        "score": 5,
        "wait_before_new_creation": 1500,
        "wait_loop_walk": 20,
        "img": "ressources/monsters/boule.gif",
        "frames_gif": 6,
        "wait_frame_animation": 7
    },
    # SQUELETTE
    {
        "width": 80,
        "height": 80,
        "color": "red",
        "life": 60,
        "gold": 7,
        "score": 5,
        "wait_before_new_creation": 2000,
        "wait_loop_walk": 20,
        "img": "ressources/monsters/squelette.gif",
        "frames_gif": 9,
        "wait_frame_animation": 10
    },
    # CHEVALIER
    {
        "width": 77,
        "height": 80,
        "color": "red",
        "life": 60,
        "gold": 7,
        "score": 5,
        "wait_before_new_creation": 2000,
        "wait_loop_walk": 20,
        "img": "ressources/monsters/chevalier.gif",
        "frames_gif": 5,
        "wait_frame_animation": 10
    },
    # CHAMPIGNON
    {
        "width": 80,
        "height": 80,
        "color": "red",
        "life": 60,
        "gold": 7,
        "score": 5,
        "wait_before_new_creation": 1000,
        "wait_loop_walk": 8,
        "img": "ressources/monsters/champignon.gif",
        "frames_gif": 8,
        "wait_frame_animation": 5
    },
    # CYCLOPE
    {
        "width": 80,
        "height": 80,
        "color": "red",
        "life": 60,
        "gold": 7,
        "score": 5,
        "wait_before_new_creation": 2000,
        "wait_loop_walk": 20,
        "img": "ressources/monsters/cyclope.gif",
        "frames_gif": 6,
        "wait_frame_animation": 7
    },
    # POULPE_BIS
    {
        "width": 80,
        "height": 80,
        "color": "red",
        "life": 60,
        "gold": 7,
        "score": 5,
        "wait_before_new_creation": 2000,
        "wait_loop_walk": 20,
        "img": "ressources/monsters/poulpe_bis.gif",
        "frames_gif": 30,
        "wait_frame_animation": 5
    },
    # PLANTE_CARNIVORE
    {
        "width": 77,
        "height": 80,
        "color": "red",
        "life": 60,
        "gold": 7,
        "score": 5,
        "wait_before_new_creation": 2000,
        "wait_loop_walk": 20,
        "img": "ressources/monsters/plante_carnivore.gif",
        "frames_gif": 12,
        "wait_frame_animation": 10
    },
    # DRAGON
    {
        "width": 80,
        "height": 80,
        "color": "red",
        "life": 60,
        "gold": 7,
        "score": 5,
        "wait_before_new_creation": 1500,
        "wait_loop_walk": 20,
        "img": "ressources/monsters/dragon.gif",
        "frames_gif": 10,
        "wait_frame_animation": 4
    },
    # GARY
    {
        "width": 80,
        "height": 80,
        "color": "red",
        "life": 60,
        "gold": 7,
        "score": 5,
        "wait_before_new_creation": 2000,
        "wait_loop_walk": 10,
        "img": "ressources/monsters/gary.gif",
        "frames_gif": 40,
        "wait_frame_animation": 2
    }
]



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
