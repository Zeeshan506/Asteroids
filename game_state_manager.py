"""Game state management module tracking arcade lifecycle, score, and player lives."""

from enum import Enum, auto


class GameState(Enum):
    """Lifecycle states for the game loop."""

    PLAYING = auto()
    GAME_OVER = auto()


class GameStateManager:
    """Manages player score, lives, respawn invulnerability, and game state transitions."""

    INITIAL_LIVES: int = 3
    INVULNERABILITY_DURATION: float = 2.0
    POINTS_LARGE: int = 20
    POINTS_MEDIUM: int = 50
    POINTS_SMALL: int = 100

    def __init__(self) -> None:
        self.state: GameState = GameState.PLAYING
        self.score: int = 0
        self.lives: int = self.INITIAL_LIVES
        self.invulnerability_timer: float = 0.0

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
            return False

        self.invulnerability_timer = self.INVULNERABILITY_DURATION
        return True

    def restart(self) -> None:
        """Reset score, lives, timers, and state to start a new game."""
        self.state = GameState.PLAYING
        self.score = 0
        self.lives = self.INITIAL_LIVES
        self.invulnerability_timer = 0.0
