import math
import pytest
from circleshape import CircleShape


def test_collision_overlapping_circles():
    c1 = CircleShape(100, 100, 20)
    c2 = CircleShape(120, 100, 20)
    # distance = 20, r1 + r2 = 40 -> 20 < 40 -> collides
    assert c1.collides_with(c2)
    assert c2.collides_with(c1)


def test_collision_concentric_circles():
    c1 = CircleShape(200, 200, 30)
    c2 = CircleShape(200, 200, 10)
    # distance = 0, r1 + r2 = 40 -> 0 < 40 -> collides
    assert c1.collides_with(c2)
    assert c2.collides_with(c1)


def test_collision_tangent_circles_touching_externally():
    c1 = CircleShape(0, 0, 15)
    c2 = CircleShape(30, 0, 15)
    # distance = 30, r1 + r2 = 30 -> 30 < 30 is False (tangent touch)
    assert not c1.collides_with(c2)
    assert not c2.collides_with(c1)


def test_collision_nearly_touching_inside_boundary():
    c1 = CircleShape(0, 0, 15)
    c2 = CircleShape(29.99, 0, 15)
    # distance = 29.99 < 30 -> collides
    assert c1.collides_with(c2)
    assert c2.collides_with(c1)


def test_collision_nearly_touching_outside_boundary():
    c1 = CircleShape(0, 0, 15)
    c2 = CircleShape(30.01, 0, 15)
    # distance = 30.01 < 30 is False -> disjoint
    assert not c1.collides_with(c2)
    assert not c2.collides_with(c1)


def test_collision_disjoint_distant_circles():
    c1 = CircleShape(50, 50, 10)
    c2 = CircleShape(500, 500, 10)
    assert not c1.collides_with(c2)
    assert not c2.collides_with(c1)


def test_collision_zero_distance_identical_coordinates():
    # Edge case: zero distance between circle centers must not raise ZeroDivisionError
    c1 = CircleShape(320, 240, 25)
    c2 = CircleShape(320, 240, 25)
    assert c1.collides_with(c2)
    assert c2.collides_with(c1)


def test_collision_zero_radius_point_inside_circle():
    point = CircleShape(100, 100, 0)
    circle = CircleShape(105, 100, 10)
    # distance = 5, r1 + r2 = 10 -> 5 < 10 -> collides
    assert point.collides_with(circle)
    assert circle.collides_with(point)


def test_collision_zero_radius_point_outside_circle():
    point = CircleShape(100, 100, 0)
    circle = CircleShape(120, 100, 10)
    # distance = 20, r1 + r2 = 10 -> 20 < 10 is False
    assert not point.collides_with(circle)
    assert not circle.collides_with(point)


def test_collision_both_zero_radius_at_same_point():
    p1 = CircleShape(50, 50, 0)
    p2 = CircleShape(50, 50, 0)
    # distance = 0, r1 + r2 = 0 -> 0 < 0 is False
    assert not p1.collides_with(p2)
    assert not p2.collides_with(p1)


def test_collision_diagonal_pythagorean_distance():
    # 3-4-5 triangle scaled: dx = 30, dy = 40 -> distance = 50
    c1 = CircleShape(0, 0, 25)
    c2_colliding = CircleShape(30, 40, 26)  # sum = 51 > 50
    c2_disjoint = CircleShape(30, 40, 24)   # sum = 49 < 50

    assert c1.collides_with(c2_colliding)
    assert not c1.collides_with(c2_disjoint)


def test_collision_negative_coordinates():
    c1 = CircleShape(-100, -200, 15)
    c2 = CircleShape(-110, -200, 15)
    # distance = 10 < 30 -> collides
    assert c1.collides_with(c2)
    assert c2.collides_with(c1)
