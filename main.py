import sys

import pygame
from pygame.sprite import Group

from asset_loader import get_background_surface
from asteroid import Asteroid
from asteroidfield import AsteroidField
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from game_state_manager import GameState, GameStateManager
from hud import draw_game_over, draw_hud
from logger import log_event, log_state
from player import Player
from shot import Shot


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    background_surface = get_background_surface()
    clock = pygame.time.Clock()
    state_manager = GameStateManager()
    dt: float = 0.0
    x = SCREEN_WIDTH / 2
    y = SCREEN_HEIGHT / 2
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots: Group = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (updatable, drawable, asteroids)
    AsteroidField.containers = updatable
    Shot.containers = (updatable, drawable, shots)
    asf = AsteroidField()
    player: Player = Player(x, y)

    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and state_manager.state == GameState.GAME_OVER:
                    state_manager.restart()
                    for ast in list(asteroids):
                        ast.kill()
                    for shot in list(shots):
                        shot.kill()
                    asf.spawn_timer = 0.0
                    player.respawn()

        screen.blit(background_surface, (0, 0))

        if state_manager.state == GameState.PLAYING:
            state_manager.update(dt)
            player.invulnerable = state_manager.is_invulnerable
            updatable.update(dt)

            if not state_manager.is_invulnerable:
                for item in asteroids:
                    if player.collides_with(item):
                        log_event("player_hit")
                        has_lives = state_manager.lose_life()
                        if has_lives:
                            player.respawn()
                        else:
                            print("Game Over!")
                        break

            for item in asteroids:
                for shot in shots:
                    if shot.collides_with(item):
                        log_event("asteroid_shot")
                        state_manager.add_asteroid_score(item.radius)
                        shot.kill()
                        item.split()
                        break

        for item in drawable:
            item.draw(screen)

        draw_hud(screen, state_manager)
        if state_manager.state == GameState.GAME_OVER:
            draw_game_over(screen, state_manager)

        pygame.display.flip()
        dt = clock.tick(60) / 1000

    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")


if __name__ == "__main__":
    main()
