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
        "graphics": "../graphics/wall.jpg",
    },
    1: {"name": "player", "type": "float", "frames": "../graphics/player"},
    2: {"name": "coin", "type": "tile", "frames": "../graphics/coin"},
    3: {
        "name": "chair",
        "type": "float",
        "frames": None,
        "graphics": "../graphics/chair.png",
    },
}
