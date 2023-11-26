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
    def __init__(self, pos, group):
        super().__init__(pos, pygame.Surface((50, 100)), group)
        self.image.fill("green")

        self.direction = vector()
        self.shift = vector(self.rect.topleft)

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.direction.x = 1
        elif keys[pygame.K_a]:
            self.direction.x = -1
        else:
            self.direction.x = 0

    def move(self, dt):
        self.shift += self.direction * s.PLAYER_SPEED * dt
        self.rect.topleft = (round(self.shift.x), round(self.shift.y))

    def update(self, dt):
        self.input()
        self.move(dt)


class Enemy(Generic):
    def __init__(self, pos, group):
        super().__init__(pos, pygame.Surface((80, 80)), group)
        self.image.fill("red")


class Prop(Generic):
    def __init__(self, pos, surf, group):
        super().__init__(pos, surf, group)
