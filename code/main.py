import pygame
import sys

from editor import Editor
from level import Level
import settings as s


class Main:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode(
            (s.WINDOW_WIDTH, s.WINDOW_HEIGTH)
        )
        self.clock = pygame.time.Clock()
        self.editor = Editor(self.switch)
        self.level = Level(self.switch)

        self.mode = 1

    def switch(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.mode = 0
            elif event.key == pygame.K_RETURN:
                self.mode = 2

    def run(self):
        while True:
            dt = self.clock.tick() / 1000
            match self.mode:
                case 0:
                    pygame.quit()
                    sys.exit()
                case 1:
                    self.editor.run(dt)
                case 2:
                    self.level.run(dt)
            pygame.display.update()


if __name__ == "__main__":
    main = Main()
    main.run()
