"""Tests for sound_manager module: defensive initialization, playback, bg music, and volume controls."""

import os
from unittest.mock import MagicMock, patch
import pytest
import pygame

from sound_manager import SoundManager


def test_sound_manager_initialization_headless():
    """AC-3.1, AC-3.9: Verify SoundManager initializes safely in headless mode."""
    sound_mgr = SoundManager()
    assert isinstance(sound_mgr.enabled, bool)
    assert sound_mgr.muted is False
    assert sound_mgr.music_volume == pytest.approx(0.20)
    assert sound_mgr.sfx_volume == pytest.approx(0.50)


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


def test_sound_manager_bg_music_playback():
    """AC-3.9: Verify background music loads and plays at default low volume."""
    with patch("pygame.mixer.music.load") as mock_load, \
         patch("pygame.mixer.music.set_volume") as mock_vol, \
         patch("pygame.mixer.music.play") as mock_play:
        sound_mgr = SoundManager()
        assert sound_mgr.music_volume == pytest.approx(0.20)
        mock_load.assert_called_with(
            os.path.join(sound_mgr.assets_dir, "bg_music.mp3")
        )
        mock_vol.assert_called_with(pytest.approx(0.20))
        mock_play.assert_called_with(-1)


def test_sound_manager_independent_volume_controls():
    """AC-3.10: Verify separate volume controllers for BG music and SFX with clamping."""
    sound_mgr = SoundManager()
    mock_sound = MagicMock()
    sound_mgr._sounds["shoot"] = mock_sound

    # Adjust music volume
    assert sound_mgr.set_music_volume(0.35) == pytest.approx(0.35)
    assert sound_mgr.music_volume == pytest.approx(0.35)
    assert sound_mgr.sfx_volume == pytest.approx(0.50)  # SFX untouched

    # Clamp music volume bounds
    assert sound_mgr.set_music_volume(1.5) == pytest.approx(1.0)
    assert sound_mgr.set_music_volume(-0.5) == pytest.approx(0.0)

    # Adjust SFX volume
    assert sound_mgr.set_sfx_volume(0.75) == pytest.approx(0.75)
    assert sound_mgr.sfx_volume == pytest.approx(0.75)
    assert sound_mgr.music_volume == pytest.approx(0.0)  # Music untouched

    # Clamp SFX volume bounds
    assert sound_mgr.set_sfx_volume(2.0) == pytest.approx(1.0)
    assert sound_mgr.set_sfx_volume(-1.0) == pytest.approx(0.0)

    # Delta changes
    sound_mgr.set_music_volume(0.20)
    sound_mgr.change_music_volume(0.10)
    assert sound_mgr.music_volume == pytest.approx(0.30)

    sound_mgr.set_sfx_volume(0.40)
    sound_mgr.change_sfx_volume(-0.15)
    assert sound_mgr.sfx_volume == pytest.approx(0.25)
