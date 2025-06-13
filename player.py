import pygame
from constants import *
from circleshape import CircleShape
from shot import Shot
from bomb import Bomb

class Player(CircleShape):
    containers = None  # Will be set in main.py

    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shoot_timer = 0
        self.bomb_cooldown = 0
        self.weapon_type = "laser"
        self.lives = 3
        self.score = 0  # Initialize score

        if self.containers:
            self.add(*self.containers)

    def draw(self, screen):
        points = self.triangle()
        pygame.draw.polygon(screen, (255, 255, 255), points, 2)

    def triangle(self):
        forward = pygame.Vector2(0, -1).rotate(self.rotation)
        right = pygame.Vector2(1, 0).rotate(self.rotation) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius + right
        c = self.position - forward * self.radius - right
        # Return integer tuples for drawing
        return [(int(a.x), int(a.y)), (int(b.x), int(b.y)), (int(c.x), int(c.y))]

    def update(self, dt):
        self.shoot_timer -= dt
        self.bomb_cooldown -= dt

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            self.shoot()
        if keys[pygame.K_b]:
            self.drop_bomb()

        self.wrap_screen()

    def shoot(self):
        if self.shoot_timer > 0 or self.weapon_type != "laser":
            return
        self.shoot_timer = PLAYER_SHOOT_COOLDOWN
        direction = pygame.Vector2(0, -1).rotate(self.rotation)
        offset = direction * PLAYER_RADIUS
        spawn_pos = self.position + offset
        shot = Shot(spawn_pos.x, spawn_pos.y)
        shot.velocity = direction * PLAYER_SHOOT_SPEED

        if hasattr(Shot, "containers"):
            for group in Shot.containers:
                group.add(shot)

    def drop_bomb(self):
        if self.bomb_cooldown > 0 or self.weapon_type != "bomb":
            return
        self.bomb_cooldown = 1.5
        bomb = Bomb(self.position.x, self.position.y)
        if hasattr(Bomb, "containers"):
            for group in Bomb.containers:
                group.add(bomb)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt
        self.rotation %= 360

    def move(self, dt):
        forward = pygame.Vector2(0, -1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt

    def wrap_screen(self):
        if self.position.x < 0:
            self.position.x = SCREEN_WIDTH
        elif self.position.x > SCREEN_WIDTH:
            self.position.x = 0
        if self.position.y < 0:
            self.position.y = SCREEN_HEIGHT
        elif self.position.y > SCREEN_HEIGHT:
            self.position.y = 0
