import pygame
import sys

from editor import Editor
import settings as s


class Main:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode(
            (s.WINDOW_WIDTH, s.WINDOW_HEIGTH)
        )
        self.clock = pygame.time.Clock()
        self.editor = Editor()

        self.mode = 1

    def run(self):
        while True:
            dt = self.clock.tick() / 1000
            match self.mode:
                case 0:
                    pygame.quit()
                    sys.exit()
                case 1:
                    self.mode = self.editor.run(dt)
            pygame.display.update()


if __name__ == "__main__":
    main = Main()
    main.run()
