WINDOW_WIDTH = 1280
WINDOW_HEIGTH = 720
TILE_SIZE = 64
MOUSE_HOLD_LIMIT = 50
ANIMATION_SPEED = 8
PLAYER_SPEED = 300

CANVAS_TEMPLATES = {
    0: {
        "name": "player",
        "ground": "mid",
        "type": "float",
        "preview": None,
        "frames": "../graphics/player/static",
    },
    1: {
        "name": "wall",
        "type": "tile",
        "frames": None,
        "preview": "../graphics/wall/wall.png",
        "graphics": "../graphics/wall/wall.png",
    },
    2: {
        "name": "air",
        "type": "tile",
        "frames": None,
        "preview": "../graphics/air.png",
        "graphics": "../graphics/air.png",
    },
    3: {
        "name": "coin",
        "ground": "mid",
        "type": "tile",
        "preview": "../graphics/coin/coin_pre.png",
        "frames": "../graphics/coin/static",
    },
    4: {
        "name": "chair_fg",
        "ground": "fore",
        "type": "float",
        "preview": "../graphics/chair/static/chair.png",
        "frames": "../graphics/chair/static",
    },
    5: {
        "name": "chair_bg",
        "ground": "back",
        "type": "float",
        "preview": "../graphics/chair/static/chair.png",
        "frames": "../graphics/chair/static",
    },
    6: {
        "name": "enemy",
        "ground": "mid",
        "type": "float",
        "preview": "../graphics/enemy/enemy.png",
        "frames": "../graphics/enemy",
    },
}

WALL_DIRECTIONS = {
    "A": (0, -1),
    "B": (-1, -1),
    "C": (-1, 0),
    "D": (-1, 1),
    "E": (0, 1),
    "F": (1, 1),
    "G": (1, 0),
    "H": (1, -1),
}
