import os
import pytest

# Ensure Pygame runs in headless mode across all test runs
os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

import pygame

from asteroid import Asteroid
from asteroidfield import AsteroidField
from player import Player
from shot import Shot


@pytest.fixture(scope="session", autouse=True)
def init_headless_pygame():
    """Initializes Pygame in headless mode once per test session."""
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture(autouse=True)
def clean_sprite_containers():
    """Ensures sprite class containers are clean before and after each test."""
    for cls in (Player, Asteroid, AsteroidField, Shot):
        if hasattr(cls, "containers"):
            delattr(cls, "containers")
    yield
    for cls in (Player, Asteroid, AsteroidField, Shot):
        if hasattr(cls, "containers"):
            delattr(cls, "containers")
