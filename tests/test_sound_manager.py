"""Tests for sound_manager module: defensive initialization, playback, and mute state."""

import os
from unittest.mock import MagicMock, patch
import pytest
import pygame

from sound_manager import SoundManager


def test_sound_manager_initialization_headless():
    """AC-3.1: Verify SoundManager initializes safely in headless mode."""
    sound_mgr = SoundManager()
    assert isinstance(sound_mgr.enabled, bool)
    assert sound_mgr.muted is False


def test_sound_manager_mute_toggle():
    """AC-3.3: Verify toggle_mute switches muted state on and off."""
    sound_mgr = SoundManager()
    sound_mgr.enabled = True
    sound_mgr.muted = False

    new_state = sound_mgr.toggle_mute()
    assert new_state is True
    assert sound_mgr.muted is True
    assert sound_mgr.is_active is False

    new_state = sound_mgr.toggle_mute()
    assert new_state is False
    assert sound_mgr.muted is False
    assert sound_mgr.is_active is True


def test_sound_manager_play_when_disabled():
    """AC-3.1: Play methods return False silently when sound is disabled."""
    sound_mgr = SoundManager()
    sound_mgr.enabled = False
    assert sound_mgr.play_shoot() is False
    assert sound_mgr.play_asteroid_hit() is False
    assert sound_mgr.play_player_hit() is False
    assert sound_mgr.play_thruster() is False


def test_sound_manager_play_when_muted():
    """AC-3.3: Play methods return False when sound is muted."""
    sound_mgr = SoundManager()
    sound_mgr.enabled = True
    sound_mgr.muted = True
    assert sound_mgr.play("shoot") is False


def test_sound_manager_play_with_mocked_sound():
    """AC-3.2: Verify sound plays when active and sound object is loaded."""
    sound_mgr = SoundManager()
    sound_mgr.enabled = True
    sound_mgr.muted = False

    mock_sound = MagicMock()
    sound_mgr._sounds["shoot"] = mock_sound

    result = sound_mgr.play_shoot()
    assert result is True
    mock_sound.play.assert_called_once()


def test_sound_manager_init_failure_fallback():
    """AC-3.1: Mixer initialization errors are caught and disable audio gracefully."""
    with patch("pygame.mixer.init", side_effect=pygame.error("No audio device")):
        with patch("pygame.mixer.get_init", return_value=False):
            sound_mgr = SoundManager()
            assert sound_mgr.enabled is False
            assert sound_mgr.is_active is False
