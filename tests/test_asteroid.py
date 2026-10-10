import math
import pytest
import pygame
from asteroid import Asteroid
from constants import ASTEROID_MAX_RADIUS, ASTEROID_MIN_RADIUS


def test_asteroid_initialization():
    asteroid = Asteroid(200.0, 300.0, 40.0)
    assert asteroid.position.x == pytest.approx(200.0)
    assert asteroid.position.y == pytest.approx(300.0)
    assert asteroid.radius == 40.0
    assert asteroid.velocity.x == 0.0
    assert asteroid.velocity.y == 0.0


def test_asteroid_update_moves_by_velocity():
    asteroid = Asteroid(100.0, 100.0, 40.0)
    asteroid.velocity = pygame.Vector2(50.0, -25.0)
    dt = 0.5
    asteroid.update(dt)

    assert asteroid.position.x == pytest.approx(125.0)
    assert asteroid.position.y == pytest.approx(87.5)


def test_asteroid_split_spawns_two_children_with_reduced_radius():
    group = pygame.sprite.Group()
    Asteroid.containers = (group,)

    initial_radius = 40.0
    parent = Asteroid(250.0, 350.0, initial_radius)
    parent.velocity = pygame.Vector2(100.0, 0.0)

    assert len(group) == 1
    assert parent in group

    parent.split()

    # Parent must be killed
    assert parent not in group
    # Two children must be created
    assert len(group) == 2

    children = list(group)
    for child in children:
        assert isinstance(child, Asteroid)
        assert child.radius == pytest.approx(initial_radius - ASTEROID_MIN_RADIUS)
        assert child.position.x == pytest.approx(250.0)
        assert child.position.y == pytest.approx(350.0)
        # Child speed must be scaled by 1.2
        assert child.velocity.length() == pytest.approx(100.0 * 1.2, rel=1e-3)

    # Angles of the two children must diverge
    angle_between = children[0].velocity.angle_to(children[1].velocity)
    # Since random angle is in [20, 50], angle difference is between 40 and 100 degrees
    assert 39.0 <= abs(angle_between) <= 101.0


def test_asteroid_split_boundary_at_minimum_radius():
    group = pygame.sprite.Group()
    Asteroid.containers = (group,)

    # Asteroid at ASTEROID_MIN_RADIUS must be destroyed without children
    min_asteroid = Asteroid(100.0, 100.0, ASTEROID_MIN_RADIUS)
    min_asteroid.velocity = pygame.Vector2(40.0, 40.0)
    assert len(group) == 1

    min_asteroid.split()

    assert min_asteroid not in group
    assert len(group) == 0


def test_asteroid_split_boundary_below_minimum_radius():
    group = pygame.sprite.Group()
    Asteroid.containers = (group,)

    small_asteroid = Asteroid(50.0, 50.0, ASTEROID_MIN_RADIUS - 5)
    small_asteroid.split()

    assert small_asteroid not in group
    assert len(group) == 0


def test_asteroid_split_full_lifecycle_from_max_radius():
    group = pygame.sprite.Group()
    Asteroid.containers = (group,)

    # Tier 3 (Max radius = 60)
    tier3 = Asteroid(500.0, 500.0, ASTEROID_MAX_RADIUS)
    tier3.velocity = pygame.Vector2(50.0, 50.0)
    tier3.split()

    # Should have 2 tier 2 asteroids (radius = 40)
    assert len(group) == 2
    for a in group:
        assert a.radius == pytest.approx(40.0)

    # Split one tier 2 asteroid
    tier2 = next(iter(group))
    tier2.split()
    # Now: 1 tier-2 remaining + 2 tier-1 spawned = 3 total
    assert len(group) == 3

    # Count radii
    radii = [a.radius for a in group]
    assert radii.count(40.0) == 1
    assert radii.count(20.0) == 2
