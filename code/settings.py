WINDOW_WIDTH = 1280
WINDOW_HEIGTH = 720
TILE_SIZE = 64
MOUSE_HOLD_LIMIT = 50
ANIMATION_SPEED = 8

CANVAS_TEMPLATES = {
    0: {
        "name": "wall",
        "type": "tile",
        "frames": None,
        "preview": "../graphics/wall_pre.png",
        "graphics": "../graphics/wall.jpg",
    },
    1: {
        "name": "player",
        "type": "float",
        "preview": "../graphics/player/player_pre.png",
        "frames": "../graphics/player/static",
    },
    2: {
        "name": "coin",
        "type": "tile",
        "preview": "../graphics/coin/coin_pre.png",
        "frames": "../graphics/coin/static",
    },
    3: {
        "name": "chair",
        "type": "float",
        "preview": "../graphics/chair/chair_pre.png",
        "frames": "../graphics/chair/static",
    },
}
