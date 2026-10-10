"""Tests for screen wrap-around and projectile boundary logic."""

from collections import defaultdict
import pytest
import pygame

from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from player import Player
from screen_wrap import is_out_of_bounds, wrap_position
from shot import Shot


def test_wrap_position_horizontal_bounds():
    """AC-3.4: Verify horizontal coordinate wrapping."""
    # Exiting right edge
    pos_right = pygame.Vector2(SCREEN_WIDTH + 5, 300)
    wrapped_right = wrap_position(pos_right)
    assert wrapped_right.x == pytest.approx(0.0)
    assert wrapped_right.y == pytest.approx(300.0)

    # Exiting left edge
    pos_left = pygame.Vector2(-5, 300)
    wrapped_left = wrap_position(pos_left)
    assert wrapped_left.x == pytest.approx(SCREEN_WIDTH)
    assert wrapped_left.y == pytest.approx(300.0)


def test_wrap_position_vertical_bounds():
    """AC-3.4: Verify vertical coordinate wrapping."""
    # Exiting bottom edge
    pos_bottom = pygame.Vector2(400, SCREEN_HEIGHT + 10)
    wrapped_bottom = wrap_position(pos_bottom)
    assert wrapped_bottom.x == pytest.approx(400.0)
    assert wrapped_bottom.y == pytest.approx(0.0)

    # Exiting top edge
    pos_top = pygame.Vector2(400, -10)
    wrapped_top = wrap_position(pos_top)
    assert wrapped_top.x == pytest.approx(400.0)
    assert wrapped_top.y == pytest.approx(SCREEN_HEIGHT)


def test_wrap_position_within_bounds_unchanged():
    """AC-3.4: Positions within screen bounds remain unaltered."""
    pos_center = pygame.Vector2(500, 350)
    wrapped = wrap_position(pos_center)
    assert wrapped.x == pytest.approx(500.0)
    assert wrapped.y == pytest.approx(350.0)


def test_player_updates_wrap_position(monkeypatch):
    """AC-3.4: Player.update wraps spaceship position when flying beyond boundaries."""
    player = Player(SCREEN_WIDTH + 10, 200)
    monkeypatch.setattr(pygame.key, "get_pressed", lambda: defaultdict(bool))

    player.update(0.1)
    assert player.position.x == pytest.approx(0.0)
    assert player.position.y == pytest.approx(200.0)


def test_is_out_of_bounds_detection():
    """AC-3.4: Verify detection of out-of-bounds positions."""
    assert is_out_of_bounds(pygame.Vector2(100, 100), margin=20.0) is False
    assert is_out_of_bounds(pygame.Vector2(-25, 100), margin=20.0) is True
    assert is_out_of_bounds(pygame.Vector2(SCREEN_WIDTH + 25, 100), margin=20.0) is True
    assert is_out_of_bounds(pygame.Vector2(100, -25), margin=20.0) is True
    assert is_out_of_bounds(pygame.Vector2(100, SCREEN_HEIGHT + 25), margin=20.0) is True


def test_shot_despawns_when_out_of_bounds():
    """AC-3.4: Shot entity despawns (kills itself) when exiting screen margin."""
    shots_group = pygame.sprite.Group()
    Shot.containers = (shots_group,)

    shot = Shot(SCREEN_WIDTH + 15, 300)
    shot.velocity = pygame.Vector2(100, 0)
    assert shot in shots_group

    # Update advances shot further out of bounds (margin=20.0)
    shot.update(0.2)
    assert shot not in shots_group
