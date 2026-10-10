"""Tests for SQLite database persistence and leaderboard operations."""

import os
import tempfile
import pytest

from leaderboard_manager import LeaderboardManager


@pytest.fixture
def temp_db_path():
    """Create a temporary sqlite db path cleaned up after test."""
    temp_dir = tempfile.mkdtemp()
    db_file = os.path.join(temp_dir, "test_leaderboard.db")
    yield db_file
    if os.path.exists(db_file):
        os.remove(db_file)
    if os.path.exists(temp_dir):
        os.rmdir(temp_dir)


def test_leaderboard_initialization_creates_table(temp_db_path):
    """AC-3.5: Verify SQLite database and leaderboard table are created."""
    mgr = LeaderboardManager(db_path=temp_db_path)
    assert os.path.exists(temp_db_path)
    assert mgr.get_high_score() == 0
    assert mgr.get_top_scores() == []


def test_leaderboard_add_and_retrieve_scores(temp_db_path):
    """AC-3.5, AC-3.7: Insert scores and fetch ordered descending."""
    mgr = LeaderboardManager(db_path=temp_db_path)
    id1 = mgr.add_score("ALICE", 150)
    id2 = mgr.add_score("BOB", 350)
    id3 = mgr.add_score("CHARLIE", 200)

    assert id1 > 0 and id2 > 0 and id3 > 0
    assert mgr.get_high_score() == 350

    top_scores = mgr.get_top_scores(limit=10)
    assert len(top_scores) == 3
    assert top_scores[0]["player_name"] == "BOB"
    assert top_scores[0]["score"] == 350
    assert top_scores[1]["player_name"] == "CHARLIE"
    assert top_scores[1]["score"] == 200
    assert top_scores[2]["player_name"] == "ALICE"
    assert top_scores[2]["score"] == 150


def test_leaderboard_data_persists_across_instances(temp_db_path):
    """AC-3.5: Ensure data persists across distinct connection/instance lifecycles."""
    mgr1 = LeaderboardManager(db_path=temp_db_path)
    mgr1.add_score("PERSISTENT_PILOT", 990)

    # Instantiate brand new manager instance pointing to the same SQLite file
    mgr2 = LeaderboardManager(db_path=temp_db_path)
    assert mgr2.get_high_score() == 990
    top = mgr2.get_top_scores()
    assert len(top) == 1
    assert top[0]["player_name"] == "PERSISTENT_PILOT"
    assert top[0]["score"] == 990


def test_leaderboard_handles_empty_or_whitespace_name(temp_db_path):
    """AC-3.5: Fallback to default player name when given empty string."""
    mgr = LeaderboardManager(db_path=temp_db_path)
    mgr.add_score("   ", 120)
    top = mgr.get_top_scores()
    assert len(top) == 1
    assert top[0]["player_name"] == "PLAYER"
    assert top[0]["score"] == 120
