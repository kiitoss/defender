"""Fichier recensant les valeurs pour le gameplay du jeu sont ici"""

#Cartes du jeu:
# -1: chemin pour les enemies
# 0: case vide
# 1-9: defenseurs alliés
# 'x': case objet a demolir avant de pouvoir construire
MAPS = [
    [
        ["x", 0, 0, 0, 0, -1, 0, "x", "x", "x", "x"],
        [-1, -1, -1, -1, -1, -1, 0, "x", "x", "x", "x"],
        [-1, "x", "x", 0, 0, 0, 0, 0, 0, 0, 0],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [0, 0, 0, 0, 0, 0, 0, 0, "x", "x", -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, "x", "x", 0, 0, 0, 0, 0, 0, 0, 0],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [0, 0, 0, 0, 0, 0, 0, 0, "x", "x", -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, "x", "x", 0, 0, 0, 0, 0, 0, 0, 0]
    ],
    [
        [0, 0, 0, 0, 0, -1, 0, "x", "x", "x", "x"],
        [0, -1, -1, -1, -1, -1, 0, "x", "x", "x", "x"],
        [0, -1, "x", 0, 0, 0, 0, 0, 0, 0, 0],
        [0, -1, -1, -1, -1, -1, -1, -1, -1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, "x", -1, 0, 0],
        [0, 0, 0, -1, -1, -1, -1, -1, -1, 0, 0],
        ["x", 0, 0, -1, "x", 0, 0, 0, 0, 0, 0],
        ["x", "x", 0, -1, -1, -1, -1, 0, 0, 0, 0],
        ["x", "x", 0, 0, 0, "x", -1, 0, 0, "x", "x"],
        ["x", "x", "x", 0, 0, -1, -1, 0, 0, "x", "x"],
        ["x", "x", "x", 0, 0, -1, 0, 0, "x", "x", "x"]
    ],
    [
        [0, 0, 0, 0, "x", -1, "x", 0, 0, 0, 0],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, 0, 0, 0, "x", 0, "x", 0, 0, 0, -1],
        [-1, 0, "x", "x", 0, "x", 0, "x", "x", 0, -1],
        [-1, 0, 0, 0, "x", 0, "x", 0, 0, 0, -1],
        [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1],
        [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1],
        [-1, 0, "x", "x", 0, "x", 0, "x", "x", 0, -1],
        [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0]
    ],
    [
        ["x", 0, 0, 0, "x", -1, "x", 0, 0, 0, "x"],
        [0, 0, 0, "x", 0, -1, 0, 0, "x", 0, 0],
        [0, 0, 0, 0, "x", -1, "x", 0, 0, 0, 0],
        [0, 0, 0, "x", 0, -1, 0, "x", 0, 0, 0],
        [0, 0, "x", 0, 0, -1, 0, 0, "x", 0, 0],
        [0, "x", 0, 0, 0, -1, 0, 0, 0, "x", 0],
        ["x", 0, 0, 0, 0, -1, 0, 0, 0, 0, "x"],
        [0, "x", 0, 0, 0, -1, 0, 0, 0, "x", 0],
        [0, 0, "x", 0, 0, -1, 0, 0, "x", 0, 0],
        [0, 0, 0, "x", 0, -1, 0, "x", 0, 0, 0],
        ["x", 0, 0, 0, "x", -1, "x", 0, 0, 0, "x"]
    ]
]


# Informations concernant le joueur
PLAYER = {
    "GOLD": 250,
    "SCORE": 0,
    "LIFE": 100,
    "MONSTER_KILLED": 0
}


# Parametres de la partie
GAME_MANAGER = {
    "status_frame_option": "clean",
    "game_speed": 1,
    "game_launched": False,
    "defender_shown": None,
    "range_shown": None,
    "case_shown": None,
    "price_remove_obstacle": 2000,
    "bloc_size": 80,
    "wait_frame_animation": 10,
    "map": MAPS[0],
    "waves": [
        #monster, qty, life, money_per_monster, prime
        [0, 20, 60, 7, 25],
        [1, 15, 70, 8, 50],
        [1, 20, 70, 8, 75],
        [2, 20, 400, 10, 100],
        [3, 40, 30, 10, 125],
        [4, 15, 400, 20, 150],
        [5, 1, 2500, 500, 175],
        [6, 10, 500, 30, 200],
        [7, 30, 1000, 40, 225],
        [8, 15, 600, 45, 250],
        [5, 1, 12000, 700, 275],
        [9, 35, 1000, 50, 305]
    ],
    "waves_round": [],
    "coeff_wave": 1,
    "wave_now": 0
}


BLOC_SIZE = GAME_MANAGER.get("bloc_size")


# Caracteristiques des defenseurs
DEFENDERS = [
    # DEFENSEUR 1
    {
        "width": BLOC_SIZE / 1.35,
        "height": BLOC_SIZE,
        "damages": 20,
        "range": BLOC_SIZE * 1.5,
        "attack_speed": 1000,
        "price": 100,
        "color": "brown",
        "ability": None,
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
                "upgrade_range": BLOC_SIZE * 0.3,
                "upgrade_damages": 20,
                "upgrade_speed": 100
            },
            {
                "price": 250,
                "min_dead": 20,
                "upgrade_range": BLOC_SIZE * 0.4,
                "upgrade_damages": 50,
                "upgrade_speed": 100,
                "evolution": True
            }
        ]
    },

    # DEFENSEUR 2
    {
        "width": BLOC_SIZE / 1.35,
        "height": BLOC_SIZE,
        "damages": 50,
        "range": BLOC_SIZE * 2,
        "attack_speed": 1000,
        "price": 250,
        "color": "black",
        "ability": None,
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
                "upgrade_range": BLOC_SIZE * 0.3,
                "upgrade_damages": 20,
                "upgrade_speed": 100
            },
            {
                "price": 500,
                "min_dead": 20,
                "upgrade_range": BLOC_SIZE * 0.4,
                "upgrade_damages": 50,
                "upgrade_speed": 100,
                "evolution": True
            }
        ]
    },

    # DEFENSEUR ATTAQUE
    {
        "width": BLOC_SIZE / 1.35,
        "height": BLOC_SIZE,
        "damages": 100,
        "range": BLOC_SIZE * 2,
        "attack_speed": 800,
        "price": 500,
        "color": "red",
        "ability": "attack",
        "sell_price": 100,
        "upgrades": [
            {
                "price": 350,
                "min_dead": 0,
                "upgrade_range": BLOC_SIZE * 0.3,
                "upgrade_damages": 50,
                "upgrade_speed": 100
            },
            {
                "price": 700,
                "min_dead": 20,
                "upgrade_range": BLOC_SIZE * 0.5,
                "upgrade_damages": 150,
                "upgrade_speed": 100
            }
        ]
    },

    # DEFENSEUR GLACE
    {
        "width": BLOC_SIZE / 1.35,
        "height": BLOC_SIZE,
        "damages": 70,
        "range": BLOC_SIZE * 2,
        "attack_speed": 1000,
        "price": 500,
        "color": "blue",
        "ability": "freeze",
        "sell_price": 100,
        "upgrades": [
            {
                "price": 350,
                "min_dead": 0,
                "upgrade_range": BLOC_SIZE * 0.3,
                "upgrade_damages": 30,
                "upgrade_speed": 100
            },
            {
                "price": 700,
                "min_dead": 20,
                "upgrade_range": BLOC_SIZE * 0.5,
                "upgrade_damages": 80,
                "upgrade_speed": 100
            }
        ]
    },

    # DEFENSEUR POISON
    {
        "width": BLOC_SIZE / 1.35,
        "height": BLOC_SIZE,
        "damages": 70,
        "range": BLOC_SIZE * 2,
        "attack_speed": 1000,
        "price": 500,
        "color": "green",
        "ability": "poison",
        "sell_price": 100,
        "upgrades": [
            {
                "price": 350,
                "min_dead": 0,
                "upgrade_range": BLOC_SIZE * 0.3,
                "upgrade_damages": 30,
                "upgrade_speed": 100
            },
            {
                "price": 700,
                "min_dead": 20,
                "upgrade_range": BLOC_SIZE * 0.5,
                "upgrade_damages": 80,
                "upgrade_speed": 100
            }
        ]
    }
]


# Caracteristiques des monstres
MONSTERS = [
    # PIEUVRE
    {
        "width": 72,
        "height": 80,
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
        "score": 10,
        "wait_before_new_creation": 5000,
        "wait_loop_walk": 30,
        "img": "ressources/monsters/squelette.gif",
        "frames_gif": 9,
        "wait_frame_animation": 10
    },
    # CHAMPIGNON
    {
        "width": 80,
        "height": 80,
        "score": 15,
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
        "score": 20,
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
        "score": 30,
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
        "score": 40,
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
        "score": 50,
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
        "score": 60,
        "wait_before_new_creation": 2000,
        "wait_loop_walk": 10,
        "img": "ressources/monsters/gary.gif",
        "frames_gif": 40,
        "wait_frame_animation": 2
    }
]
