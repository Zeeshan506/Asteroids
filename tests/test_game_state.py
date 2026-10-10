"""Unit and regression tests for GameStateManager, Player respawn, and HUD rendering."""

import pytest
import pygame

from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from game_state_manager import GameState, GameStateManager
from hud import clear_font_cache, draw_game_over, draw_hud, get_font
from player import Player


@pytest.fixture(autouse=True)
def reset_hud():
    """Ensure font cache is clean before and after each test."""
    clear_font_cache()
    yield
    clear_font_cache()


def test_initial_game_state():
    """AC-2.2: Verify initial state starts with 3 lives, score 0, and PLAYING state."""
    manager = GameStateManager()
    assert manager.state == GameState.PLAYING
    assert manager.score == 0
    assert manager.lives == 3
    assert manager.invulnerability_timer == 0.0
    assert manager.is_invulnerable is False


@pytest.mark.parametrize(
    "radius,expected_points",
    [
        (60.0, 20),   # Tier 3 (Large)
        (50.0, 20),   # Tier 3 (Large)
        (40.0, 50),   # Tier 2 (Medium)
        (30.0, 50),   # Tier 2 (Medium)
        (20.0, 100),  # Tier 1 (Small)
        (10.0, 100),  # Tier 1 (Small)
    ],
)
def test_asteroid_tiered_scoring(radius, expected_points):
    """AC-2.1: Verify destroying asteroids awards points matching radius tiers."""
    manager = GameStateManager()
    awarded = manager.add_asteroid_score(radius)
    assert awarded == expected_points
    assert manager.score == expected_points


def test_cumulative_score_addition():
    """AC-2.1: Verify sequential asteroid destructions accumulate score correctly."""
    manager = GameStateManager()
    manager.add_asteroid_score(60.0)  # +20 -> 20
    manager.add_asteroid_score(40.0)  # +50 -> 70
    manager.add_asteroid_score(20.0)  # +100 -> 170
    assert manager.score == 170


def test_lose_life_decrements_and_activates_invulnerability():
    """AC-2.2, AC-2.3: Verify colliding decrements exactly 1 life and starts 2.0s invulnerability."""
    manager = GameStateManager()
    has_lives = manager.lose_life()

    assert has_lives is True
    assert manager.lives == 2
    assert manager.invulnerability_timer == pytest.approx(2.0)
    assert manager.is_invulnerable is True
    assert manager.state == GameState.PLAYING


def test_invulnerability_timer_decrement():
    """AC-2.3: Verify invulnerability countdown decrements smoothly by delta time."""
    manager = GameStateManager()
    manager.lose_life()

    manager.update(0.5)
    assert manager.invulnerability_timer == pytest.approx(1.5)
    assert manager.is_invulnerable is True

    manager.update(1.5)
    assert manager.invulnerability_timer == pytest.approx(0.0)
    assert manager.is_invulnerable is False

    # Additional update does not drop below 0
    manager.update(0.1)
    assert manager.invulnerability_timer == pytest.approx(0.0)


def test_collisions_ignored_during_invulnerability():
    """AC-2.4: Verify collisions while invulnerable are completely ignored."""
    manager = GameStateManager()
    manager.lose_life()  # lives -> 2, invulnerable for 2.0s

    assert manager.is_invulnerable is True
    # Subsequent collision attempt during invulnerability
    result = manager.lose_life()
    assert result is False
    assert manager.lives == 2  # Lives remain unchanged


def test_lives_exhaustion_transitions_to_game_over():
    """AC-2.5: Verify depleting all 3 lives transitions state to GAME_OVER."""
    manager = GameStateManager()

    # Life 1 lost -> 2 remaining
    assert manager.lose_life() is True
    assert manager.lives == 2
    manager.update(2.1)  # expire invulnerability

    # Life 2 lost -> 1 remaining
    assert manager.lose_life() is True
    assert manager.lives == 1
    manager.update(2.1)  # expire invulnerability

    # Life 3 lost -> 0 remaining -> GAME_OVER
    assert manager.lose_life() is False
    assert manager.lives == 0
    assert manager.state == GameState.GAME_OVER
    assert manager.invulnerability_timer == pytest.approx(0.0)

    # Further calls in GAME_OVER do nothing
    assert manager.lose_life() is False
    assert manager.lives == 0


def test_restart_resets_full_state():
    """AC-2.6: Verify restart restores lives, score, timers, and state."""
    manager = GameStateManager()
    manager.add_asteroid_score(60.0)
    manager.lose_life()
    manager.update(2.1)
    manager.lose_life()
    manager.update(2.1)
    manager.lose_life()
    assert manager.state == GameState.GAME_OVER

    manager.restart()
    assert manager.state == GameState.PLAYING
    assert manager.score == 0
    assert manager.lives == 3
    assert manager.invulnerability_timer == pytest.approx(0.0)
    assert manager.is_invulnerable is False


def test_player_respawn_repositions_to_center():
    """AC-2.3: Verify Player.respawn resets coordinates to screen center and clears rotation."""
    player = Player(10.0, 20.0)
    player.rotation = 120.0
    player.shot_countdown_timer = 0.25

    player.respawn()
    assert player.position.x == pytest.approx(SCREEN_WIDTH / 2)
    assert player.position.y == pytest.approx(SCREEN_HEIGHT / 2)
    assert player.rotation == pytest.approx(0.0)
    assert player.shot_countdown_timer == pytest.approx(0.0)
    assert player.invulnerable is True


def test_player_draw_flicker_during_invulnerability():
    """AC-2.4: Verify Player.draw executes cleanly and handles flicker branch."""
    player = Player(100.0, 100.0)
    target_surf = pygame.Surface((400, 400))

    player.invulnerable = True
    player.draw(target_surf)
    player.draw(None)  # Defensive none guard

    player.invulnerable = False
    player.draw(target_surf)


def test_hud_rendering():
    """AC-2.7: Verify draw_hud and draw_game_over render cleanly to surface."""
    manager = GameStateManager()
    manager.add_asteroid_score(40.0)
    screen_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Test playing HUD
    draw_hud(screen_surf, manager)
    draw_hud(None, manager)

    # Test game over overlay
    manager.state = GameState.GAME_OVER
    draw_game_over(screen_surf, manager)
    draw_game_over(None, manager)


def test_get_font_caching():
    """Verify font instances are cached per requested point size."""
    f1 = get_font(24)
    f2 = get_font(24)
    assert f1 is f2
    f3 = get_font(32)
    assert f1 is not f3
