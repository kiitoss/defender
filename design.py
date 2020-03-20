"""Créateur des corps des différentes entitées du jeu"""
import random

def rgb_traductor(rgb):
    """transforme rgb en couleur compréhensible par tkinter"""
    return "#%02x%02x%02x" % rgb
def bleu_clair():
    """retourn la couleur bleu clair"""
    return rgb_traductor((0, 126, 254))
def bleu_fonce():
    """retourn la couleur bleu foncé"""
    return rgb_traductor((0, 10, 244))
def marron():
    """retourn la couleur marron"""
    return rgb_traductor((111, 82, 48))
def jaune():
    """retourn la couleur jaune"""
    return rgb_traductor((254, 211, 48))
def orange():
    """retourn la couleur orange"""
    return rgb_traductor((254, 163, 48))
def rouge():
    """retourn la couleur orange"""
    return rgb_traductor((254, 17, 48))
def noir():
    """retourn la couleur noir"""
    return "black"
def blanc():
    """retourn la couleur blanc"""
    return "white"
def beige():
    """retourn la couleur beige"""
    return rgb_traductor((249, 192, 141))
def grey():
    """retourn la couleur gris"""
    return "grey"
def green():
    """retourn la couleur vert"""
    return "green"

def draw_bloc(code, canvas, size, x_origin, y_origin):
    """Dessine les blocs du terrain"""
    bloc_pixel = []
    all_colors = {
        "classic_bloc": [rgb_traductor((78, 175, 0)), rgb_traductor((91, 155, 1))],
        "locked_bloc": [rgb_traductor((242, 201, 1)), "black"]
    }
    if code == 0:
        bloc = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]
        list_colors = all_colors.get("classic_bloc")
    elif code == "x":
        bloc = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 0, 0, 0, 0, 1, 1, 1],
            [1, 1, 1, 1, 0, 0, 1, 1, 1, 1],
            [1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
            [1, 0, 0, 1, 0, 0, 1, 0, 0, 1],
            [1, 0, 0, 1, 0, 0, 1, 0, 0, 1],
            [1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
            [1, 1, 1, 1, 0, 0, 1, 1, 1, 1],
            [1, 1, 1, 0, 0, 0, 0, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]
        list_colors = all_colors.get("locked_bloc")

    pixel_size = size / len(bloc)

    if len(bloc) != len(bloc[0]):
        return []


    for pos_y, line in enumerate(bloc):
        for pos_x, value in enumerate(line):
            if code == 0:
                color = list_colors[random.randrange(len(list_colors))]
            else:
                color = list_colors[value]
            bloc_pixel.append(
                canvas.create_rectangle(
                    x_origin + pos_x * pixel_size,
                    y_origin + pos_y * pixel_size,
                    x_origin + (pos_x+1) * pixel_size,
                    y_origin + (pos_y+1) * pixel_size,
                    fill=color,
                    outline=""
                )
            )
    return bloc_pixel

def body_creation_defender(canvas, item, code=None):
    """Créateur du corps des defenders"""
    my_defender = []
    patron = DEFENDERS.get("classique")
    pixel_size = item.width / len(patron[0])
    if code is None:
        code = item.code

    if code == 0:
        list_colors = COLORS_DEFENDERS.get("grey")
    elif code == 1:
        list_colors = COLORS_DEFENDERS.get("red")
    elif code == 2:
        list_colors = COLORS_DEFENDERS.get("blue")
    elif code == 3:
        list_colors = COLORS_DEFENDERS.get("green")
    else:
        return []

    for pos_y, line in enumerate(patron):
        for pos_x, value in enumerate(line):
            my_defender.append(
                canvas.create_rectangle(
                    item.pos_x + pos_x * pixel_size,
                    item.pos_y + pos_y * pixel_size,
                    item.pos_x + (pos_x+1) * pixel_size,
                    item.pos_y + (pos_y+1) * pixel_size,
                    fill=list_colors[value],
                    outline=""
                )
            )
    return my_defender

def upgrade_life(canvas, item):
    """Mise à jour de la jauge de vie des enemies"""
    if item.life <= item.max_life / 3:
        color = "red"
    elif item.life <= item.max_life / 2:
        color = "orange"
    else:
        color = "green"

    return canvas.create_rectangle(
                item.pos_x,
                item.pos_y - 10,
                item.pos_x + item.width * item.life / item.max_life,
                item.pos_y - 5,
                fill=color
                )


DEFENDERS = {
    "classique": [
        [0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 1, 1, 1, 2, 0, 1, 0, 0],
        [0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 2, 0, 0, 0, 2, 0],
        [6, 0, 0, 6, 0, 0, 0, 0, 0, 0, 1, 1, 1, 2, 2, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 0, 0, 0, 0, 0],
        [0, 6, 6, 6, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 0, 0, 0, 0],
        [4, 6, 4, 6, 4, 0, 0, 0, 7, 7, 4, 4, 7, 7, 7, 7, 0, 0, 0, 0],
        [0, 4, 4, 4, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 0, 0],
        [0, 0, 5, 0, 0, 0, 0, 8, 9, 9, 9, 9, 9, 9, 9, 9, 8, 0, 0, 0],
        [0, 0, 3, 0, 0, 0, 0, 8, 7, 9, 9, 9, 9, 9, 7, 9, 8, 0, 0, 0],
        [0, 0, 3, 0, 0, 0, 0, 8, 9, 9, 9, 9, 9, 9, 9, 9, 8, 0, 0, 0],
        [0, 0, 3, 0, 0, 0, 0, 8, 9, 9, 9, 9, 9, 9, 9, 9, 8, 0, 0, 0],
        [0, 0, 3, 0, 0, 0, 0, 8, 9, 9, 9, 9, 9, 9, 9, 8, 8, 1, 0, 0],
        [0, 0, 3, 0, 0, 0, 0, 8, 9, 9, 8, 8, 9, 9, 9, 8, 8, 1, 1, 0],
        [0, 0, 3, 0, 0, 0, 0, 8, 9, 8, 9, 9, 8, 9, 8, 8, 2, 1, 1, 1],
        [0, 0, 3, 0, 0, 0, 0, 8, 8, 8, 8, 8, 8, 8, 8, 2, 1, 2, 1, 1],
        [0, 9, 9, 1, 1, 1, 1, 8, 8, 8, 8, 8, 8, 8, 2, 1, 1, 2, 1, 1],
        [0, 9, 9, 1, 2, 2, 2, 2, 8, 8, 8, 8, 8, 2, 1, 1, 1, 2, 1, 1],
        [0, 0, 3, 0, 0, 0, 0, 0, 8, 8, 8, 8, 2, 1, 1, 1, 1, 2, 1, 1],
        [0, 0, 3, 0, 0, 0, 0, 0, 2, 8, 8, 2, 2, 1, 1, 1, 1, 2, 1, 1],
        [0, 0, 3, 0, 0, 0, 0, 0, 2, 8, 2, 1, 2, 1, 1, 1, 1, 2, 9, 9],
        [0, 0, 3, 0, 0, 0, 0, 0, 2, 1, 2, 1, 2, 1, 1, 1, 1, 2, 9, 9],
        [0, 0, 3, 0, 0, 0, 0, 0, 2, 1, 1, 1, 2, 1, 1, 1, 1, 2, 2, 0],
        [0, 0, 3, 0, 0, 0, 0, 0, 2, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 3, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        [0, 0, 3, 0, 0, 0, 0, 0, 3, 3, 3, 3, 0, 0, 0, 3, 3, 3, 3, 0]
    ]
}

COLORS_DEFENDERS = {
    "grey": [
        "",
        grey(),
        grey(),
        marron(),
        grey(),
        grey(),
        grey(),
        noir(),
        blanc(),
        beige()
    ],
    "blue": [
        "",
        bleu_clair(),
        bleu_fonce(),
        marron(),
        jaune(),
        orange(),
        rouge(),
        noir(),
        blanc(),
        beige()
    ],
    "red": [
        "",
        rouge(),
        rouge(),
        marron(),
        jaune(),
        bleu_fonce(),
        bleu_clair(),
        noir(),
        blanc(),
        beige()
    ],
    "yellow": [
        "",
        jaune(),
        jaune(),
        marron(),
        bleu_fonce(),
        rouge(),
        rouge(),
        noir(),
        blanc(),
        beige()
    ],
    "green": [
        "",
        green(),
        green(),
        marron(),
        green(),
        green(),
        green(),
        noir(),
        blanc(),
        beige()
    ]
}
