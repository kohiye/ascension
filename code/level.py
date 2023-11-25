import pygame
import sys


class Level:
    def __init__(self, switch):
        self.display_surface = pygame.display.get_surface()
        self.switch = switch

    def event_loop(self):
        for event in pygame.event.get():
            self.switch(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def run(self, dt):
        self.event_loop()
        self.display_surface.fill("red")
