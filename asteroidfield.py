import random
from constants import *
from asteroid import Asteroid

class AsteroidField:
    def __init__(self):
        self.timer = 0

    def update(self, dt):
        self.timer -= dt
        if self.timer <= 0:
            self.timer = ASTEROID_SPAWN_RATE
            radius = random.randint(ASTEROID_MIN_RADIUS, ASTEROID_MAX_RADIUS)
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

            # Creating an asteroid will auto-add it to sprite groups via containers
            Asteroid(x, y, radius)
