import pygame
import sys

from pygame.math import Vector2 as vector

import settings as s
from lvlsprites import Generic, Player, Coin, Prop, Enemy
from gameMenu import Menu


class Level:
    def __init__(self, lvl_data, switch, asset_dict):
        self.display_surface = pygame.display.get_surface()
        self.switch = switch

        self.menu = Menu()

        self.coin_sound = pygame.mixer.Sound("../audio/coin.mp3")
        self.coin_sound.set_volume(s.VOLUME)

        self.player_sprites = PlayerCameraGroup()
        self.generic_sprites = PlayerCameraGroup()
        self.fore_sprites = PlayerCameraGroup()
        self.back_sprites = PlayerCameraGroup()
        self.mid_sprites = PlayerCameraGroup()
        self.wall_sprites = PlayerCameraGroup()
        self.coin_sprites = PlayerCameraGroup()
        self.player_sprites = PlayerCameraGroup()
        self.enemy_sprites = PlayerCameraGroup()
        self.collision_sprites = PlayerCameraGroup()
        self.exit_door_group = PlayerCameraGroup()

        self.player_bullets = PlayerCameraGroup()
        self.enemy_bullets = PlayerCameraGroup()

        self.money = 0
        self.player_health = 100

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
                Enemy(
                    pos,
                    asset_dict["enemy"],
                    groups + [self.enemy_sprites],
                    self.collision_sprites,
                    data,
                    self.enemy_bullets,
                )
                continue

            match data:
                case 4:
                    Prop(pos, asset_dict["chairR_fg"], groups)
                case 5:
                    Prop(pos, asset_dict["chairR_bg"], groups)
                case 6:
                    Prop(pos, asset_dict["chairL_fg"], groups)
                case 7:
                    Prop(pos, asset_dict["chairL_bg"], groups)
                case 8:
                    Prop(pos, asset_dict["table_fg"], groups)
                case 9:
                    Prop(pos, asset_dict["table_bg"], groups)
                case 10:
                    Prop(pos, asset_dict["box_fg"], groups)
                case 11:
                    Prop(pos, asset_dict["box_bg"], groups)

                case 14:
                    Prop(pos, asset_dict["entrance"], groups)
                    player_pos = (pos[0] + s.PLAYER_DOOR_SPAWN_DISTANCE, pos[1])
                    self.player = Player(
                        player_pos, 
                        asset_dict["player"], 
                        groups + [self.mid_sprites],
                        self.collision_sprites,
                        self.player_bullets,
                        self.switch,
                    )
                case 15:
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
            self.coin_sound.play()

    def enemy_hit(self):
        hits = pygame.sprite.groupcollide(
            self.enemy_sprites, self.player_bullets, False, True
        )
        if hits:
            for enemy, points in hits.items():
                enemy.health -= len(points)

                if enemy.health <= 0:
                    enemy.kill()
                    self.money += 10
                    self.coin_sound.play()

    def player_hit(self):
        hits = pygame.sprite.spritecollide(self.player, self.enemy_bullets, True)
        for sprite in hits:
            self.player_health -= 1

        if self.player_health <= 0:
            self.switch("death", money=self.money)

    def door_exit(self):
        if pygame.sprite.spritecollide(self.player, self.exit_door_group, False):
            self.switch("lvl_exit", money=self.money)

    def bullet_wall_collison(self):
        enemy_collisions = pygame.sprite.groupcollide(
            self.collision_sprites, self.enemy_bullets, False, True
        )
        player_collisions = pygame.sprite.groupcollide(
            self.collision_sprites, self.player_bullets, False, True
        )

    def draw_enemy_guns(self, offset):
        for enemy in self.enemy_sprites:
            gun_rect = enemy.gun_rect.copy()
            gun_rect.topleft -= offset
            self.display_surface.blit(enemy.gun_surf, gun_rect)

    def run(self, dt):
        self.event_loop()
        self.generic_sprites.update(dt)
        self.player_bullets.update(dt)
        self.enemy_bullets.update(dt)
        self.bullet_wall_collison()
        self.coin_collision()
        self.enemy_hit()
        self.player_hit()
        self.door_exit()

        self.display_surface.fill("black")
        self.wall_sprites.camera_draw(self.player)
        self.back_sprites.camera_draw(self.player)
        self.mid_sprites.camera_draw(self.player)

        self.offset = vector()
        self.offset.x = self.player.rect.centerx - s.WINDOW_WIDTH // 2
        self.offset.y = (
            self.player.rect.centery - s.WINDOW_HEIGHT // 2 - s.CAMERA_Y_SHIFT
        )
        gun_rect = self.player.gun_rect.copy()
        gun_rect.topleft -= self.offset
        self.display_surface.blit(self.player.gun_surf, gun_rect)

        self.draw_enemy_guns(self.offset)

        self.fore_sprites.camera_draw(self.player)

        self.player_bullets.camera_draw(self.player)
        self.enemy_bullets.camera_draw(self.player)


class PlayerCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = vector()

    def camera_draw(self, player):
        self.offset.x = player.rect.centerx - s.WINDOW_WIDTH // 2
        self.offset.y = player.rect.centery - s.WINDOW_HEIGHT // 2 - s.CAMERA_Y_SHIFT

        for sprite in self:
            offset_rect = sprite.rect.copy()
            offset_rect.center -= self.offset
            self.display_surface.blit(sprite.image, offset_rect)
