import pygame
import sys
from pygame.math import Vector2 as vector
from pygame.mouse import get_pressed as mouse_buttons
from pygame.mouse import get_pos as mouse_pos

from menu import Menu
from support import import_dir
import settings as s
from timer import Timer


class Editor:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.menu = Menu()

        self.imports()

        self.origin = vector((s.WINDOW_WIDTH // 2, s.WINDOW_HEIGTH // 2))
        self.pan_mode = False
        self.hold_timer = Timer(200)
        self.pan_offset = vector()
        self.mode = 1

        self.guide_surf = pygame.Surface((s.WINDOW_WIDTH, s.WINDOW_WIDTH))
        self.guide_surf.set_colorkey("green")

        # canvas stuff:
        self.canvas_data = {}
        self.last_cell = None
        self.float_cooldown_timer = Timer(100)
        self.selection_id = 0

        # float stuff:
        self.canvas_floats = pygame.sprite.Group()
        self.float_drag_active = False

    def imports(self):
        self.animations = {}
        for key, value in s.CANVAS_TEMPLATES.items():
            if value["frames"]:
                frames = import_dir(value["frames"])
                self.animations[key] = {
                    "frame_index": 0,
                    "frames": frames,
                    "length": len(frames),
                }

    def animations_update(self, dt):
        for value in self.animations.values():
            value["frame_index"] += s.ANIMATION_SPEED * dt
            if value["frame_index"] >= value["length"]:
                value["frame_index"] = 0

    def event_loop(self):
        for event in pygame.event.get():
            self.hold_checker(event)
            self.mode_switch(event)
            self.pan_movement(event)
            self.float_drag(event)
            self.selection_arrows(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.canvas_add()
                self.canvas_remove()
            else:
                if not self.hold_timer.active and not self.float_cooldown_timer.active:
                    self.canvas_add()
                    self.canvas_remove()

    def hold_checker(self, event):
        if event.type == (pygame.MOUSEBUTTONDOWN or pygame.MOUSEBUTTONUP):
            self.hold_timer.deactivate()
            self.hold_timer.activate()

    def mode_switch(self, event):
        if event.type == pygame.QUIT:
            self.mode = 0
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.mode = 0

    def selection_arrows(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                self.selection_id += 1
            if event.key == pygame.K_LEFT:
                self.selection_id -= 1
        self.selection_id = max(0, min(self.selection_id, 2))

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

            for sprite in self.canvas_floats:
                sprite.pan_pos(self.origin)

    def canvas_add(self):
        if mouse_buttons()[0] and not self.float_drag_active:
            current_cell = self.get_current_cell()
            print(s.CANVAS_TEMPLATES[self.selection_id]["type"])
            if s.CANVAS_TEMPLATES[self.selection_id]["type"] == "tile":
                if current_cell != self.last_cell:
                    if current_cell in self.canvas_data:
                        self.canvas_data[current_cell].add_id(self.selection_id)
                    else:
                        self.canvas_data[current_cell] = CanvasTile(self.selection_id)

                    self.last_cell = current_cell
            if s.CANVAS_TEMPLATES[self.selection_id]["type"] == "float":
                CanvasFloat(
                    pos=mouse_pos(),
                    frames=self.animations[self.selection_id]["frames"],
                    float_id=self.selection_id,
                    origin=self.origin,
                    group=self.canvas_floats,
                )
                self.float_cooldown_timer.activate()

    def canvas_remove(self):
        if mouse_buttons()[2]:
            if self.canvas_data:
                current_cell = self.get_current_cell()
                if current_cell in self.canvas_data:
                    self.canvas_data[current_cell].remove_id(self.selection_id)
                    if self.canvas_data[current_cell].is_empty:
                        del self.canvas_data[current_cell]

    def float_drag(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and mouse_buttons()[0]:
            for sprite in self.canvas_floats:
                if sprite.rect.collidepoint(mouse_pos()):
                    self.float_drag_active = True
                    sprite.start_drag()

        if event.type == pygame.MOUSEBUTTONUP and self.float_drag_active:
            for sprite in self.canvas_floats:
                if sprite.selected:
                    sprite.end_drag(self.origin)
                    self.float_drag_active = False

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

    def draw_level(self):
        for cell_pos, tile in self.canvas_data.items():
            pos = self.origin + vector(cell_pos) * s.TILE_SIZE

            if tile.wall:
                surf = pygame.image.load(
                    s.CANVAS_TEMPLATES[0]["graphics"]
                ).convert_alpha()
                rect = surf.get_rect(topleft=pos)
                self.display_surface.blit(surf, rect)
            if tile.coin:
                frames = self.animations[tile.coin]["frames"]
                index = int(self.animations[tile.coin]["frame_index"])
                coin_surf = frames[index]
                rect = coin_surf.get_rect(
                    center=(pos.x + s.TILE_SIZE // 2, pos.y + s.TILE_SIZE // 2)
                )
                self.display_surface.blit(coin_surf, rect)

        self.canvas_floats.draw(self.display_surface)

    def run(self, dt):
        self.event_loop()

        self.animations_update(dt)
        self.canvas_floats.update(dt)
        self.hold_timer.update()
        self.float_cooldown_timer.update()

        self.display_surface.fill("white")
        self.draw_tile_guides()
        self.draw_level()
        pygame.draw.circle(self.display_surface, "red", self.origin, 5)
        self.menu.display()
        return self.mode


class CanvasTile:
    def __init__(self, tile_id):
        self.wall = False
        self.coin = None

        self.is_empty = False

        self.add_id(tile_id)

    def add_id(self, tile_id):
        match tile_id:
            case 0:
                self.wall = True
            case 2:
                self.coin = tile_id

    def remove_id(self, tile_id):
        match tile_id:
            case 0:
                self.wall = False
            case 2:
                self.coin = None
        self.check_content()

    def check_content(self):
        if not self.wall and not self.coin:
            self.is_empty = True


class CanvasFloat(pygame.sprite.Sprite):
    def __init__(self, pos, frames, float_id, origin, group):
        super().__init__(group)
        self.float_id = float_id

        self.frames = frames
        self.frame_index = 0

        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=pos)

        self.distance_to_origin = vector(self.rect.topleft) - origin
        self.selected = False
        self.mouse_offset = vector()

    def start_drag(self):
        self.selected = True
        self.mouse_offset = vector(mouse_pos()) - vector(self.rect.topleft)

    def drag(self):
        if self.selected:
            self.rect.topleft = mouse_pos() - self.mouse_offset

    def end_drag(self, origin):
        self.selected = False
        self.distance_to_origin = vector(self.rect.topleft) - origin

    def animate(self, dt):
        self.frame_index += s.ANIMATION_SPEED * dt
        if self.frame_index > len(self.frames):
            self.frame_index = 0
        temp_index = int(self.frame_index)
        self.image = self.frames[temp_index]
        self.rect = self.image.get_rect(midbottom=self.rect.midbottom)

    def pan_pos(self, origin):
        self.rect.topleft = origin + self.distance_to_origin

    def update(self, dt):
        self.animate(dt)
        self.drag()
