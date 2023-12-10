import pygame
from math import atan2

from pygame.math import Vector2 as vector
from pygame.mouse import get_pos as mouse_pos
from pygame.mouse import get_pressed as mouse_buttons

import settings as s
from timer import Timer
from support import signum


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

        # gun
        self.face_vector = vector(1, 0)
        self.gun_surf_temp = pygame.image.load("../graphics/gun.png").convert_alpha()
        self.gun_rect = self.gun_surf_temp.get_rect(center=self.rect.center)
        self.gun_vector = vector(self.gun_rect.center) - vector(mouse_pos())
        self.offset = vector()
        self.ammo = 10
        self.gun_cooldown = Timer(100)

        self.gun_surf = self.gun_surf_temp.copy()

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

        self.offset.x = self.rect.centerx - s.WINDOW_WIDTH // 2
        self.offset.y = self.rect.centery - s.WINDOW_HEIGHT // 2 - 50
        self.gun_vector = vector(mouse_pos()) + self.offset - vector(self.rect.center)
        angle = self.gun_vector.angle_to(self.face_vector)

        self.gun_surf = pygame.transform.rotate(self.gun_surf_temp, angle)
        self.gun_rect = self.gun_surf.get_rect()
        self.gun_rect.center = self.rect.center

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

    def get_gun(self):
        return self.gun_surf

    def shoot(self):
        if self.ammo and not self.gun_cooldown.active and mouse_buttons()[0]:
            self.ammo -= 1
            self.gun_cooldown.activate()
            self.image.fill("orange")
            # print("booom ", self.ammo)

    def update(self, dt):
        self.image.fill("green")
        self.input()
        self.move(dt)
        self.shoot()
        self.check_ground()
        self.gun_cooldown.update()


class Enemy(Generic):
    def __init__(self, pos, group, collision_sprites, enemy_id):
        super().__init__(pos, pygame.Surface((80, 80)), group)
        self.image.fill("blue")

        self.display_surf = pygame.display.get_surface()

        self.speed = vector()
        self.thrust = vector()
        self.drag = vector()
        self.shift = vector(self.rect.topleft)
        self.drag_coeff = 0.01

        self.collision_sprites = collision_sprites
        self.last_target = vector(self.rect.center)
        self.node_target = None
        self.target = self.last_target
        self.agro = False
        self.agro_timer = Timer(10000)

        self.hitbox = self.rect.inflate(-40, -40)
        self.repulsion_rect = self.rect.inflate(40, 40)
        self.player_repulsion_rect = self.rect.inflate(400, 400)
        self.repulsion = vector()
        self.offset = vector()

        self.enemy_id = enemy_id
        self.node_index = 1

    def share_data(self, player, nodes):
        self.player = player
        self.nodes = nodes

    def offset_sync(self):
        self.offset.x = self.player.rect.centerx - s.WINDOW_WIDTH // 2
        self.offset.y = self.player.rect.centery - s.WINDOW_HEIGHT // 2 - 50

    def input(self):
        target_diff = self.target - vector(self.rect.center)
        if target_diff != vector((0, 0)):
            self.thrust = 500 * target_diff.normalize()

    def attack(self):
        if self.agro:
            pass

    def enemy_vision(self):
        obstuctions = []
        for sprite in self.collision_sprites:
            if sprite.rect.clipline(self.player.rect.center, self.rect.center):
                obstuctions.append(sprite)

        if obstuctions and self.agro:
            self.target = self.last_target
            self.image.fill("orange")
            dist_to_target = vector(self.hitbox.center) - vector(self.target)
            if dist_to_target.magnitude() < 40:
                if not self.agro_timer.active:
                    self.agro_timer.activate()
                else:
                    self.agro_timer.update()
                if not self.agro_timer.active:
                    self.agro = False

        elif obstuctions and not self.agro:
            if self.node_target:
                self.target = self.node_target
            else:
                self.target = self.last_target
            self.image.fill("blue")

        else:
            self.agro = True
            self.target = vector(self.player.rect.center)
            self.last_target = self.target
            self.image.fill("red")

    def friction(self):
        self.drag.x = (
            self.drag_coeff * (self.speed.x**2)
            if self.speed.x < 0
            else -self.drag_coeff * (self.speed.x**2)
        )
        self.drag.y = (
            self.drag_coeff * (self.speed.y**2)
            if self.speed.y < 0
            else -self.drag_coeff * (self.speed.y**2)
        )

    def move(self, dt):
        self.friction()
        self.repulsion_check()
        self.player_repulsion_check()

        self.speed.x += (
            self.thrust.x
            + self.drag.x
            + 200 * self.repulsion.x
            + 4000 * self.player_repulsion.x
        ) * dt
        self.speed.y += (
            self.thrust.y
            + self.drag.y
            + 200 * self.repulsion.y
            + 4000 * self.player_repulsion.y
        ) * dt

        self.shift.x += self.speed.x * dt
        self.hitbox.x = round(self.shift.x)
        self.repulsion_rect.centerx = self.hitbox.centerx
        self.player_repulsion_rect.centerx = self.hitbox.centerx
        self.collistion_check("X")
        self.rect.centerx = self.hitbox.centerx

        self.shift.y += self.speed.y * dt
        self.hitbox.y = round(self.shift.y)
        self.repulsion_rect.centery = self.hitbox.centery
        self.player_repulsion_rect.centery = self.hitbox.centery
        self.collistion_check("Y")
        self.rect.centery = self.hitbox.centery

    def node_route(self):
        if not self.agro and self.nodes:
            self.node_target = vector(self.nodes[self.node_index])
            dist_to_node = vector(self.hitbox.center) - vector(
                self.nodes[self.node_index]
            )
            if dist_to_node.magnitude() < 40:
                self.node_index += 1
            if self.node_index > len(self.nodes):
                self.node_index = 1

    def player_repulsion_check(self):
        self.player_repulsion = vector()
        if self.player.rect.colliderect(self.player_repulsion_rect):
            repulsion_distance = vector(self.rect.center) - vector(
                self.player.rect.center
            )
            self.player_repulsion = repulsion_distance.normalize() * (
                100 / repulsion_distance.magnitude()
            )

    def repulsion_check(self):
        self.repulsion = vector()
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.repulsion_rect):
                repulsion_distance = vector(self.rect.center) - vector(
                    sprite.rect.center
                )
                repulsion_multi = repulsion_distance.normalize() * (
                    100 / repulsion_distance.magnitude()
                )
                self.repulsion += repulsion_multi

        if abs(self.repulsion.x) < 2:
            self.repulsion.x = 0
        if abs(self.repulsion.y) < 2:
            self.repulsion.y = 0

    def collistion_check(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox):
                if direction == "X":
                    if self.speed.x > 0:
                        self.hitbox.right = sprite.rect.left
                    if self.speed.x < 0:
                        self.hitbox.left = sprite.rect.right
                    self.shift.x = self.hitbox.x
                    self.speed.x = -self.speed.x

                if direction == "Y":
                    if self.speed.y > 0:
                        self.hitbox.bottom = sprite.rect.top
                    if self.speed.y < 0:
                        self.hitbox.top = sprite.rect.bottom
                    self.shift.y = self.hitbox.y
                    self.speed.y = -self.speed.y

    def update(self, dt):
        self.offset_sync()
        self.node_route()
        self.enemy_vision()
        self.input()
        self.move(dt)


class Prop(Generic):
    def __init__(self, pos, surf, group):
        super().__init__(pos, surf, group)

class Bullet(pygame.sprite.Sprite):
    def __init__(self):
