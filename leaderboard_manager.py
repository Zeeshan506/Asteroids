"""Local SQLite persistence manager for leaderboard records and high scores."""

from datetime import datetime
import sqlite3
from typing import Any, Optional


class LeaderboardManager:
    """Manages leaderboard persistence in a local SQLite database (sqlite.db)."""

    DEFAULT_DB_PATH: str = "sqlite.db"

    def __init__(self, db_path: Optional[str] = None) -> None:
        self.db_path: str = db_path if db_path is not None else self.DEFAULT_DB_PATH
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        """Create and return an SQLite connection with row factories enabled."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        """Initialize schema and ensure the leaderboard table exists."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS leaderboard (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    player_name TEXT NOT NULL,
                    score INTEGER NOT NULL,
                    created_at TEXT NOT NULL
                )
                """
            )
            cursor.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_leaderboard_score
                ON leaderboard (score DESC)
                """
            )
            conn.commit()

    def add_score(self, player_name: str, score: int) -> int:
        """Record a completed game score into the local SQLite database.

        Args:
            player_name: Label or identifier for the player.
            score: Final score achieved.

        Returns:
            int: The primary key ID of the newly inserted record.
        """
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cleaned_name = player_name.strip() if player_name.strip() else "PLAYER"
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO leaderboard (player_name, score, created_at)
                VALUES (?, ?, ?)
                """,
                (cleaned_name, max(0, score), now_str),
            )
            conn.commit()
            return cursor.lastrowid or 0

    def get_top_scores(self, limit: int = 10) -> list[dict[str, Any]]:
        """Retrieve top high score records sorted by score descending.

        Args:
            limit: Maximum number of records to return.

        Returns:
            list[dict[str, Any]]: List of dictionary rows with name, score, date.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id, player_name, score, created_at
                FROM leaderboard
                ORDER BY score DESC, id ASC
                LIMIT ?
                """,
                (limit,),
            )
            rows = cursor.fetchall()
            return [
                {
                    "id": row["id"],
                    "player_name": row["player_name"],
                    "score": row["score"],
                    "created_at": row["created_at"],
                }
                for row in rows
            ]

    def get_high_score(self) -> int:
        """Return the all-time highest score recorded in the local database.

        Returns:
            int: Highest score, or 0 if no entries exist.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT MAX(score) AS max_score FROM leaderboard")
            row = cursor.fetchone()
            if row and row["max_score"] is not None:
                return int(row["max_score"])
            return 0
