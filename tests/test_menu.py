"""Tests for menu navigation and leaderboard view rendering."""

import pytest
import pygame

from menu import (
    MENU_OPTIONS,
    draw_leaderboard,
    draw_menu,
    handle_leaderboard_key,
    handle_menu_key,
)


def test_menu_navigation_down_and_up():
    """AC-3.6: Verify navigating up and down cycles through menu options."""
    idx, action = handle_menu_key(pygame.K_DOWN, 0)
    assert idx == 1
    assert action is None

    idx, action = handle_menu_key(pygame.K_DOWN, 1)
    assert idx == 2
    assert action is None

    # Cycling past end wraps to 0
    idx, action = handle_menu_key(pygame.K_DOWN, 2)
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
    assert action == "QUIT"


def test_menu_direct_shortcuts():
    """AC-3.6: Direct shortcut keys for leaderboard and quit."""
    _, action_l = handle_menu_key(pygame.K_l, 0)
    assert action_l == "LEADERBOARD"

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
