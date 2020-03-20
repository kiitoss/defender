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
    "wave_running": 0,
    "price_remove_obstacle": 2000,
    "wave_size": 20,
    "bloc_size": 80,
    "wait_frame_animation": 10
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
