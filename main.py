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

    score = 0
    font = pygame.font.Font(None, 36)  # Default font, size 36

    while True:
        dt = clock.tick(60) / 1000  # Calculate dt at the start of the loop

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        updatable.update(dt)
        asteroid_field.update(dt)

        # Handle collisions and life system
        for asteroid in asteroids:
            if asteroid.collides_with(player):
                player.lives -= 1
                print(f"Lives left: {player.lives}")
                # Reset player position and rotation on hit
                player.position = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                player.rotation = 0
                if player.lives <= 0:
                    print("Game Over!")
                    return
            for shot in shots:
                if asteroid.collides_with(shot):
                    shot.kill()
                    asteroid.split()
                    score += 10  # Increase score for destroying asteroid

        # Draw background and game objects
        screen.blit(background, (0, 0))
        for obj in drawable:
            obj.draw(screen)

        # Render score on screen (top left)
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))

        # Render lives on screen (top right)
        lives_text = font.render(f"Lives: {player.lives}", True, (0, 0, 0))
        lives_rect = lives_text.get_rect(topright=(SCREEN_WIDTH - 10, 10))
        screen.blit(lives_text, lives_rect)

        pygame.display.flip()

if __name__ == "__main__":
    main()
