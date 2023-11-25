import pygame

import settings as s


class Menu:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.test_menu_surf = pygame.surface.Surface((100, 100))
        self.test_menu_surf.fill("blue")
        self.test_menu_rect = self.test_menu_surf.get_rect(
            midleft=(0, s.WINDOW_HEIGTH // 2)
        )

    def display(self):
        self.display_surface.blit(self.test_menu_surf, self.test_menu_rect)
