"""Toutes les valeurs concernant le gameplay du jeu sont ici"""
PLAYER = {
    "GOLD": 250,
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
    "bloc_size": 80,
    "wait_frame_animation": 10,
    "waves": [
        [0, 20, 20],
        [1, 20, 50],
        [1, 30, 75],
        [2, 10, 100],
        [3, 50, 125],
        [4, 20, 150],
        [5, 1, 175],
        [6, 30, 200],
        [7, 30, 225],
        [8, 20, 250],
        [9, 40, 275]
    ],
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
                "upgrade_speed": 100
            },
            {
                "price": 100,
                "min_dead": 0,
                "upgrade_range": BLOC_SIZE * 0.2,
                "upgrade_damages": 20,
                "upgrade_speed": 100
            },
            {
                "price": 150,
                "min_dead": 20,
                "upgrade_range": BLOC_SIZE * 0.2,
                "upgrade_damages": 50,
                "upgrade_speed": 100,
                "evolution": True
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
                "min_dead": 20,
                "upgrade_range": BLOC_SIZE * 0.2,
                "upgrade_damages": 50,
                "upgrade_speed": 100,
                "evolution": True
            }
        ]
    },

    # DEFENDER ATTAQUE
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
            }
        ]
    },

    # DEFENDER GLACE
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
            }
        ]
    },

    # DEFENDER POISON
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
            }
        ]
    }
]



MONSTERS = [
    # PIEUVRE
    {
        "width": 72,
        "height": 80,
        "life": 60,
        "gold": 7,
        "score": 5,
        "wait_before_new_creation": 2500,
        "wait_loop_walk": 25,
        "img": "ressources/monsters/pieuvre.gif",
        "frames_gif": 5,
        "wait_frame_animation": 5
    },
    # BOULE
    {
        "width": 56,
        "height": 80,
        "life": 80,
        "gold": 8,
        "score": 7,
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
        "life": 400,
        "gold": 20,
        "score": 10,
        "wait_before_new_creation": 7000,
        "wait_loop_walk": 30,
        "img": "ressources/monsters/squelette.gif",
        "frames_gif": 9,
        "wait_frame_animation": 10
    },
    # CHAMPIGNON
    {
        "width": 80,
        "height": 80,
        "life": 60,
        "gold": 5,
        "score": 5,
        "wait_before_new_creation": 200,
        "wait_loop_walk": 20,
        "img": "ressources/monsters/champignon.gif",
        "frames_gif": 8,
        "wait_frame_animation": 5
    },
    # CHEVALIER
    {
        "width": 77,
        "height": 80,
        "life": 600,
        "gold": 40,
        "score": 15,
        "wait_before_new_creation": 3000,
        "wait_loop_walk": 20,
        "img": "ressources/monsters/chevalier.gif",
        "frames_gif": 5,
        "wait_frame_animation": 10
    },
    # CYCLOPE
    {
        "width": 80,
        "height": 80,
        "life": 10000,
        "gold": 500,
        "score": 100,
        "wait_before_new_creation": 2000,
        "wait_loop_walk": 100,
        "img": "ressources/monsters/cyclope.gif",
        "frames_gif": 6,
        "wait_frame_animation": 7
    },
    # POULPE_BIS
    {
        "width": 80,
        "height": 80,
        "life": 500,
        "gold": 40,
        "score": 20,
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
        "life": 1000,
        "gold": 30,
        "score": 30,
        "wait_before_new_creation": 3000,
        "wait_loop_walk": 30,
        "img": "ressources/monsters/plante_carnivore.gif",
        "frames_gif": 12,
        "wait_frame_animation": 10
    },
    # DRAGON
    {
        "width": 80,
        "height": 80,
        "life": 500,
        "gold": 20,
        "score": 40,
        "wait_before_new_creation": 1000,
        "wait_loop_walk": 20,
        "img": "ressources/monsters/dragon.gif",
        "frames_gif": 10,
        "wait_frame_animation": 4
    },
    # GARY
    {
        "width": 80,
        "height": 80,
        "life": 1000,
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
