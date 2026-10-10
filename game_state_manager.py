"""Game state management module tracking arcade lifecycle, score, and player lives."""

from enum import Enum, auto
from typing import Optional

from leaderboard_manager import LeaderboardManager


class GameState(Enum):
    """Lifecycle states for the game loop."""

    MENU = auto()
    PLAYING = auto()
    PAUSED = auto()
    LEADERBOARD = auto()
    GAME_OVER = auto()


class GameStateManager:
    """Manages player score, lives, respawn invulnerability, and game state transitions."""

    INITIAL_LIVES: int = 3
    INVULNERABILITY_DURATION: float = 2.0
    POINTS_LARGE: int = 20
    POINTS_MEDIUM: int = 50
    POINTS_SMALL: int = 100

    def __init__(
        self,
        leaderboard_manager: Optional[LeaderboardManager] = None,
        initial_state: GameState = GameState.PLAYING,
    ) -> None:
        self.state: GameState = initial_state
        self.score: int = 0
        self.lives: int = self.INITIAL_LIVES
        self.invulnerability_timer: float = 0.0
        self.score_recorded: bool = False

        self.leaderboard: LeaderboardManager = (
            leaderboard_manager
            if leaderboard_manager is not None
            else LeaderboardManager()
        )
        self.high_score: int = self.leaderboard.get_high_score()

    @property
    def is_invulnerable(self) -> bool:
        """Return True if player currently has active respawn invulnerability."""
        return self.invulnerability_timer > 0.0

    def add_asteroid_score(self, radius: float) -> int:
        """Award score points based on destroyed asteroid radius tier.

        Args:
            radius: Radius of the destroyed asteroid.

        Returns:
            int: Points added to the player's score.
        """
        if radius > 40:
            points = self.POINTS_LARGE
        elif radius > 20:
            points = self.POINTS_MEDIUM
        else:
            points = self.POINTS_SMALL

        self.score += points
        if self.score > self.high_score:
            self.high_score = self.score
        return points

    def update(self, dt: float) -> None:
        """Update active timers such as respawn invulnerability.

        Args:
            dt: Delta time in seconds since the last frame.
        """
        if self.invulnerability_timer > 0.0:
            self.invulnerability_timer = max(0.0, self.invulnerability_timer - dt)

    def lose_life(self) -> bool:
        """Decrement player life upon collision if not invulnerable.

        Returns:
            bool: True if player has remaining lives and will respawn,
                  False if lives reached 0 or if collision was ignored.
        """
        if self.is_invulnerable or self.state == GameState.GAME_OVER:
            return False

        self.lives -= 1
        if self.lives <= 0:
            self.lives = 0
            self.state = GameState.GAME_OVER
            self.invulnerability_timer = 0.0
            self._record_final_score()
            return False

        self.invulnerability_timer = self.INVULNERABILITY_DURATION
        return True

    def _record_final_score(self) -> None:
        """Persist final score to SQLite database if not already saved."""
        if not self.score_recorded:
            self.leaderboard.add_score("PLAYER", self.score)
            self.high_score = self.leaderboard.get_high_score()
            self.score_recorded = True

    def toggle_pause(self) -> bool:
        """Toggle between PLAYING and PAUSED states.

        Returns:
            bool: True if currently paused, False otherwise.
        """
        if self.state == GameState.PLAYING:
            self.state = GameState.PAUSED
            return True
        elif self.state == GameState.PAUSED:
            self.state = GameState.PLAYING
            return False
        return False

    def start_game(self) -> None:
        """Begin a new gameplay session from MENU or LEADERBOARD."""
        self.state = GameState.PLAYING
        self.score = 0
        self.lives = self.INITIAL_LIVES
        self.invulnerability_timer = 0.0
        self.score_recorded = False

    def restart(self) -> None:
        """Reset score, lives, timers, and state to start a new game."""
        self.start_game()
