import pygame
import random
from constants import *
from asteroid import Asteroid

class AsteroidField:
    containers = None

    def __init__(self):
        self.timer = 0
        if self.containers:
            self.add(*self.containers)

    def add(self, *groups):
        # no need to be sprite, but we keep it in updatable group to manage timer
        for group in groups:
            group.add(self)

    def update(self, dt):
        self.timer -= dt
        if self.timer <= 0:
            self.timer = ASTEROID_SPAWN_RATE
            radius = random.randint(ASTEROID_MIN_RADIUS, ASTEROID_MAX_RADIUS)
            # Spawn at random edge of screen
            edge = random.choice(['top', 'bottom', 'left', 'right'])
            if edge == 'top':
                x = random.uniform(0, SCREEN_WIDTH)
                y = 0
            elif edge == 'bottom':
                x = random.uniform(0, SCREEN_WIDTH)
                y = SCREEN_HEIGHT
            elif edge == 'left':
                x = 0
                y = random.uniform(0, SCREEN_HEIGHT)
            else:  # right
                x = SCREEN_WIDTH
                y = random.uniform(0, SCREEN_HEIGHT)

            asteroid = Asteroid(x, y, radius)
