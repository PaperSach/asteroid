import sys
import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from bomb import Bomb
from explosion import Explosion  # If using explosion effects

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Asteroid Game")
    clock = pygame.time.Clock()

    # Load and scale background image
    background = pygame.image.load("background.jpg").convert()
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # Font for score display
    font = pygame.font.SysFont(None, 36)  # Default font, size 36

    # Sprite groups
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    # Register containers
    Asteroid.containers = (asteroids, updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    Bomb.containers = (updatable, drawable)
    Explosion.containers = (updatable, drawable)
    Player.containers = (updatable, drawable)

    # Create game objects
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()

    score = 0  # Initialize score

    dt = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        updatable.update(dt)
        asteroid_field.update(dt)

        # Handle collisions and update score
        for asteroid in list(asteroids):
            if asteroid.collides_with(player):
                print("Game Over! Final Score:", score)
                return
            for shot in list(shots):
                if asteroid.collides_with(shot):
                    shot.kill()
                    asteroid.split()
                    score += 10  # Add points per asteroid hit

        # Draw background and game objects
        screen.blit(background, (0, 0))

        for obj in drawable:
            obj.draw(screen)

        # Draw score on screen
        score_surface = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_surface, (10, 10))

        pygame.display.flip()
        dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()
