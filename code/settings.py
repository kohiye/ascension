WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
TILE_SIZE = 64
MOUSE_HOLD_LIMIT = 50
ANIMATION_SPEED = 8
PLAYER_SPEED = 300
GRAVITY = 5
BULLET_SPEED = 500
BULLET_LIFE_TIME_MS = 10000
CAMERA_Y_SHIFT = 50
ENEMY_PLAYER_REPULSION = 400
PLAYER_DOOR_SPAWN_DISTANCE = 70
VOLUME = 0.1

CANVAS_TEMPLATES = {
    0: {
        "name": "player",
        "ground": "mid",
        "type": "float",
        "menu": None,
        "preview": None,
        "frames": "../graphics/player/static",
    },
    1: {
        "name": "wall",
        "type": "tile",
        "menu": "wall",
        "preview": "../graphics/wall/X.png",
        "graphics": "../graphics/wall/wall.png",
        "frames": None,
    },
    2: {
        "name": "air",
        "type": "tile",
        "menu": "wall",
        "preview": "../graphics/air.png",
        "graphics": "../graphics/air.png",
        "frames": None,
    },
    3: {
        "name": "coin",
        "ground": "mid",
        "type": "tile",
        "menu": "coin",
        "preview": "../graphics/coin/coin_pre.png",
        "frames": "../graphics/coin/static",
    },
    4: {
        "name": "chairR_fg",
        "ground": "fore",
        "type": "float",
        "menu": "environment fg",
        "preview": "../graphics/chairR/static/chairR.png",
        "frames": "../graphics/chairR/static",
    },
    5: {
        "name": "chairR_bg",
        "ground": "back",
        "type": "float",
        "menu": "environment bg",
        "preview": "../graphics/chairR/chairR_pre.png",
        "frames": "../graphics/chairR/static",
    },
    6: {
        "name": "chairL_fg",
        "ground": "fore",
        "type": "float",
        "menu": "environment fg",
        "preview": "../graphics/chairL/static/chairL.png",
        "frames": "../graphics/chairL/static",
    },
    7: {
        "name": "chairL_bg",
        "ground": "back",
        "type": "float",
        "menu": "environment bg",
        "preview": "../graphics/chairL/static/chairL.png",
        "frames": "../graphics/chairL/static",
    },
    8: {
        "name": "table_fg",
        "ground": "fore",
        "type": "float",
        "menu": "environment fg",
        "preview": "../graphics/table/static/table.png",
        "frames": "../graphics/table/static",
    },
    9: {
        "name": "table_bg",
        "ground": "back",
        "type": "float",
        "menu": "environment bg",
        "preview": "../graphics/table/static/table.png",
        "frames": "../graphics/table/static",
    },
    10: {
        "name": "box_fg",
        "ground": "fore",
        "type": "float",
        "menu": "environment fg",
        "preview": "../graphics/box/static/box.png",
        "frames": "../graphics/box/static",
    },
    11: {
        "name": "box_bg",
        "ground": "back",
        "type": "float",
        "menu": "environment bg",
        "preview": "../graphics/box/static/box.png",
        "frames": "../graphics/box/static",
    },
    12: {
        "name": "enemy",
        "ground": "mid",
        "type": "float",
        "menu": "enemy",
        "preview": "../graphics/enemy/static/pixil-frame-0.png",
        "frames": "../graphics/enemy/static/",
    },
    13: {
        "name": "ai_node",
        "ground": "fore",
        "type": "float",
        "menu": "enemy",
        "preview": "../graphics/node/node.png",
        "frames": "../graphics/node",
    },
    14: {
        "name": "entrance",
        "ground": "back",
        "type": "float",
        "menu": None,
        "preview": None,
        "frames": "../graphics/entrance",
    },
    15: {
        "name": "exit",
        "ground": "back",
        "type": "float",
        "menu": None,
        "preview": None,
        "frames": "../graphics/exit",
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
