"""Tests for menu navigation, leaderboard view, and audio volume controller rendering."""

import pytest
import pygame

from menu import (
    MENU_OPTIONS,
    draw_audio_settings,
    draw_leaderboard,
    draw_menu,
    handle_audio_key,
    handle_leaderboard_key,
    handle_menu_key,
)
from sound_manager import SoundManager


def test_menu_navigation_down_and_up():
    """AC-3.6: Verify navigating up and down cycles through menu options."""
    idx, action = handle_menu_key(pygame.K_DOWN, 0)
    assert idx == 1
    assert action is None

    idx, action = handle_menu_key(pygame.K_DOWN, 1)
    assert idx == 2
    assert action is None

    # Cycling past end wraps to 0
    idx, action = handle_menu_key(pygame.K_DOWN, len(MENU_OPTIONS) - 1)
    assert idx == 0
    assert action is None

    # Navigating UP cycles backwards
    idx, action = handle_menu_key(pygame.K_UP, 0)
    assert idx == len(MENU_OPTIONS) - 1
    assert action is None


def test_menu_selection_actions():
    """AC-3.6: Pressing Enter or Space triggers the selected action."""
    idx, action = handle_menu_key(pygame.K_RETURN, 0)
    assert action == "START GAME"

    idx, action = handle_menu_key(pygame.K_SPACE, 1)
    assert action == "LEADERBOARD"

    idx, action = handle_menu_key(pygame.K_RETURN, 2)
    assert action == "AUDIO SETTINGS"

    idx, action = handle_menu_key(pygame.K_RETURN, 3)
    assert action == "QUIT"


def test_menu_direct_shortcuts():
    """AC-3.6: Direct shortcut keys for leaderboard, audio, and quit."""
    _, action_l = handle_menu_key(pygame.K_l, 0)
    assert action_l == "LEADERBOARD"

    _, action_a = handle_menu_key(pygame.K_a, 0)
    assert action_a == "AUDIO SETTINGS"

    _, action_q = handle_menu_key(pygame.K_q, 0)
    assert action_q == "QUIT"

    _, action_esc = handle_menu_key(pygame.K_ESCAPE, 0)
    assert action_esc == "QUIT"


def test_leaderboard_navigation_key():
    """AC-3.7: Pressing Escape or Enter in leaderboard returns to MENU."""
    assert handle_leaderboard_key(pygame.K_ESCAPE) == "MENU"
    assert handle_leaderboard_key(pygame.K_RETURN) == "MENU"
    assert handle_leaderboard_key(pygame.K_SPACE) == "MENU"
    assert handle_leaderboard_key(pygame.K_m) == "MENU"
    assert handle_leaderboard_key(pygame.K_UNKNOWN) is None


def test_handle_audio_key_navigation_and_adjustment():
    """AC-3.10: Verify audio settings key handlers adjust music and SFX volumes."""
    sound_mgr = SoundManager()
    sound_mgr.set_music_volume(0.20)
    sound_mgr.set_sfx_volume(0.50)

    # When on item 0 (Music Volume): Left/Right adjusts music volume
    handle_audio_key(pygame.K_RIGHT, 0, sound_mgr)
    assert sound_mgr.music_volume == pytest.approx(0.25)
    handle_audio_key(pygame.K_LEFT, 0, sound_mgr)
    assert sound_mgr.music_volume == pytest.approx(0.20)

    # When on item 1 (SFX Volume): Left/Right adjusts SFX volume
    handle_audio_key(pygame.K_RIGHT, 1, sound_mgr)
    assert sound_mgr.sfx_volume == pytest.approx(0.55)
    handle_audio_key(pygame.K_LEFT, 1, sound_mgr)
    assert sound_mgr.sfx_volume == pytest.approx(0.50)

    # When on item 2 (Mute): Space toggles mute
    assert sound_mgr.muted is False
    handle_audio_key(pygame.K_SPACE, 2, sound_mgr)
    assert sound_mgr.muted is True

    # When on item 3 (Back to Menu): Return gives action "MENU"
    idx, action = handle_audio_key(pygame.K_RETURN, 3, sound_mgr)
    assert action == "MENU"

    # ESC anywhere gives action "MENU"
    _, esc_action = handle_audio_key(pygame.K_ESCAPE, 0, sound_mgr)
    assert esc_action == "MENU"


def test_draw_menu_headless_surface():
    """AC-3.6: draw_menu renders without errors onto a surface."""
    surface = pygame.Surface((1280, 720))
    draw_menu(surface, selected_index=0)


def test_draw_leaderboard_headless_surface():
    """AC-3.7: draw_leaderboard renders both empty and populated records cleanly."""
    surface = pygame.Surface((1280, 720))
    draw_leaderboard(surface, scores=[])

    records = [
        {"player_name": "ACE", "score": 450, "created_at": "2026-10-10 12:00:00"}
    ]
    draw_leaderboard(surface, scores=records)


def test_draw_audio_settings_headless_surface():
    """AC-3.10: draw_audio_settings renders without errors onto a surface."""
    surface = pygame.Surface((1280, 720))
    sound_mgr = SoundManager()
    draw_audio_settings(surface, sound_mgr, selected_index=0)
