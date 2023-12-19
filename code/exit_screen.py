import pygame

import settings as s


class Score:
    def __init__(self, switch,money):
        self.display_surface = pygame.display.get_surface()
        self.switch = switch
        self.money=money

    def event_loop(self):
        for event in pygame.event.get():
            self.switch(event)

    def display(self, dt):
        self.event_loop()
        self.display_surface.fill("black")

        self.font = pygame.font.Font("../font/Pixeltype.ttf", 50)
        text = self.font.render("Level completed", True, "white")
        text_rect = text.get_rect(center=(s.WINDOW_HEIGHT // 2 + 280, s.WINDOW_WIDTH // 2 - 500))
        self.display_surface.blit(text, text_rect)

        result_text = "Your Result: " + str(self.money)
        result_text = self.font.render(result_text, True, "white")
        result_rect = result_text.get_rect(center=(s.WINDOW_HEIGHT // 2 + 280, s.WINDOW_WIDTH // 2 - 300))
        self.display_surface.blit(result_text, result_rect)

        continue_text = "Press return to continue"
        continue_text = self.font.render(continue_text, True, "white")
        continue_rect = continue_text.get_rect(center=(s.WINDOW_HEIGHT // 2 + 280, s.WINDOW_WIDTH // 2 - 100))
        self.display_surface.blit(continue_text, continue_rect)
