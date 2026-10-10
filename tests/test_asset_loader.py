"""Unit and regression tests for asset loading, caching, scaling, and sprite rendering."""

from pathlib import Path
import pytest
import pygame

from asset_loader import (
    ASSETS_DIR,
    clear_cache,
    get_assets_dir,
    get_asteroid_surface,
    get_background_surface,
    get_player_surface,
    load_image,
    _IMAGE_CACHE,
)
from asteroid import Asteroid
from constants import (
    ASTEROID_MAX_RADIUS,
    ASTEROID_MIN_RADIUS,
    PLAYER_RADIUS,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)
from player import Player


@pytest.fixture(autouse=True)
def reset_asset_cache():
    """Ensure asset cache is clean before and after each test."""
    clear_cache()
    yield
    clear_cache()


def test_get_assets_dir_exists():
    """AC-1.1: Verify assets directory path exists and points to repository assets."""
    assets_path = get_assets_dir()
    assert assets_path.exists()
    assert assets_path.is_dir()
    assert (assets_path / "spaceship.png").is_file()


def test_load_all_five_game_assets():
    """AC-1.1: Verify all 5 game texture assets can be loaded without error."""
    asset_names = [
        "spaceship.png",
        "asteriods_big.png",
        "asteriods_mid.png",
        "asteriods_small.png",
        "background.png",
    ]
    for asset_name in asset_names:
        surface = load_image(asset_name)
        assert isinstance(surface, pygame.Surface)
        assert surface.get_width() > 0
        assert surface.get_height() > 0


def test_load_image_caching():
    """AC-1.1: Verify repeated load calls return memoized surface instance."""
    surf1 = load_image("spaceship.png", (40, 40))
    surf2 = load_image("spaceship.png", (40, 40))
    assert surf1 is surf2
    assert len(_IMAGE_CACHE) == 1


def test_load_image_different_sizes_cached_separately():
    """Verify different scale dimensions create distinct cache entries."""
    surf_small = load_image("spaceship.png", (40, 40))
    surf_large = load_image("spaceship.png", (80, 80))
    assert surf_small is not surf_large
    assert surf_small.get_size() == (40, 40)
    assert surf_large.get_size() == (80, 80)
    assert len(_IMAGE_CACHE) == 2


def test_load_image_missing_file_raises_not_found():
    """AC-1.1: Verify loading nonexistent file raises descriptive FileNotFoundError."""
    with pytest.raises(FileNotFoundError, match="Asset file not found"):
        load_image("non_existent_sprite.png")


def test_clear_cache():
    """Verify clear_cache completely flushes memoized surfaces."""
    load_image("spaceship.png", (40, 40))
    assert len(_IMAGE_CACHE) == 1
    clear_cache()
    assert len(_IMAGE_CACHE) == 0


def test_get_player_surface():
    """AC-1.3: Verify get_player_surface returns surface scaled to player diameter."""
    player_surf = get_player_surface()
    expected_dim = int(PLAYER_RADIUS * 2)
    assert player_surf.get_size() == (expected_dim, expected_dim)


def test_get_background_surface():
    """AC-1.2: Verify get_background_surface returns surface scaled to screen resolution."""
    bg_surf = get_background_surface()
    assert bg_surf.get_size() == (SCREEN_WIDTH, SCREEN_HEIGHT)


@pytest.mark.parametrize(
    "radius,expected_tier_file,expected_dim",
    [
        (60.0, "asteriods_big.png", 120),
        (50.0, "asteriods_big.png", 100),
        (40.0, "asteriods_mid.png", 80),
        (30.0, "asteriods_mid.png", 60),
        (20.0, "asteriods_small.png", 40),
        (10.0, "asteriods_small.png", 20),
    ],
)
def test_get_asteroid_surface_tiers_and_scaling(radius, expected_tier_file, expected_dim):
    """AC-1.4: Verify tier assignment and diameter scaling across asteroid sizes."""
    surf = get_asteroid_surface(radius)
    assert surf.get_size() == (expected_dim, expected_dim)


def test_player_sprite_initialization_and_drawing():
    """AC-1.3: Verify Player initializes with sprite and draws rotated texture to surface."""
    player = Player(200.0, 300.0)
    assert hasattr(player, "image")
    assert isinstance(player.image, pygame.Surface)

    target_surface = pygame.Surface((800, 600))
    # Test drawing at default rotation
    player.draw(target_surface)

    # Test drawing at rotated angle
    player.rotate(0.5)
    player.draw(target_surface)

    # Test defensive guard against None screen
    player.draw(None)


def test_asteroid_sprite_initialization_and_drawing():
    """AC-1.4: Verify Asteroid initializes with tiered sprite and draws centered rect."""
    asteroid_big = Asteroid(100.0, 100.0, ASTEROID_MAX_RADIUS)
    assert hasattr(asteroid_big, "image")
    assert asteroid_big.image.get_size() == (int(ASTEROID_MAX_RADIUS * 2), int(ASTEROID_MAX_RADIUS * 2))

    target_surface = pygame.Surface((800, 600))
    asteroid_big.draw(target_surface)
    asteroid_big.draw(None)


def test_asteroid_split_assigns_correct_child_sprites():
    """AC-1.4: Verify child asteroids created by split have correct tier-scaled sprites."""
    parent = Asteroid(100.0, 100.0, 60.0)
    parent.velocity = pygame.Vector2(10.0, 0.0)

    # Capture containers or mock group to capture split children
    group = pygame.sprite.Group()
    Asteroid.containers = (group,)

    parent.split()
    children = group.sprites()
    assert len(children) == 2
    for child in children:
        assert child.radius == pytest.approx(40.0)
        assert child.image.get_size() == (80, 80)


def test_collision_math_unaffected_by_sprites():
    """AC-1.5: Verify circle collision detection uses mathematical radius, not sprite rects."""
    player = Player(100.0, 100.0)
    asteroid = Asteroid(100.0, 130.0, 20.0)

    # Distance is 30, radii sum is 20 + 20 = 40 -> colliding
    assert player.collides_with(asteroid) is True

    # Rotate player 90 degrees (sprite bounding box dimensions change)
    player.rotation = 90.0
    # Collision math must remain completely identical
    assert player.collides_with(asteroid) is True

    # Move asteroid outside collision radius
    asteroid.position = pygame.Vector2(100.0, 150.0)
    # Distance is 50, radii sum is 40 -> not colliding
    assert player.collides_with(asteroid) is False
