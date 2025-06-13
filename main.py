import sys
import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from bomb import Bomb
from explosion import Explosion

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

    dt = 0

    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Update game objects
        updatable.update(dt)
        asteroid_field.update(dt)

        # Collision detection
        for asteroid in asteroids:
            if asteroid.collides_with(player):
                player.lives -= 1
                if player.lives <= 0:
                    print("Game Over!")
                    pygame.quit()
                    sys.exit()
                else:
                    # Reset player position and rotation after collision
                    player.position = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                    player.rotation = 0

            for shot in shots:
                if asteroid.collides_with(shot):
                    shot.kill()
                    asteroid.split()

        # Draw everything
        screen.blit(background, (0, 0))

        for obj in drawable:
            obj.draw(screen)

        # Draw UI: Score and Lives
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {player.score if hasattr(player, 'score') else 0}", True, (255, 255, 255))
        lives_text = font.render(f"Lives: {player.lives}", True, (255, 255, 255))

        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (SCREEN_WIDTH - lives_text.get_width() - 10, 10))

        pygame.display.flip()

        dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()
