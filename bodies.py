"""Créateur des corps des différentes entitées du jeu"""

def body_creation_defender(code, canvas, item):
    """Créateur du corps des defenders"""
    if code in (0, 1):
        return [
            canvas.create_rectangle(
                item.pos_x + item.width / 4,
                item.pos_y,
                item.pos_x + 3 * item.width / 4,
                item.pos_y + item.height / 4,
                fill=item.color
            ),
            canvas.create_rectangle(
                item.pos_x + item.width/ 8,
                item.pos_y + item.height / 4,
                item.pos_x + 7 * item.width / 8,
                item.pos_y + item.height,
                fill=item.color
            ),
            canvas.create_rectangle(
                item.pos_x,
                item.pos_y + 3 * item.height / 8,
                item.pos_x + item.width / 8,
                item.pos_y + item.height,
                fill=item.color
            ),
            canvas.create_rectangle(
                item.pos_x + 7 * item.width / 8,
                item.pos_y + 3 * item.height / 8,
                item.pos_x + item.width,
                item.pos_y + item.height,
                fill=item.color
            )
        ]
    return None


def body_creation_monster(code, canvas, item):
    """Créateur du corps des monstres"""
    if code in (0, 1, 2):
        return [
            upgrade_life(canvas, item),
            canvas.create_rectangle(
                item.pos_x,
                item.pos_y - 10,
                item.pos_x + item.width,
                item.pos_y - 5
            ),
            canvas.create_rectangle(
                item.pos_x + item.width / 4,
                item.pos_y,
                item.pos_x + 3 * item.width / 4,
                item.pos_y + item.height / 4,
                fill=item.color
            ),
            canvas.create_rectangle(
                item.pos_x + item.width/ 8,
                item.pos_y + item.height / 4,
                item.pos_x + 7 * item.width / 8,
                item.pos_y + item.height,
                fill=item.color
            ),
            canvas.create_rectangle(
                item.pos_x,
                item.pos_y + 3 * item.height / 8,
                item.pos_x + item.width / 8,
                item.pos_y + item.height,
                fill=item.color
            ),
            canvas.create_rectangle(
                item.pos_x + 7 * item.width / 8,
                item.pos_y + 3 * item.height / 8,
                item.pos_x + item.width,
                item.pos_y + item.height,
                fill=item.color
            )
        ]
    return None

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
