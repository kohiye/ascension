import pygame
import sys

from pygame.math import Vector2 as vector

import settings as s
from lvlsprites import Generic, Player, Coin, Prop, Enemy


class Level:
    def __init__(self, lvl_data, switch, asset_dict):
        self.display_surface = pygame.display.get_surface()
        self.switch = switch

        self.generic_sprites = PlayerCameraGroup()
        self.fore_sprites = PlayerCameraGroup()
        self.back_sprites = PlayerCameraGroup()
        self.mid_sprites = PlayerCameraGroup()
        self.wall_sprites = PlayerCameraGroup()
        self.coin_sprites = PlayerCameraGroup()
        self.enemy_sprites = PlayerCameraGroup()
        self.collision_sprites = PlayerCameraGroup()

        self.money = 0

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
                elif layer_name == "coins":
                    groups.append(self.wall_sprites)
                    groups.append(self.coin_sprites)
                else:
                    groups.append(self.wall_sprites)

                if layer_name == "walls":
                    Generic(
                        pos,
                        asset_dict["walls"][data],
                        groups + [self.collision_sprites],
                    )
                if layer_name == "air":
                    Generic(pos, asset_dict["air"], groups)
                if layer_name == "coins":
                    Coin(pos, asset_dict["coin"], groups)

                match data:
                    case 0:
                        self.player = Player(pos, groups, self.collision_sprites)

                    case 4:
                        Prop(pos, asset_dict["chair_fg"], groups)
                    case 5:
                        Prop(pos, asset_dict["chair_bg"], groups)
                    case 6:
                        Enemy(
                            pos,
                            groups + [self.enemy_sprites],
                            self.collision_sprites,
                        )
                    case 8:
                        Prop(pos, asset_dict["entrance"], groups)
                    case 9:
                        Prop(pos, asset_dict["exit"], groups)

            for enemy in self.enemy_sprites:
                enemy.share_player(self.player)

    def event_loop(self):
        for event in pygame.event.get():
            self.switch(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def coin_collision(self):
        collided_coins = pygame.sprite.spritecollide(
            self.player, self.coin_sprites, True
        )
        for sprite in collided_coins:
            self.money += 1

    def run(self, dt):
        self.event_loop()
        self.generic_sprites.update(dt)
        self.coin_collision()

        self.display_surface.fill("lightblue")
        self.wall_sprites.camera_draw(self.player)
        self.back_sprites.camera_draw(self.player)
        self.mid_sprites.camera_draw(self.player)
        self.fore_sprites.camera_draw(self.player)


class PlayerCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = vector()

    def camera_draw(self, player):
        self.offset.x = player.rect.centerx - s.WINDOW_WIDTH // 2
        self.offset.y = player.rect.centery - s.WINDOW_HEIGHT // 2 - 50

        for sprite in self:
            offset_rect = sprite.rect.copy()
            offset_rect.center -= self.offset
            self.display_surface.blit(sprite.image, offset_rect)

        gun_rect = player.gun_rect.copy()
        gun_rect.center -= self.offset
        self.display_surface.blit(player.gun_surf, gun_rect)
