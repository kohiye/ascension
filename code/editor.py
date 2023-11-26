import pygame
import sys
import pickle

from pygame.math import Vector2 as vector
from pygame.mouse import get_pressed as mouse_buttons
from pygame.mouse import get_pos as mouse_pos
from pygame.image import load

from editorMenu import Menu
from support import import_dir, import_dir_dict
import settings as s
from timer import Timer


class Editor:
    def __init__(self, switch):
        self.display_surface = pygame.display.get_surface()
        self.menu = Menu()
        self.switch = switch

        self.imports()
        self.export_name = "../saves/level.pickle"

        self.origin = vector((s.WINDOW_WIDTH // 2, s.WINDOW_HEIGTH // 2))
        self.pan_mode = False
        self.hold_timer = Timer(200)
        self.pan_offset = vector()

        self.guide_surf = pygame.Surface((s.WINDOW_WIDTH, s.WINDOW_WIDTH))
        self.guide_surf.set_colorkey("green")

        # canvas stuff:
        self.canvas_data = {}
        self.last_cell = None
        self.float_cooldown_timer = Timer(100)
        self.selection_id = 1

        # float stuff:
        self.canvas_floats = pygame.sprite.Group()
        self.canvas_foregroud = pygame.sprite.Group()
        self.canvas_midground = pygame.sprite.Group()
        self.canvas_backgroud = pygame.sprite.Group()
        self.float_drag_active = False

        # player
        CanvasFloat(
            pos=(400, s.WINDOW_HEIGTH // 2),
            frames=self.animations[0]["frames"],
            float_id=0,
            origin=self.origin,
            groups=[self.canvas_floats, self.canvas_midground],
        )

    def imports(self):
        # tiles
        self.wall_tiles = import_dir_dict("../graphics/wall")
        self.air_surf = load("../graphics/air.png").convert_alpha()

        # animations
        self.animations = {}
        for key, value in s.CANVAS_TEMPLATES.items():
            if value["frames"]:
                frames = import_dir(value["frames"])
                self.animations[key] = {
                    "frame_index": 0,
                    "frames": frames,
                    "length": len(frames),
                }
        # preview
        self.preview_surfs = {
            key: load(value["preview"]).convert_alpha()
            for key, value in s.CANVAS_TEMPLATES.items()
            if value["preview"]
        }

    def export_level(self):
        # pin floats to tiles
        for tile in self.canvas_data.values():
            tile.pinned_floats = []

        for sprite in self.canvas_floats:
            current_cell = self.get_current_cell(sprite.rect.topleft)
            offset = sprite.distance_to_origin - vector(current_cell) * s.TILE_SIZE

            if current_cell in self.canvas_data:
                self.canvas_data[current_cell].add_id(sprite.float_id, offset)
            else:
                self.canvas_data[current_cell] = CanvasTile(sprite.float_id, offset)

        # pickle me this( converting lvl into a pickle)
        layers = {
            "walls": {},
            "foreground": {},
            "background": {},
            "midground": {},
            "coins": {},
        }

        for tile_pos, tile in self.canvas_data.items():
            x = tile_pos[0] * s.TILE_SIZE
            y = tile_pos[1] * s.TILE_SIZE

            if tile.wall:
                layers["walls"][(x, y)] = (
                    tile.get_wall_name()
                    if tile.get_wall_name() in self.wall_tiles
                    else "X"
                )
            if tile.coin:
                layers["coins"][
                    (x + s.TILE_SIZE // 2, y + s.TILE_SIZE // 2)
                ] = tile.coin

            if tile.pinned_floats:
                for float_id, offset in tile.pinned_floats:
                    if s.CANVAS_TEMPLATES[float_id]["ground"] == "mid":
                        layers["midground"][
                            (int(x + offset.x), int(y + offset.y))
                        ] = float_id
                    elif s.CANVAS_TEMPLATES[float_id]["ground"] == "fore":
                        layers["foreground"][
                            (int(x + offset.x), int(y + offset.y))
                        ] = float_id
                    else:
                        layers["background"][
                            (int(x + offset.x), int(y + offset.y))
                        ] = float_id

        with open(self.export_name, "wb") as f:
            pickle.dump(layers, f)

    def check_border(self, cell_pos):
        cluster = []
        for col in range(3):
            for row in range(3):
                neighbor = (col + cell_pos[0] - 1, row + cell_pos[1] - 1)
                cluster.append(neighbor)

        for cell in cluster:
            if cell in self.canvas_data and self.canvas_data[cell].wall:
                self.canvas_data[cell].wall_neighbors = []
                for name, place in s.WALL_DIRECTIONS.items():
                    neighbor_cell = (cell[0] + place[0], cell[1] + place[1])

                    if neighbor_cell in self.canvas_data:
                        if self.canvas_data[neighbor_cell].air:
                            self.canvas_data[cell].wall_neighbors.append(name)

    def animations_update(self, dt):
        for value in self.animations.values():
            value["frame_index"] += s.ANIMATION_SPEED * dt
            if value["frame_index"] >= value["length"]:
                value["frame_index"] = 0

    def event_loop(self):
        for event in pygame.event.get():
            self.hold_checker(event)
            self.switch(event)
            self.pan_movement(event)
            self.float_drag(event)
            self.selection_arrows(event)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.export_level()

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

    def selection_arrows(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                self.selection_id += 1
            if event.key == pygame.K_LEFT:
                self.selection_id -= 1
        self.selection_id = max(1, min(self.selection_id, len(s.CANVAS_TEMPLATES) - 1))

    def get_current_cell(self, pos):
        temp_vect = (vector(pos) - self.origin) // s.TILE_SIZE
        return (temp_vect.x, temp_vect.y)

    def mouse_on_float(self):
        for sprite in self.canvas_floats:
            if sprite.rect.collidepoint(mouse_pos()):
                return sprite

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
            current_cell = self.get_current_cell(mouse_pos())
            if s.CANVAS_TEMPLATES[self.selection_id]["type"] == "tile":
                if current_cell != self.last_cell:
                    if current_cell in self.canvas_data:
                        self.canvas_data[current_cell].add_id(self.selection_id)
                        if self.canvas_data[current_cell].is_empty:
                            del self.canvas_data[current_cell]
                    else:
                        self.canvas_data[current_cell] = CanvasTile(self.selection_id)

                    self.check_border(current_cell)
                    self.last_cell = current_cell
            if s.CANVAS_TEMPLATES[self.selection_id]["type"] == "float":
                if s.CANVAS_TEMPLATES[self.selection_id]["ground"] == "fore":
                    groups = [self.canvas_floats, self.canvas_foregroud]
                elif s.CANVAS_TEMPLATES[self.selection_id]["ground"] == "mid":
                    groups = [self.canvas_floats, self.canvas_midground]
                else:
                    groups = [self.canvas_floats, self.canvas_backgroud]

                CanvasFloat(
                    pos=mouse_pos(),
                    frames=self.animations[self.selection_id]["frames"],
                    float_id=self.selection_id,
                    origin=self.origin,
                    groups=groups,
                )
                self.float_cooldown_timer.activate()

    def canvas_remove(self):
        if mouse_buttons()[2]:
            if self.canvas_data:
                current_cell = self.get_current_cell(mouse_pos())
                if current_cell in self.canvas_data:
                    self.canvas_data[current_cell].remove_id(self.selection_id)
                    if self.canvas_data[current_cell].is_empty:
                        del self.canvas_data[current_cell]
                    self.check_border(current_cell)

            selected_float = self.mouse_on_float()
            if selected_float:
                selected_float.kill()

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
            pygame.draw.line(self.guide_surf, "black", (x, 0), (x, s.WINDOW_HEIGTH))

        for row in range(rows + 1):
            y = origin_offset.y + row * s.TILE_SIZE
            pygame.draw.line(self.guide_surf, "black", (0, y), (s.WINDOW_WIDTH, y))

        self.display_surface.blit(self.guide_surf, (0, 0))

    def draw_level(self):
        for cell_pos, tile in self.canvas_data.items():
            pos = self.origin + vector(cell_pos) * s.TILE_SIZE
            if tile.air:
                self.display_surface.blit(self.air_surf, pos)

        self.canvas_backgroud.draw(self.display_surface)
        for cell_pos, tile in self.canvas_data.items():
            pos = self.origin + vector(cell_pos) * s.TILE_SIZE

            if tile.wall:
                surf = self.wall_tiles[
                    tile.get_wall_name()
                    if tile.get_wall_name() in self.wall_tiles
                    else "X"
                ]
                self.display_surface.blit(surf, pos)

            if tile.coin:
                frames = self.animations[tile.coin]["frames"]
                index = int(self.animations[tile.coin]["frame_index"])
                coin_surf = frames[index]
                rect = coin_surf.get_rect(
                    center=(pos.x + s.TILE_SIZE // 2, pos.y + s.TILE_SIZE // 2)
                )
                self.display_surface.blit(coin_surf, rect)

        self.canvas_midground.draw(self.display_surface)
        self.canvas_foregroud.draw(self.display_surface)

    def draw_float_frame(self):
        selected_float = self.mouse_on_float()
        if selected_float:
            rect = selected_float.rect.inflate(10, 10)
            color = "black"
            width = 3
            size = 15
            # topleft
            pygame.draw.lines(
                self.display_surface,
                color,
                False,
                (
                    (rect.left, rect.top + size),
                    rect.topleft,
                    (rect.left + size, rect.top),
                ),
                width,
            )
            # topright
            pygame.draw.lines(
                self.display_surface,
                color,
                False,
                (
                    (rect.right - size, rect.top),
                    rect.topright,
                    (rect.right, rect.top + size),
                ),
                width,
            )
            # bottomleft
            pygame.draw.lines(
                self.display_surface,
                color,
                False,
                (
                    (rect.left, rect.bottom - size),
                    rect.bottomleft,
                    (rect.left + size, rect.bottom),
                ),
                width,
            )
            # bottomright
            pygame.draw.lines(
                self.display_surface,
                color,
                False,
                (
                    (rect.right - size, rect.bottom),
                    rect.bottomright,
                    (rect.right, rect.bottom - size),
                ),
                width,
            )
            return True

    def draw_previews(self):
        type_dict = {key: value["type"] for key, value in s.CANVAS_TEMPLATES.items()}
        surf = self.preview_surfs[self.selection_id].copy()
        surf.set_alpha(200)

        if type_dict[self.selection_id] == "tile":
            current_cell = self.get_current_cell(mouse_pos())
            rect = surf.get_rect(
                topleft=self.origin + vector(current_cell) * s.TILE_SIZE
            )
        else:
            rect = surf.get_rect(center=mouse_pos())

        self.display_surface.blit(surf, rect)

    def run(self, dt):
        self.event_loop()

        self.animations_update(dt)
        self.canvas_floats.update(dt)
        self.hold_timer.update()
        self.float_cooldown_timer.update()

        self.display_surface.fill("white")
        self.draw_level()
        self.draw_tile_guides()
        if not self.draw_float_frame():
            self.draw_previews()

        pygame.draw.circle(self.display_surface, "red", self.origin, 5)
        self.menu.display()


class CanvasTile:
    def __init__(self, tile_id, offset=vector()):
        self.wall = False
        self.air = False
        self.coin = None

        self.is_empty = False

        self.wall_neighbors = []

        self.pinned_floats = []

        self.add_id(tile_id, offset=offset)

    def add_id(self, selection_id, offset=vector()):
        match selection_id:
            case 1:
                self.wall = True
                self.air = False
            case 2:
                self.air = True
                self.wall = False
            case 3:
                self.coin = selection_id

            case _:
                if (selection_id, offset) not in self.pinned_floats:
                    self.pinned_floats.append((selection_id, offset))

    def remove_id(self, tile_id):
        match tile_id:
            case 1:
                self.wall = False
            case 2:
                self.air = False
            case 3:
                self.coin = None
        self.check_content()

    def check_content(self):
        if not self.wall and not self.coin and not self.air and not self.pinned_floats:
            self.is_empty = True

    def get_wall_name(self):
        return "".join(self.wall_neighbors)


class CanvasFloat(pygame.sprite.Sprite):
    def __init__(self, pos, frames, float_id, origin, groups):
        super().__init__(groups)
        self.float_id = float_id

        self.frames = frames
        if len(self.frames) == 1:
            self.static = True
        else:
            self.static = False
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
        if not self.static:
            self.animate(dt)
        self.drag()
