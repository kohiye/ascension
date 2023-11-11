import pygame
import sys
from pygame.math import Vector2 as vector
from pygame.mouse import get_pressed as mouse_buttons
from pygame.mouse import get_pos as mouse_pos

from menu import Menu
import settings as s


class Editor:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.menu = Menu()

        self.origin = vector((s.WINDOW_WIDTH // 2, s.WINDOW_HEIGTH // 2))
        self.pan_mode = False
        self.pan_offset = vector()
        self.mode = 1

        self.guide_surf = pygame.Surface((s.WINDOW_WIDTH, s.WINDOW_WIDTH))
        self.guide_surf.set_colorkey("green")

        # canvas stuff:
        self.canvas_data = {}
        self.last_cell = None

    def event_loop(self):
        for event in pygame.event.get():
            self.mode_switch(event)
            self.pan_movement(event)
            self.canvas_add()

    def mode_switch(self, event):
        if event.type == pygame.QUIT:
            self.mode = 0
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.mode = 0

    def get_current_cell(self):
        temp_vect = (vector(mouse_pos()) - self.origin) // s.TILE_SIZE
        return (temp_vect.x, temp_vect.y)

    def pan_movement(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and mouse_buttons()[1]:
            self.pan_mode = True
            self.pan_offset = vector(mouse_pos()) - self.origin
        if not mouse_buttons()[1]:
            self.pan_mode = False
        if self.pan_mode:
            self.origin = vector(mouse_pos()) - self.pan_offset

    def canvas_add(self):
        if mouse_buttons()[2]:
            current_cell = self.get_current_cell()

            if current_cell != self.last_cell:
                if current_cell in self.canvas_data:
                    pass
                else:
                    self.canvas_data[current_cell] = "occupied"
                self.last_cell = current_cell
                print(self.canvas_data)

    def draw_tile_guides(self):
        cols = s.WINDOW_WIDTH // s.TILE_SIZE
        rows = s.WINDOW_HEIGTH // s.TILE_SIZE

        origin_offset = vector(self.origin.x % s.TILE_SIZE, self.origin.y % s.TILE_SIZE)

        self.guide_surf.fill("green")

        for col in range(cols + 1):
            x = origin_offset.x + col * s.TILE_SIZE
            pygame.draw.line(self.guide_surf, "gray", (x, 0), (x, s.WINDOW_HEIGTH))

        for row in range(rows + 1):
            y = origin_offset.y + row * s.TILE_SIZE
            pygame.draw.line(self.guide_surf, "gray", (0, y), (s.WINDOW_WIDTH, y))

        self.display_surface.blit(self.guide_surf, (0, 0))

    def run(self, dt):
        self.event_loop()
        self.display_surface.fill("white")
        self.draw_tile_guides()
        pygame.draw.circle(self.display_surface, "red", self.origin, 30)
        self.menu.display()
        return self.mode
