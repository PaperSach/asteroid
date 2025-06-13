import pygame
from constants import *
from circleshape import CircleShape

class Bomb(CircleShape):
    containers = None

    def __init__(self, x, y):
        super().__init__(x, y, 10)
        self.velocity = pygame.Vector2(0, 100)  # Falls downward slowly
        self.timer = 3  # seconds before explosion
        if self.containers:
            self.add(*self.containers)

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), self.position, self.radius)
        pygame.draw.circle(screen, (255, 255, 0), self.position, self.radius - 3)

    def update(self, dt):
        self.position += self.velocity * dt
        self.timer -= dt
        self.wrap_screen()
        if self.timer <= 0:
            self.explode()

    def explode(self):
        from explosion import Explosion  # avoid circular import
        Explosion(self.position)
        self.kill()

    def wrap_screen(self):
        if self.position.x < 0:
            self.position.x = SCREEN_WIDTH
        elif self.position.x > SCREEN_WIDTH:
            self.position.x = 0
        if self.position.y < 0:
            self.position.y = SCREEN_HEIGHT
        elif self.position.y > SCREEN_HEIGHT:
            self.position.y = 0
