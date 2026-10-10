"""Head-up display (HUD) module for rendering score, lives, pause, and game over screens."""

import pygame

from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from game_state_manager import GameStateManager

_FONT_CACHE: dict[int, pygame.font.Font] = {}


def get_font(size: int = 24) -> pygame.font.Font:
    """Return a cached Pygame font instance of the requested size."""
    if size not in _FONT_CACHE:
        if not pygame.font.get_init():
            pygame.font.init()
        try:
            _FONT_CACHE[size] = pygame.font.SysFont("dejavusans", size, bold=True)
        except Exception:
            _FONT_CACHE[size] = pygame.font.Font(None, size)
    return _FONT_CACHE[size]


def clear_font_cache() -> None:
    """Clear cached fonts (useful during test resets)."""
    _FONT_CACHE.clear()


def draw_hud(screen: pygame.Surface, state_manager: GameStateManager) -> None:
    """Render active gameplay HUD (score top-left, high score center, lives top-right).

    Args:
        screen: Pygame display surface.
        state_manager: GameStateManager instance holding current score, high score, and lives.
    """
    if screen is None:
        return

    font = get_font(28)

    # Score display at top-left
    score_surf = font.render(f"SCORE: {state_manager.score}", True, (255, 255, 255))
    screen.blit(score_surf, (20, 20))

    # High score at top-center
    high_score_surf = font.render(
        f"HIGH SCORE: {state_manager.high_score}", True, (255, 215, 0)
    )
    high_score_rect = high_score_surf.get_rect(center=(SCREEN_WIDTH // 2, 34))
    screen.blit(high_score_surf, high_score_rect)

    # Lives display at top-right
    lives_surf = font.render(f"LIVES: {state_manager.lives}", True, (255, 255, 255))
    lives_x = SCREEN_WIDTH - lives_surf.get_width() - 20
    screen.blit(lives_surf, (lives_x, 20))


def draw_paused(screen: pygame.Surface) -> None:
    """Render centered PAUSED overlay banner.

    Args:
        screen: Pygame display surface.
    """
    if screen is None:
        return

    banner_font = get_font(56)
    sub_font = get_font(24)

    pause_surf = banner_font.render("GAME PAUSED", True, (255, 230, 80))
    pause_rect = pause_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
    screen.blit(pause_surf, pause_rect)

    hint_surf = sub_font.render("PRESS P TO RESUME", True, (200, 220, 240))
    hint_rect = hint_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
    screen.blit(hint_surf, hint_rect)


def draw_game_over(screen: pygame.Surface, state_manager: GameStateManager) -> None:
    """Render centered Game Over banner with final score and navigation prompts.

    Args:
        screen: Pygame display surface.
        state_manager: GameStateManager instance with final score.
    """
    if screen is None:
        return

    banner_font = get_font(56)
    score_font = get_font(32)
    prompt_font = get_font(22)

    # Game Over title
    title_surf = banner_font.render("GAME OVER", True, (255, 60, 60))
    title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60))
    screen.blit(title_surf, title_rect)

    # Final score
    final_score_surf = score_font.render(
        f"FINAL SCORE: {state_manager.score}", True, (240, 240, 240)
    )
    score_rect = final_score_surf.get_rect(
        center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    )
    screen.blit(final_score_surf, score_rect)

    # Prompt actions
    prompt_str = "PRESS R TO RESTART  |  M FOR MENU  |  L FOR LEADERBOARD"
    prompt_surf = prompt_font.render(prompt_str, True, (160, 220, 255))
    prompt_rect = prompt_surf.get_rect(
        center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60)
    )
    screen.blit(prompt_surf, prompt_rect)
