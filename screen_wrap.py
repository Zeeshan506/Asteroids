"""Screen boundary wrap-around and bounds detection module."""

import pygame

from constants import SCREEN_HEIGHT, SCREEN_WIDTH


def wrap_position(
    position: pygame.Vector2,
    width: int = SCREEN_WIDTH,
    height: int = SCREEN_HEIGHT,
    margin: float = 0.0,
) -> pygame.Vector2:
    """Wrap a 2D coordinate vector smoothly across screen boundaries.

    Args:
        position: Current position vector.
        width: Screen width in pixels.
        height: Screen height in pixels.
        margin: Optional buffer margin allowing entities to cross before wrapping.

    Returns:
        pygame.Vector2: Wrapped coordinate position.
    """
    wrapped = pygame.Vector2(position.x, position.y)

    if wrapped.x < -margin:
        wrapped.x = width + margin
    elif wrapped.x > width + margin:
        wrapped.x = -margin

    if wrapped.y < -margin:
        wrapped.y = height + margin
    elif wrapped.y > height + margin:
        wrapped.y = -margin

    return wrapped


def is_out_of_bounds(
    position: pygame.Vector2,
    width: int = SCREEN_WIDTH,
    height: int = SCREEN_HEIGHT,
    margin: float = 20.0,
) -> bool:
    """Return True if a position is strictly beyond the screen boundaries plus margin.

    Args:
        position: Coordinate to test.
        width: Screen width in pixels.
        height: Screen height in pixels.
        margin: Buffer distance outside screen boundaries.

    Returns:
        bool: True if off-screen, False otherwise.
    """
    return (
        position.x < -margin
        or position.x > width + margin
        or position.y < -margin
        or position.y > height + margin
    )
