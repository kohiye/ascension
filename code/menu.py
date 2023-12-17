import pygame
from pygame.mouse import get_pressed as mouse_buttons
from pygame.mouse import get_pos as mouse_pos

import settings as s


class Menu:
    def __init__(self, switch):
        self.menu = pygame.image.load("../graphics/menu.png").convert_alpha()
        self.display_surface = pygame.display.get_surface()
        self.switch = switch
        self.font = pygame.font.Font("../font/Pixeltype.ttf", 50)
        self.exit_text_surf = self.font.render("     QUIT", False, "black")
        self.editor_text_surf = self.font.render("   Editor", False, "black")

        self.buttons = pygame.sprite.Group()
        Button(
            self.exit_text_surf,
            pygame.Rect(
                s.WINDOW_WIDTH // 2 - 100, s.WINDOW_HEIGHT // 2 - 50 + 150, 200, 100
            ),
            self.buttons,
            "exit",
        )
        Button(
            self.editor_text_surf,
            pygame.Rect(
                s.WINDOW_WIDTH // 2 - 100, s.WINDOW_HEIGHT // 2 - 50 - 150, 200, 100
            ),
            self.buttons,
            "editor",
        )

    def click(self):
        for sprite in self.buttons:
            if sprite.rect.collidepoint(mouse_pos()):
                if mouse_buttons()[0]:
                    return sprite.id
                else:
                    return None

    def event_loop(self):
        for event in pygame.event.get():
            self.switch(event)

    def display(self, dt):
        self.event_loop()
        self.display_surface.blit(self.menu,(0,0))
        self.buttons.draw(self.display_surface)


class Button(pygame.sprite.Sprite):
    def __init__(self, surf, rect, group, id):
        super().__init__(group)
        self.image = pygame.Surface((175, 75))
        self.image.fill(s.GREEN)
        self.image.blit(surf, (25, 25))
        self.rect = rect
        self.id = id

    def update(self):
        self.image.fill("blue")
