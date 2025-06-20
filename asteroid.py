import pygame
import random
from constants import *
from circleshape import CircleShape

class Asteroid(CircleShape):
    containers = None

    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.velocity = pygame.Vector2(random.uniform(-100, 100), random.uniform(-100, 100))
        if self.containers:
            self.add(*self.containers)

    def draw(self, screen):
        pygame.draw.circle(screen, "red", self.position, self.radius)

    def update(self, dt):
        self.position += self.velocity * dt
        self.wrap_screen()

    def wrap_screen(self):
        if self.position.x < 0:
            self.position.x = SCREEN_WIDTH
        elif self.position.x > SCREEN_WIDTH:
            self.position.x = 0
        if self.position.y < 0:
            self.position.y = SCREEN_HEIGHT
        elif self.position.y > SCREEN_HEIGHT:
            self.position.y = 0

    def split(self):
        self.kill()

        if self.radius <= ASTEROID_MIN_RADIUS:
            return

        random_angle = random.uniform(20, 50)

        a = self.velocity.rotate(random_angle)
        b = self.velocity.rotate(-random_angle)

        new_radius = self.radius - ASTEROID_MIN_RADIUS
        asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid1.velocity = a * 1.2
        asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid2.velocity = b * 1.2

    def collides_with(self, other):
        dist = self.position.distance_to(other.position)
        return dist < self.radius + other.radius
