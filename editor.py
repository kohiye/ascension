import pygame
import sys
from pygame.math import Vector2 as vector
from pygame.mouse import get_pressed as mouse_buttons
from pygame.mouse import get_pos as mouse_pos


class Editor:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()

        self.origin = vector((500, 250))
        self.pan_mode = False
        self.pan_offset = vector()
        self.mode = 1

    def event_loop(self):
        for event in pygame.event.get():
            self.mode_switch(event)
            self.pan_movement(event)

    def mode_switch(self, event):
        if event.type == pygame.QUIT:
            self.mode = 0
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.mode = 0

    def pan_movement(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and mouse_buttons()[1]:
            self.pan_mode = True
            self.pan_offset = vector(mouse_pos()) - self.origin
        if not mouse_buttons()[1]:
            self.pan_mode = False
        if self.pan_mode:
            self.origin = vector(mouse_pos()) - self.pan_offset

    def run(self, dt):
        self.event_loop()
        self.display_surface.fill("white")
        pygame.draw.circle(self.display_surface, "red", self.origin, 30)
        return self.mode
