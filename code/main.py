import pygame
import sys

from pygame.image import load

from editor import Editor
from level import Level
from menu import Menu
from exit_screen import Score
from death_screen import Result

import settings as s
from support import import_dir, import_dir_dict


class Main:
    def __init__(self):
        pygame.init()
        pygame.mixer.set_num_channels(30)
        self.display_surface = pygame.display.set_mode(
            (s.WINDOW_WIDTH, s.WINDOW_HEIGHT)
        )
        self.clock = pygame.time.Clock()

        self.imports()

        self.menu = Menu(self.switch)
        self.editor = Editor(self.wall_tiles, self.switch)

        self.mode = 0

    def imports(self):
        self.wall_tiles = import_dir_dict("../graphics/wall")
        self.air_surf = load("../graphics/air.png").convert_alpha()
        self.coin_frames = import_dir("../graphics/coin/static")
        self.chairR_fg = load("../graphics/chairR/static/chairR.png").convert_alpha()
        self.chairR_bg = load("../graphics/chairR/static/chairR.png").convert_alpha()
        self.chairL_fg = load("../graphics/chairL/static/chairL.png").convert_alpha()
        self.chairL_bg = load("../graphics/chairL/static/chairL.png").convert_alpha()
        self.box_fg = load("../graphics/box/static/box.png").convert_alpha()
        self.box_bg = load("../graphics/box/static/box.png").convert_alpha()
        self.table_fg = load("../graphics/table/static/table.png").convert_alpha()
        self.table_bg = load("../graphics/table/static/table.png").convert_alpha()
        self.exit = load("../graphics/exit/exit.png").convert_alpha()
        self.entrance = load("../graphics/entrance/entrance.png").convert_alpha()

    def main_menu_click(self):
        id = self.menu.click()
        if id and self.mode == 0:
            if id == "exit":
                pygame.quit()
                sys.exit()

            elif id == "editor":
                self.mode = 1

    def switch(self, event, lvl_data=None, money=None):
        if event == "lvl_exit":
            self.exit_screen = Score(self.switch, money)
            self.mode = 3
        elif event == "death":
            self.death_screen = Result(self.switch, money)
            self.mode = 4
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if self.mode == 0:
                    pygame.quit()
                    sys.exit()
                self.mode = 0
            elif event.key == pygame.K_RETURN:
                if self.mode in [0, 2, 3, 4]:
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
                            "chairR_fg": self.chairR_fg,
                            "chairR_bg": self.chairR_bg,
                            "chairL_fg": self.chairL_fg,
                            "chairL_bg": self.chairL_bg,
                            "table_fg": self.table_fg,
                            "table_bg": self.table_bg,
                            "box_fg" : self.box_fg,
                            "box_bg" : self.box_bg,
                            "exit": self.exit,
                            "entrance": self.entrance,
                        },
                    )

    def run(self):
        while True:
            self.main_menu_click()
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
                case 4:
                    self.death_screen.display(dt)
            pygame.display.update()


if __name__ == "__main__":
    main = Main()
    main.run()
