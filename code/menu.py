import pygame

import settings as s


class Menu:
    def __init__(self, switch):
        self.display_surface = pygame.display.get_surface()
        self.switch = switch

        self.buttons = pygame.sprite.Group()
        Button(
            pygame.Rect(s.WINDOW_WIDTH // 2 - 50, s.WINDOW_HEIGTH // 2 - 50, 100, 100),
            self.buttons,
        )

    def event_loop(self):
        for event in pygame.event.get():
            self.switch(event)

    def display(self, dt):
        self.event_loop()
        self.display_surface.fill("pink")
        self.buttons.draw(self.display_surface)


class Button(pygame.sprite.Sprite):
    def __init__(self, rect, group):
        super().__init__(group)
        self.image = pygame.Surface(rect.size)
        self.rect = rect

    def update(self):
        self.image.fill("blue")
