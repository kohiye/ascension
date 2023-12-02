import pygame
import sys

import settings as s
from lvlsprites import Generic, Player, Coin, Prop, Enemy


class Level:
    def __init__(self, lvl_data, switch, asset_dict):
        self.display_surface = pygame.display.get_surface()
        self.switch = switch

        self.generic_sprites = pygame.sprite.Group()
        self.fore_sprites = pygame.sprite.Group()
        self.back_sprites = pygame.sprite.Group()
        self.mid_sprites = pygame.sprite.Group()
        self.wall_sprites = pygame.sprite.Group()
        self.coin_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

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
                            self.player,
                            self.collision_sprites,
                        )

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
        self.wall_sprites.draw(self.display_surface)
        self.back_sprites.draw(self.display_surface)
        self.mid_sprites.draw(self.display_surface)
        self.fore_sprites.draw(self.display_surface)
