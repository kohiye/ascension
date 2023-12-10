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
        self.exit_door_group = PlayerCameraGroup()

        self.money = 0
        self.nodes = {}

        self.build(lvl_data, asset_dict)

    def build(self, lvl_data, asset_dict):
        for layer_name, layer in lvl_data.items():
            if layer_name == "nodes":
                self.build_nodes(layer)
            else:
                self.build_lvl(layer_name, layer, asset_dict)

        for enemy in self.enemy_sprites:
            if enemy.enemy_id in self.nodes:
                nodes = self.nodes[enemy.enemy_id]
            else:
                nodes = None
            enemy.share_data(self.player, nodes)

    def build_nodes(self, layer):
        for pos, data in layer.items():
            if data[0] in self.nodes:
                self.nodes[data[0]][data[1]] = pos
            else:
                self.nodes[data[0]] = {data[1]: pos}

    def build_lvl(self, layer_name, layer, asset_dict):
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

            if layer_name == "enemies":
                Enemy(pos, groups + [self.enemy_sprites], self.collision_sprites, data)
                continue

            match data:
                case 4:
                    Prop(pos, asset_dict["chair_fg"], groups)
                case 5:
                    Prop(pos, asset_dict["chair_bg"], groups)
                case 8:
                    Prop(pos, asset_dict["entrance"], groups)
                    player_pos = (pos[0] + 70, pos[1])
                    self.player = Player(player_pos, groups, self.collision_sprites)
                case 9:
                    Prop(pos, asset_dict["exit"], groups + [self.exit_door_group])

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

    def door_exit(self):
        if pygame.sprite.spritecollide(self.player, self.exit_door_group, False):
            self.switch("lvl_exit")

    def run(self, dt):
        self.event_loop()
        self.generic_sprites.update(dt)
        self.coin_collision()
        self.door_exit()

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
