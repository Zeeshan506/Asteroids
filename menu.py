"""Main menu and leaderboard rendering and navigation module."""

from typing import Any, Optional

import pygame

from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from hud import get_font

MENU_OPTIONS = ["START GAME", "LEADERBOARD", "QUIT"]


def handle_menu_key(key: int, current_index: int) -> tuple[int, Optional[str]]:
    """Handle keyboard inputs on the main menu.

    Args:
        key: Pygame key constant from event.
        current_index: Index of currently selected menu item.

    Returns:
        tuple[int, Optional[str]]: (updated_index, action_name_or_None)
    """
    total = len(MENU_OPTIONS)
    if key in (pygame.K_UP, pygame.K_w):
        return (current_index - 1) % total, None
    elif key in (pygame.K_DOWN, pygame.K_s):
        # Only treat 's' as navigation if down, but 's' key alone starts if not using WASD
        return (current_index + 1) % total, None
    elif key in (pygame.K_RETURN, pygame.K_SPACE):
        selected = MENU_OPTIONS[current_index]
        return current_index, selected
    elif key == pygame.K_l:
        return 1, "LEADERBOARD"
    elif key in (pygame.K_q, pygame.K_ESCAPE):
        return current_index, "QUIT"

    return current_index, None


def handle_leaderboard_key(key: int) -> Optional[str]:
    """Handle keyboard inputs on the leaderboard screen.

    Args:
        key: Pygame key constant from event.

    Returns:
        Optional[str]: Action such as "MENU" or "START" or None.
    """
    if key in (pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_SPACE, pygame.K_m, pygame.K_b):
        return "MENU"
    return None


def draw_menu(screen: pygame.Surface, selected_index: int) -> None:
    """Render the main arcade title and interactive navigation menu.

    Args:
        screen: Pygame display surface.
        selected_index: Index of the currently highlighted option.
    """
    if screen is None:
        return

    title_font = get_font(64)
    item_font = get_font(32)
    hint_font = get_font(20)

    # Title
    title_surf = title_font.render("A S T E R O I D S", True, (100, 220, 255))
    title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 160))
    screen.blit(title_surf, title_rect)

    # Subtitle
    sub_surf = hint_font.render("DEFEND THE GALAXY", True, (180, 200, 220))
    sub_rect = sub_surf.get_rect(center=(SCREEN_WIDTH // 2, 215))
    screen.blit(sub_surf, sub_rect)

    # Options
    start_y = 310
    spacing = 60
    for idx, option in enumerate(MENU_OPTIONS):
        is_selected = idx == selected_index
        color = (255, 230, 80) if is_selected else (200, 200, 200)
        label = f">  {option}  <" if is_selected else option
        opt_surf = item_font.render(label, True, color)
        opt_rect = opt_surf.get_rect(center=(SCREEN_WIDTH // 2, start_y + idx * spacing))
        screen.blit(opt_surf, opt_rect)

    # Control hints at footer
    hints = "NAVIGATE: UP/DOWN or W/S  |  SELECT: ENTER / SPACE  |  MUTE: M"
    hints_surf = hint_font.render(hints, True, (140, 150, 160))
    hints_rect = hints_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60))
    screen.blit(hints_surf, hints_rect)


def draw_leaderboard(screen: pygame.Surface, scores: list[dict[str, Any]]) -> None:
    """Render the persistent top scores leaderboard table.

    Args:
        screen: Pygame display surface.
        scores: List of score records with player_name, score, created_at.
    """
    if screen is None:
        return

    title_font = get_font(48)
    header_font = get_font(24)
    row_font = get_font(22)
    prompt_font = get_font(20)

    # Title
    title_surf = title_font.render("TOP PILOTS LEADERBOARD", True, (255, 215, 0))
    title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 110))
    screen.blit(title_surf, title_rect)

    # Table Header
    header_str = f"{'RANK':<6}{'PILOT':<16}{'SCORE':>8}      {'DATE':<19}"
    hdr_surf = header_font.render(header_str, True, (120, 220, 255))
    hdr_rect = hdr_surf.get_rect(center=(SCREEN_WIDTH // 2, 180))
    screen.blit(hdr_surf, hdr_rect)

    # Divider
    divider_surf = header_font.render("-" * 52, True, (80, 100, 130))
    div_rect = divider_surf.get_rect(center=(SCREEN_WIDTH // 2, 205))
    screen.blit(divider_surf, div_rect)

    # Rows
    y = 235
    if not scores:
        empty_surf = row_font.render("NO FLIGHT RECORDS FOUND YET", True, (180, 180, 180))
        empty_rect = empty_surf.get_rect(center=(SCREEN_WIDTH // 2, 280))
        screen.blit(empty_surf, empty_rect)
    else:
        for idx, entry in enumerate(scores[:10]):
            rank = f"#{idx + 1}"
            name = entry.get("player_name", "PILOT")[:14]
            score_val = entry.get("score", 0)
            date_val = entry.get("created_at", "")[:19]
            row_str = f"{rank:<6}{name:<16}{score_val:>8}      {date_val:<19}"

            color = (255, 255, 255) if idx == 0 else (210, 210, 210)
            row_surf = row_font.render(row_str, True, color)
            row_rect = row_surf.get_rect(center=(SCREEN_WIDTH // 2, y))
            screen.blit(row_surf, row_rect)
            y += 32

    # Prompt
    prompt_surf = prompt_font.render("PRESS ESC OR ENTER TO RETURN TO MAIN MENU", True, (140, 200, 255))
    prompt_rect = prompt_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60))
    screen.blit(prompt_surf, prompt_rect)
