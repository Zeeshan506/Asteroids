"""Main menu, leaderboard, and audio volume controller rendering and navigation module."""

from typing import Any, Optional

import pygame

from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from hud import get_font
from sound_manager import SoundManager

MENU_OPTIONS = ["START GAME", "LEADERBOARD", "AUDIO SETTINGS", "QUIT"]
AUDIO_OPTIONS = ["MUSIC VOLUME", "SFX VOLUME", "MUTE", "BACK TO MENU"]


def handle_menu_key(key: int, current_index: int) -> tuple[int, Optional[str]]:
    """Handle keyboard inputs on the main menu."""
    total = len(MENU_OPTIONS)
    if key in (pygame.K_UP, pygame.K_w):
        return (current_index - 1) % total, None
    elif key in (pygame.K_DOWN, pygame.K_s):
        return (current_index + 1) % total, None
    elif key in (pygame.K_RETURN, pygame.K_SPACE):
        selected = MENU_OPTIONS[current_index]
        return current_index, selected
    elif key == pygame.K_l:
        return 1, "LEADERBOARD"
    elif key == pygame.K_a:
        return 2, "AUDIO SETTINGS"
    elif key in (pygame.K_q, pygame.K_ESCAPE):
        return current_index, "QUIT"

    return current_index, None


def handle_leaderboard_key(key: int) -> Optional[str]:
    """Handle keyboard inputs on the leaderboard screen."""
    if key in (pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_SPACE, pygame.K_m, pygame.K_b):
        return "MENU"
    return None


def handle_audio_key(
    key: int,
    current_index: int,
    sound_manager: SoundManager,
) -> tuple[int, Optional[str]]:
    """Handle keyboard inputs on the audio volume controller screen."""
    total = len(AUDIO_OPTIONS)
    if key in (pygame.K_UP, pygame.K_w):
        return (current_index - 1) % total, None
    elif key in (pygame.K_DOWN, pygame.K_s):
        return (current_index + 1) % total, None

    # Adjust music volume
    if current_index == 0:
        if key in (pygame.K_LEFT, pygame.K_a, pygame.K_MINUS):
            sound_manager.change_music_volume(-0.05)
        elif key in (pygame.K_RIGHT, pygame.K_d, pygame.K_EQUALS):
            sound_manager.change_music_volume(0.05)

    # Adjust SFX volume
    elif current_index == 1:
        if key in (pygame.K_LEFT, pygame.K_a, pygame.K_MINUS):
            sound_manager.change_sfx_volume(-0.05)
        elif key in (pygame.K_RIGHT, pygame.K_d, pygame.K_EQUALS):
            sound_manager.change_sfx_volume(0.05)

    # Toggle Mute
    elif current_index == 2:
        if key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_m):
            sound_manager.toggle_mute()

    # Back to Menu
    elif current_index == 3:
        if key in (pygame.K_RETURN, pygame.K_SPACE):
            return current_index, "MENU"

    if key in (pygame.K_ESCAPE, pygame.K_b):
        return current_index, "MENU"

    return current_index, None


def draw_menu(screen: pygame.Surface, selected_index: int) -> None:
    """Render the main arcade title and interactive navigation menu."""
    if screen is None:
        return

    title_font = get_font(64)
    item_font = get_font(32)
    hint_font = get_font(20)

    # Title
    title_surf = title_font.render("A S T E R O I D S", True, (100, 220, 255))
    title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 140))
    screen.blit(title_surf, title_rect)

    # Subtitle
    sub_surf = hint_font.render("DEFEND THE GALAXY", True, (180, 200, 220))
    sub_rect = sub_surf.get_rect(center=(SCREEN_WIDTH // 2, 195))
    screen.blit(sub_surf, sub_rect)

    # Options
    start_y = 280
    spacing = 54
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
    hints_rect = hints_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
    screen.blit(hints_surf, hints_rect)


def draw_leaderboard(screen: pygame.Surface, scores: list[dict[str, Any]]) -> None:
    """Render the persistent top scores leaderboard table."""
    if screen is None:
        return

    title_font = get_font(48)
    header_font = get_font(24)
    row_font = get_font(22)
    prompt_font = get_font(20)

    # Title
    title_surf = title_font.render("TOP PILOTS LEADERBOARD", True, (255, 215, 0))
    title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 100))
    screen.blit(title_surf, title_rect)

    # Table Header
    header_str = f"{'RANK':<6}{'PILOT':<16}{'SCORE':>8}      {'DATE':<19}"
    hdr_surf = header_font.render(header_str, True, (120, 220, 255))
    hdr_rect = hdr_surf.get_rect(center=(SCREEN_WIDTH // 2, 165))
    screen.blit(hdr_surf, hdr_rect)

    # Divider
    divider_surf = header_font.render("-" * 52, True, (80, 100, 130))
    div_rect = divider_surf.get_rect(center=(SCREEN_WIDTH // 2, 190))
    screen.blit(divider_surf, div_rect)

    # Rows
    y = 220
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
    prompt_rect = prompt_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
    screen.blit(prompt_surf, prompt_rect)


def draw_audio_settings(
    screen: pygame.Surface,
    sound_manager: SoundManager,
    selected_index: int,
) -> None:
    """Render the separate audio volume controllers screen."""
    if screen is None:
        return

    title_font = get_font(48)
    label_font = get_font(28)
    hint_font = get_font(20)

    title_surf = title_font.render("AUDIO & VOLUME CONTROLLER", True, (100, 220, 255))
    title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 120))
    screen.blit(title_surf, title_rect)

    music_pct = int(sound_manager.music_volume * 100)
    sfx_pct = int(sound_manager.sfx_volume * 100)
    mute_status = "MUTED" if sound_manager.muted else "ACTIVE"

    def make_bar(percent: int) -> str:
        filled = int(percent / 5)
        return f"[{'#' * filled}{'.' * (20 - filled)}]"

    items = [
        f"BG MUSIC VOLUME:  {make_bar(music_pct)}  {music_pct}%",
        f"SFX SOUND VOLUME: {make_bar(sfx_pct)}  {sfx_pct}%",
        f"AUDIO STATE:     [{mute_status}]",
        "BACK TO MAIN MENU",
    ]

    start_y = 230
    spacing = 65
    for idx, text in enumerate(items):
        is_sel = idx == selected_index
        color = (255, 230, 80) if is_sel else (210, 210, 210)
        prefix = "> " if is_sel else "  "
        suffix = " <" if is_sel else ""
        surf = label_font.render(f"{prefix}{text}{suffix}", True, color)
        rect = surf.get_rect(center=(SCREEN_WIDTH // 2, start_y + idx * spacing))
        screen.blit(surf, rect)

    hints = "UP/DOWN: SELECT | LEFT/RIGHT: ADJUST VOLUME | SPACE/M: MUTE | ESC: BACK"
    hints_surf = hint_font.render(hints, True, (140, 150, 160))
    hints_rect = hints_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
    screen.blit(hints_surf, hints_rect)
