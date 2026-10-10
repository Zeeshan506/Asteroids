"""Laser shot entity module."""

import pygame

from circleshape import CircleShape
from constants import SHOT_RADIUS
from screen_wrap import is_out_of_bounds


class Shot(CircleShape):
    """Fired projectile moving at fixed velocity and removed when leaving screen."""

    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y, SHOT_RADIUS)

    def update(self, dt: float) -> None:
        """Advance position along velocity and despawn when exiting screen."""
        self.position += self.velocity * dt
        if is_out_of_bounds(self.position):
            self.kill()

    def draw(self, screen: pygame.Surface) -> None:
        """Draw laser shot as white circle."""
        if screen is not None:
            pygame.draw.circle(screen, "white", self.position, self.radius)
