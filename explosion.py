import pygame
from constants import *
from circleshape import CircleShape

class Explosion(CircleShape):
    containers = None

    def __init__(self, position):
        super().__init__(position.x, position.y, 30)
        self.timer = 0.5  # half second duration
        if self.containers:
            self.add(*self.containers)

    def update(self, dt):
        self.timer -= dt
        if self.timer <= 0:
            self.kill()

    def draw(self, screen):
        radius = int(self.radius * (self.timer / 0.5))
        if radius > 0:
            pygame.draw.circle(screen, (255, 165, 0), self.position, radius)
