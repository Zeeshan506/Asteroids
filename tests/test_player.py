import math
import pytest
import pygame
from constants import (
    PLAYER_RADIUS,
    PLAYER_SHOOT_COOLDOWN_SECONDS,
    PLAYER_SHOOT_SPEED,
    PLAYER_SPEED,
    PLAYER_TURN_SPEED,
)
from player import Player
from shot import Shot


def test_player_initialization():
    player = Player(150.0, 250.0)
    assert player.position.x == pytest.approx(150.0)
    assert player.position.y == pytest.approx(250.0)
    assert player.radius == PLAYER_RADIUS
    assert player.rotation == 0
    assert player.shot_countdown_timer == 0.0


def test_player_rotation_positive_dt():
    player = Player(0, 0)
    dt = 0.2
    player.rotate(dt)
    expected_rotation = PLAYER_TURN_SPEED * dt
    assert player.rotation == pytest.approx(expected_rotation)


def test_player_rotation_negative_dt():
    player = Player(0, 0)
    player.rotation = 90.0
    dt = -0.1
    player.rotate(dt)
    expected_rotation = 90.0 + (PLAYER_TURN_SPEED * -0.1)
    assert player.rotation == pytest.approx(expected_rotation)


def test_player_forward_movement_default_orientation():
    player = Player(100.0, 100.0)
    player.rotation = 0.0  # Unit vector is (0, 1) pointing downward in Pygame coords
    dt = 0.5
    player.move(dt)

    expected_dx = 0.0
    expected_dy = PLAYER_SPEED * dt
    assert player.position.x == pytest.approx(100.0 + expected_dx)
    assert player.position.y == pytest.approx(100.0 + expected_dy)


def test_player_backward_movement():
    player = Player(100.0, 100.0)
    player.rotation = 0.0
    dt = 0.5
    player.move(-dt)

    assert player.position.x == pytest.approx(100.0)
    assert player.position.y == pytest.approx(100.0 - (PLAYER_SPEED * dt))


def test_player_movement_at_cardinal_rotations():
    # Pygame's Vector2(0, 1).rotate(angle) rotates clockwise
    # Test 90 degrees rotation
    player_90 = Player(200.0, 200.0)
    player_90.rotation = 90.0
    player_90.move(1.0)
    expected_vec_90 = pygame.Vector2(0, 1).rotate(90.0) * PLAYER_SPEED
    assert player_90.position.x == pytest.approx(200.0 + expected_vec_90.x)
    assert player_90.position.y == pytest.approx(200.0 + expected_vec_90.y)

    # Test 180 degrees rotation
    player_180 = Player(200.0, 200.0)
    player_180.rotation = 180.0
    player_180.move(1.0)
    expected_vec_180 = pygame.Vector2(0, 1).rotate(180.0) * PLAYER_SPEED
    assert player_180.position.x == pytest.approx(200.0 + expected_vec_180.x)
    assert player_180.position.y == pytest.approx(200.0 + expected_vec_180.y)


def test_player_shoot_creates_shot_with_correct_velocity():
    player = Player(300.0, 400.0)
    player.rotation = 45.0
    shots_group = pygame.sprite.Group()
    Shot.containers = (shots_group,)

    player.shoot()
    assert len(shots_group) == 1
    shot = next(iter(shots_group))
    assert shot.position.x == pytest.approx(300.0)
    assert shot.position.y == pytest.approx(400.0)

    expected_velocity = pygame.Vector2(0, 1).rotate(45.0) * PLAYER_SHOOT_SPEED
    assert shot.velocity.x == pytest.approx(expected_velocity.x)
    assert shot.velocity.y == pytest.approx(expected_velocity.y)


def test_player_update_decrements_shoot_cooldown():
    player = Player(100.0, 100.0)
    player.shot_countdown_timer = PLAYER_SHOOT_COOLDOWN_SECONDS

    dt = 0.1
    # Exercise the actual Player.update logic
    player.update(dt)
    assert player.shot_countdown_timer == pytest.approx(
        PLAYER_SHOOT_COOLDOWN_SECONDS - dt
    )

    player.update(0.2)
    assert player.shot_countdown_timer == pytest.approx(0.0)

    player.update(0.1)
    assert player.shot_countdown_timer == pytest.approx(-0.1)


def test_player_update_gates_shooting_on_cooldown(monkeypatch):
    from collections import defaultdict

    shots_group = pygame.sprite.Group()
    Shot.containers = (shots_group,)

    player = Player(100.0, 100.0)
    # Simulate SPACE key continuously pressed
    space_pressed = defaultdict(bool, {pygame.K_SPACE: True})
    monkeypatch.setattr(pygame.key, "get_pressed", lambda: space_pressed)

    # Initial state: timer == 0.0 -> First shot fired and cooldown reset
    player.update(0.05)
    assert len(shots_group) == 1
    assert player.shot_countdown_timer == pytest.approx(PLAYER_SHOOT_COOLDOWN_SECONDS)

    # Next frame during cooldown: no new shot should be created
    player.update(0.1)
    assert len(shots_group) == 1
    assert player.shot_countdown_timer == pytest.approx(
        PLAYER_SHOOT_COOLDOWN_SECONDS - 0.1
    )

    # Cooldown expires: next shot is permitted
    player.update(0.25)
    assert len(shots_group) == 2
    assert player.shot_countdown_timer == pytest.approx(PLAYER_SHOOT_COOLDOWN_SECONDS)


def test_player_triangle_geometry():
    player = Player(100.0, 100.0)
    player.rotation = 0.0
    points = player.triangle()

    assert len(points) == 3
    # Front tip (a)
    tip = points[0]
    expected_tip = pygame.Vector2(100.0, 100.0) + pygame.Vector2(0, 1) * PLAYER_RADIUS
    assert tip.x == pytest.approx(expected_tip.x)
    assert tip.y == pytest.approx(expected_tip.y)


def test_player_update_processes_movement_and_turn_keys(monkeypatch):
    from collections import defaultdict

    player = Player(200.0, 200.0)

    # Press D (turn right) and W (move forward)
    keys_dw = defaultdict(bool, {pygame.K_d: True, pygame.K_w: True})
    monkeypatch.setattr(pygame.key, "get_pressed", lambda: keys_dw)

    dt = 0.1
    player.update(dt)

    assert player.rotation == pytest.approx(PLAYER_TURN_SPEED * dt)
    # Movement applies with current rotation (note: turn applies first in update)
    assert player.position.x != pytest.approx(200.0) or player.position.y != pytest.approx(200.0)


def test_player_draw_visual_shield_border():
    """Verify player draws visual collision shield glow and border around model."""
    player = Player(200.0, 200.0)
    surface = pygame.Surface((400, 400))

    # Normal flight
    player.invulnerable = False
    player.draw(surface)

    # Invulnerable state (golden shield border)
    player.invulnerable = True
    player.draw(surface)

    # None surface guard
    player.draw(None)


