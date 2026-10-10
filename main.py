import sys
from typing import Optional

import pygame
from pygame.sprite import Group

from asset_loader import get_background_surface
from asteroid import Asteroid
from asteroidfield import AsteroidField
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from game_state_manager import GameState, GameStateManager
from hud import draw_game_over, draw_hud, draw_paused
from logger import log_event, log_state
from menu import (
    draw_audio_settings,
    draw_leaderboard,
    draw_menu,
    handle_audio_key,
    handle_leaderboard_key,
    handle_menu_key,
)
from player import Player
from shot import Shot
from sound_manager import SoundManager


def reset_game_entities(
    player: Player,
    asteroids: Group,
    shots: Group,
    asteroid_field: AsteroidField,
) -> None:
    """Clear active projectiles and asteroids and center player."""
    for ast in list(asteroids):
        ast.kill()
    for shot in list(shots):
        shot.kill()
    asteroid_field.spawn_timer = 0.0
    player.respawn()


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    background_surface = get_background_surface()
    clock = pygame.time.Clock()
    sound_manager = SoundManager()
    state_manager = GameStateManager(initial_state=GameState.MENU)
    selected_menu_index: int = 0
    selected_audio_index: int = 0
    dt: float = 0.0

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots: Group = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (updatable, drawable, asteroids)
    AsteroidField.containers = updatable
    Shot.containers = (updatable, drawable, shots)

    asf = AsteroidField()
    player: Player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, sound_manager=sound_manager)

    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:
                if state_manager.state == GameState.MENU:
                    if event.key == pygame.K_m:
                        sound_manager.toggle_mute()
                    selected_menu_index, action = handle_menu_key(event.key, selected_menu_index)
                    if action == "START GAME":
                        state_manager.start_game()
                        reset_game_entities(player, asteroids, shots, asf)
                    elif action == "LEADERBOARD":
                        state_manager.state = GameState.LEADERBOARD
                    elif action == "AUDIO SETTINGS":
                        state_manager.state = GameState.AUDIO_SETTINGS
                    elif action == "QUIT":
                        return

                elif state_manager.state == GameState.AUDIO_SETTINGS:
                    selected_audio_index, action = handle_audio_key(
                        event.key, selected_audio_index, sound_manager
                    )
                    if action == "MENU":
                        state_manager.state = GameState.MENU

                elif state_manager.state == GameState.LEADERBOARD:
                    action = handle_leaderboard_key(event.key)
                    if action == "MENU":
                        state_manager.state = GameState.MENU

                elif state_manager.state in (GameState.PLAYING, GameState.PAUSED):
                    if event.key == pygame.K_p:
                        state_manager.toggle_pause()
                    elif event.key == pygame.K_m:
                        sound_manager.toggle_mute()
                    elif event.key == pygame.K_LEFTBRACKET:
                        sound_manager.change_music_volume(-0.05)
                    elif event.key == pygame.K_RIGHTBRACKET:
                        sound_manager.change_music_volume(0.05)
                    elif event.key == pygame.K_MINUS:
                        sound_manager.change_sfx_volume(-0.05)
                    elif event.key in (pygame.K_EQUALS, pygame.K_PLUS):
                        sound_manager.change_sfx_volume(0.05)
                    elif event.key == pygame.K_ESCAPE:
                        state_manager.state = GameState.MENU

                elif state_manager.state == GameState.GAME_OVER:
                    if event.key == pygame.K_r:
                        state_manager.restart()
                        reset_game_entities(player, asteroids, shots, asf)
                    elif event.key in (pygame.K_ESCAPE, pygame.K_m):
                        state_manager.state = GameState.MENU
                    elif event.key == pygame.K_l:
                        state_manager.state = GameState.LEADERBOARD

        screen.blit(background_surface, (0, 0))

        if state_manager.state == GameState.PLAYING:
            state_manager.update(dt)
            player.invulnerable = state_manager.is_invulnerable
            updatable.update(dt)

            if not state_manager.is_invulnerable:
                for item in asteroids:
                    if player.collides_with(item):
                        log_event("player_hit")
                        sound_manager.play_player_hit()
                        has_lives = state_manager.lose_life()
                        if has_lives:
                            player.respawn()
                        break

            for item in asteroids:
                for shot in shots:
                    if shot.collides_with(item):
                        log_event("asteroid_shot")
                        sound_manager.play_asteroid_hit()
                        state_manager.add_asteroid_score(item.radius)
                        shot.kill()
                        item.split()
                        break

        if state_manager.state in (GameState.PLAYING, GameState.PAUSED, GameState.GAME_OVER):
            for item in drawable:
                item.draw(screen)
            draw_hud(screen, state_manager)

        if state_manager.state == GameState.MENU:
            draw_menu(screen, selected_menu_index)
        elif state_manager.state == GameState.LEADERBOARD:
            top_scores = state_manager.leaderboard.get_top_scores(10)
            draw_leaderboard(screen, top_scores)
        elif state_manager.state == GameState.AUDIO_SETTINGS:
            draw_audio_settings(screen, sound_manager, selected_audio_index)
        elif state_manager.state == GameState.PAUSED:
            draw_paused(screen, sound_manager)
        elif state_manager.state == GameState.GAME_OVER:
            draw_game_over(screen, state_manager)

        pygame.display.flip()
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
