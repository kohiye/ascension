import pygame

import settings as s


class Score:
    def __init__(self, switch):
        self.display_surface = pygame.display.get_surface()
        self.switch = switch

    def event_loop(self):
        for event in pygame.event.get():
            self.switch(event)

    def display(self, dt):
        self.event_loop()
        self.display_surface.fill("Green")
