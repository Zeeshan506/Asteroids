import pytest
import pygame
from asteroid import Asteroid
from constants import SHOT_RADIUS
from shot import Shot


def test_shot_initialization():
    shot = Shot(120.0, 340.0)
    assert shot.position.x == pytest.approx(120.0)
    assert shot.position.y == pytest.approx(340.0)
    assert shot.radius == SHOT_RADIUS
    assert shot.velocity.x == 0.0
    assert shot.velocity.y == 0.0


def test_shot_movement_updates_position():
    shot = Shot(100.0, 100.0)
    shot.velocity = pygame.Vector2(300.0, -150.0)
    dt = 0.2
    shot.update(dt)

    assert shot.position.x == pytest.approx(100.0 + (300.0 * 0.2))
    assert shot.position.y == pytest.approx(100.0 + (-150.0 * 0.2))


def test_shot_zero_dt_preserves_position():
    shot = Shot(50.0, 50.0)
    shot.velocity = pygame.Vector2(500.0, 500.0)
    shot.update(0.0)

    assert shot.position.x == pytest.approx(50.0)
    assert shot.position.y == pytest.approx(50.0)


def test_shot_collides_with_asteroid():
    shot = Shot(100.0, 100.0)
    asteroid_colliding = Asteroid(110.0, 100.0, 20.0)
    asteroid_far = Asteroid(300.0, 300.0, 20.0)

    # distance to colliding = 10 < 5 + 20 (25)
    assert shot.collides_with(asteroid_colliding)
    # distance to far = 282.8 > 25
    assert not shot.collides_with(asteroid_far)


def test_shot_kill_removes_from_groups():
    group = pygame.sprite.Group()
    Shot.containers = (group,)

    shot = Shot(200.0, 200.0)
    assert shot in group
    shot.kill()
    assert shot not in group
