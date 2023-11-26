import pygame
from pygame.math import Vector2 as vector

import settings as s


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
    def __init__(self, pos, group, collision_sprites):
        super().__init__(pos, pygame.Surface((90, 127)), group)
        self.image.fill("green")

        self.speed = vector()
        self.touch_ground = True

        self.hitbox = self.rect.inflate(-50, -15)
        self.shift = vector(self.hitbox.topleft)
        self.collision_sprites = collision_sprites

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.speed.x = 1
        elif keys[pygame.K_a]:
            self.speed.x = -1
        else:
            self.speed.x = 0

        if keys[pygame.K_w] and self.touch_ground:
            self.speed.y = -2

    def move(self, dt):
        self.shift.x += self.speed.x * s.PLAYER_SPEED * dt
        self.hitbox.x = round(self.shift.x)
        self.rect.centerx = self.hitbox.centerx
        self.collistion_check("X")

        self.gravity_pull(dt)
        self.hitbox.y = round(self.shift.y)
        self.rect.centery = self.hitbox.centery
        self.collistion_check("Y")

    def gravity_pull(self, dt):
        self.speed.y += s.GRAVITY * dt
        self.shift.y += self.speed.y

    def check_ground(self):
        bottom_rect = pygame.Rect(
            self.hitbox.left, self.hitbox.bottom, self.hitbox.width, 2
        )
        ground_sprites = [
            sprite
            for sprite in self.collision_sprites
            if sprite.rect.colliderect(bottom_rect)
        ]
        self.touch_ground = True if ground_sprites else False

    def collistion_check(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox):
                if direction == "X":
                    if self.speed.x > 0:
                        self.hitbox.right = sprite.rect.left
                    if self.speed.x < 0:
                        self.hitbox.left = sprite.rect.right
                    self.rect.centerx = self.hitbox.centerx
                    self.shift.x = self.hitbox.x
                    self.speed.x = 0

                if direction == "Y":
                    if self.speed.y > 0:
                        self.hitbox.bottom = sprite.rect.top
                    if self.speed.y < 0:
                        self.hitbox.top = sprite.rect.bottom
                    self.rect.centery = self.hitbox.centery
                    self.shift.y = self.hitbox.y
                    self.speed.y = 0

    def update(self, dt):
        self.input()
        self.move(dt)
        self.check_ground()


class Enemy(Generic):
    def __init__(self, pos, group):
        super().__init__(pos, pygame.Surface((80, 80)), group)
        self.image.fill("red")


class Prop(Generic):
    def __init__(self, pos, surf, group):
        super().__init__(pos, surf, group)
