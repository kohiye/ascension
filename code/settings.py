WINDOW_WIDTH = 1280
WINDOW_HEIGTH = 720
TILE_SIZE = 64
MOUSE_HOLD_LIMIT = 50
ANIMATION_SPEED = 8
PLAYER_SPEED = 300
GRAVITY = 5

CANVAS_TEMPLATES = {
    0: {
        "name": "player",
        "ground": "mid",
        "type": "float",
        "menu": None,
        "menu_surf": None,
        "preview": None,
        "frames": "../graphics/player/static",
    },
    1: {
        "name": "wall",
        "type": "tile",
        "menu": "terrain",
        "menu_surf": "../graphics/wall/wall.png",
        "preview": "../graphics/wall/wall.png",
        "graphics": "../graphics/wall/wall.png",
        "frames": None,
    },
    2: {
        "name": "air",
        "type": "tile",
        "menu": "terrain",
        "menu_surf": "../graphics/air.png",
        "preview": "../graphics/air.png",
        "graphics": "../graphics/air.png",
        "frames": None,
    },
    3: {
        "name": "coin",
        "ground": "mid",
        "type": "tile",
        "menu": "coin",
        "menu_surf": "../graphics/coin/static/a.png",
        "preview": "../graphics/coin/coin_pre.png",
        "frames": "../graphics/coin/static",
    },
    4: {
        "name": "chair_fg",
        "ground": "fore",
        "type": "float",
        "menu": "chair fg",
        "menu_surf": "../graphics/chair/static/chair.png",
        "preview": "../graphics/chair/static/chair.png",
        "frames": "../graphics/chair/static",
    },
    5: {
        "name": "chair_bg",
        "ground": "back",
        "type": "float",
        "menu": "chair bg",
        "menu_surf": "../graphics/chair/static/chair.png",
        "preview": "../graphics/chair/static/chair.png",
        "frames": "../graphics/chair/static",
    },
    6: {
        "name": "enemy",
        "ground": "mid",
        "type": "float",
        "menu": "enemy",
        "menu_surf": "../graphics/enemy/enemy.png",
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
