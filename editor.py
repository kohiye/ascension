import pygame
import sys


class Editor:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()

    def event_loop(self):
        pass

    def mode_switch(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 0

    def run(self, dt):
        self.event_loop()
        self.display_surface.fill("white")
        pygame.draw.circle(self.display_surface, "red", (500, 250), 30)
