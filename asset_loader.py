"""Asset loader module for caching, scaling, and managing game textures."""

from pathlib import Path
import pygame

from constants import PLAYER_RADIUS, SCREEN_HEIGHT, SCREEN_WIDTH

ASSETS_DIR: Path = Path(__file__).resolve().parent / "assets"
_IMAGE_CACHE: dict[tuple[str, tuple[int, int] | None], pygame.Surface] = {}


def get_assets_dir() -> Path:
    """Return the absolute directory path where game assets reside."""
    return ASSETS_DIR


def clear_cache() -> None:
    """Clear cached image surfaces (useful for testing and memory resets)."""
    _IMAGE_CACHE.clear()


def load_image(filename: str, size: tuple[int, int] | None = None) -> pygame.Surface:
    """Load an image from the assets directory with optional scaling and caching.

    Args:
        filename: Relative filename within assets/ or absolute path to image.
        size: Optional (width, height) tuple to scale the loaded surface to.

    Returns:
        pygame.Surface: The loaded (and scaled) image surface.

    Raises:
        FileNotFoundError: If the specified image asset cannot be found.
    """
    path = Path(filename)
    if not path.is_absolute():
        path = ASSETS_DIR / filename

    if not path.is_file():
        raise FileNotFoundError(f"Asset file not found at: {path}")

    cache_key = (str(path.resolve()), size)
    if cache_key in _IMAGE_CACHE:
        return _IMAGE_CACHE[cache_key]

    raw_surface = pygame.image.load(str(path))

    # Defensive conversion: only convert when a display surface is active
    if pygame.display.get_surface() is not None:
        if "background" in path.name.lower():
            surface = raw_surface.convert()
        else:
            surface = raw_surface.convert_alpha()
    else:
        surface = raw_surface

    if size is not None:
        try:
            surface = pygame.transform.smoothscale(surface, size)
        except Exception:
            surface = pygame.transform.scale(surface, size)

    _IMAGE_CACHE[cache_key] = surface
    return surface


def get_player_surface() -> pygame.Surface:
    """Return the scaled spaceship sprite surface."""
    diameter = int(PLAYER_RADIUS * 2)
    return load_image("spaceship.png", (diameter, diameter))


def get_asteroid_surface(radius: float) -> pygame.Surface:
    """Return the appropriate tier-scaled asteroid sprite surface.

    Tier mapping based on radius:
    - radius > 40: asteriods_big.png (Tier 3)
    - 20 < radius <= 40: asteriods_mid.png (Tier 2)
    - radius <= 20: asteriods_small.png (Tier 1)
    """
    if radius > 40:
        asset_name = "asteriods_big.png"
    elif radius > 20:
        asset_name = "asteriods_mid.png"
    else:
        asset_name = "asteriods_small.png"

    diameter = int(round(radius * 2))
    return load_image(asset_name, (diameter, diameter))


def get_background_surface(
    size: tuple[int, int] = (SCREEN_WIDTH, SCREEN_HEIGHT)
) -> pygame.Surface:
    """Return the scaled background surface for full screen display."""
    return load_image("background.png", size)
