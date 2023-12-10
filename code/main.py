import pygame
import sys

from pygame.image import load

from editor import Editor
from level import Level
from menu import Menu
from exit_screen import Score

import settings as s
from support import import_dir, import_dir_dict


class Main:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode(
            (s.WINDOW_WIDTH, s.WINDOW_HEIGHT)
        )
        self.clock = pygame.time.Clock()

        self.imports()

        self.menu = Menu(self.switch)
        self.exit_screen = Score(self.switch)
        self.editor = Editor(self.wall_tiles, self.switch)

        self.mode = 1

    def imports(self):
        self.wall_tiles = import_dir_dict("../graphics/wall")
        self.air_surf = load("../graphics/air.png").convert_alpha()
        self.coin_frames = import_dir("../graphics/coin/static")
        self.chair_fg = load("../graphics/chair/static/chair.png").convert_alpha()
        self.chair_bg = load("../graphics/chair/static/chair.png").convert_alpha()
        self.exit = load("../graphics/exit/exit.png").convert_alpha()
        self.entrance = load("../graphics/entrance/entrance.png").convert_alpha()

    def switch(self, event, lvl_data=None):
        if event == "lvl_exit":
            self.mode = 3
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if self.mode == 0:
                    pygame.quit()
                    sys.exit()
                self.mode = 0
            elif event.key == pygame.K_RETURN:
                if self.mode == (0 or 2 or 3):
                    self.mode = 1
                elif self.mode == 1:
                    self.mode = 2
                    self.level = Level(
                        lvl_data,
                        self.switch,
                        {
                            "walls": self.wall_tiles,
                            "air": self.air_surf,
                            "coin": self.coin_frames,
                            "chair_fg": self.chair_fg,
                            "chair_bg": self.chair_bg,
                            "exit": self.exit,
                            "entrance": self.entrance,
                        },
                    )

    def run(self):
        while True:
            dt = self.clock.tick() / 1000
            match self.mode:
                case 0:
                    self.menu.display(dt)
                case 1:
                    self.editor.run(dt)
                case 2:
                    self.level.run(dt)
                case 3:
                    self.exit_screen.display(dt)
            pygame.display.update()


if __name__ == "__main__":
    main = Main()
    main.run()
