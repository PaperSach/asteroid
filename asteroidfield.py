import pygame
import random
from constants import *
from asteroid import Asteroid

class AsteroidField(pygame.sprite.Sprite):
    containers = None  # This will be set in main.py to the update group

    def __init__(self):
        super().__init__()
        self.spawn_timer = 0

    def update(self, dt):
        self.spawn_timer -= dt
        if self.spawn_timer <= 0:
            self.spawn_timer = ASTEROID_SPAWN_RATE
            self.spawn_asteroid()

    def spawn_asteroid(self):
        # Spawn asteroid at random edge of screen with random velocity
        side = random.choice(['top', 'bottom', 'left', 'right'])

        if side == 'top':
            x = random.uniform(0, SCREEN_WIDTH)
            y = 0
        elif side == 'bottom':
            x = random.uniform(0, SCREEN_WIDTH)
            y = SCREEN_HEIGHT
        elif side == 'left':
            x = 0
            y = random.uniform(0, SCREEN_HEIGHT)
        else:  # right
            x = SCREEN_WIDTH
            y = random.uniform(0, SCREEN_HEIGHT)

        radius = random.choice([ASTEROID_MIN_RADIUS * i for i in range(1, ASTEROID_KINDS + 1)])

        asteroid = Asteroid(x, y, radius)

        # Add asteroid to all its containers if not automatically handled by containers attribute
        if self.containers:
            for group in self.containers:
                group.add(asteroid)
