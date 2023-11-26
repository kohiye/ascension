import pygame
import sys

import settings as s


class Level:
    def __init__(self, lvl_data, switch, asset_dict):
        self.display_surface = pygame.display.get_surface()
        self.switch = switch

        self.generic_sprites = pygame.sprite.Group()
        self.fore_sprites = pygame.sprite.Group()
        self.back_sprites = pygame.sprite.Group()
        self.mid_sprites = pygame.sprite.Group()
        self.wall_sprites = pygame.sprite.Group()

        self.build(lvl_data, asset_dict)

    def build(self, lvl_data, asset_dict):
        for layer_name, layer in lvl_data.items():
            for pos, data in layer.items():
                groups = [self.generic_sprites]
                if layer_name == "midground":
                    groups.append(self.mid_sprites)
                elif layer_name == "foreground":
                    groups.append(self.fore_sprites)
                elif layer_name == "background":
                    groups.append(self.back_sprites)
                else:
                    groups.append(self.wall_sprites)

                if layer_name == "walls":
                    Generic(pos, asset_dict["walls"][data], groups)
                if layer_name == "air":
                    Generic(pos, asset_dict["air"], groups)
                if layer_name == "coins":
                    Coin(pos, asset_dict["coin"], groups)

                match data:
                    case 0:
                        Player(pos, groups)

                    case 4:
                        Prop(pos, asset_dict["chair_fg"], groups)
                    case 5:
                        Prop(pos, asset_dict["chair_bg"], groups)

    def event_loop(self):
        for event in pygame.event.get():
            self.switch(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def run(self, dt):
        self.event_loop()
        self.generic_sprites.update(dt)
        self.display_surface.fill("red")
        self.wall_sprites.draw(self.display_surface)
        self.back_sprites.draw(self.display_surface)
        self.mid_sprites.draw(self.display_surface)
        self.fore_sprites.draw(self.display_surface)


class Generic(pygame.sprite.Sprite):
    def __init__(self, pos, surf, group):
        super().__init__(group)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)


class Animated(Generic):
    def __init__(self, pos, frames, group):
        self.frames = frames
        self.frame_index = 0
        super().__init__(pos, self.frames[self.frame_index], group)

    def animate(self, dt):
        self.frame_index += s.ANIMATION_SPEED * dt
        self.frame_index = (
            0 if self.frame_index >= len(self.frames) else self.frame_index
        )
        self.image = self.frames[int(self.frame_index)]

    def update(self, dt):
        self.animate(dt)


class Coin(Animated):
    def __init__(self, pos, frames, group):
        super().__init__(pos, frames, group)
        self.rect = self.image.get_rect(center=pos)


class Player(Generic):
    def __init__(self, pos, group):
        super().__init__(pos, pygame.Surface((100, 100)), group)
        self.image.fill("black")


class Prop(Generic):
    def __init__(self, pos, surf, group):
        super().__init__(pos, surf, group)
