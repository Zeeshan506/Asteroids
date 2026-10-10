"""Defensive audio management module for sound effects and mute handling."""

import os
from typing import Optional

import pygame


class SoundManager:
    """Manages audio initialization, playback, and mute toggling defensively."""

    def __init__(self, assets_dir: Optional[str] = None) -> None:
        self.enabled: bool = False
        self.muted: bool = False
        self._sounds: dict[str, pygame.mixer.Sound] = {}

        if assets_dir is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            assets_dir = os.path.join(base_dir, "assets", "music")
        self.assets_dir = assets_dir

        self._init_mixer()
        if self.enabled:
            self._load_sounds()

    def _init_mixer(self) -> None:
        """Attempt safe initialization of pygame.mixer."""
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            self.enabled = True
        except (pygame.error, Exception):
            self.enabled = False

    def _load_sounds(self) -> None:
        """Load audio files safely with fallback handling."""
        sound_mappings = {
            "shoot": "single_shot.mp3",
            "asteroid_hit": "asteroid_destruction.mp3",
            "player_hit": "asteroid_destruction.mp3",
            "thruster": "single_shot.mp3",
        }

        for name, filename in sound_mappings.items():
            path = os.path.join(self.assets_dir, filename)
            if os.path.isfile(path):
                try:
                    sound = pygame.mixer.Sound(path)
                    sound.set_volume(0.4)
                    self._sounds[name] = sound
                except (pygame.error, Exception):
                    pass

    def toggle_mute(self) -> bool:
        """Toggle mute state on or off.

        Returns:
            bool: True if sound is now muted, False if unmuted.
        """
        self.muted = not self.muted
        return self.muted

    @property
    def is_active(self) -> bool:
        """Return True if audio is enabled and unmuted."""
        return self.enabled and not self.muted

    def play(self, sound_name: str) -> bool:
        """Play requested sound effect if active.

        Args:
            sound_name: Identifier of the sound to play.

        Returns:
            bool: True if sound was played, False otherwise.
        """
        if not self.is_active:
            return False

        sound = self._sounds.get(sound_name)
        if sound is not None:
            try:
                sound.play()
                return True
            except (pygame.error, Exception):
                return False
        return False

    def play_shoot(self) -> bool:
        return self.play("shoot")

    def play_asteroid_hit(self) -> bool:
        return self.play("asteroid_hit")

    def play_player_hit(self) -> bool:
        return self.play("player_hit")

    def play_thruster(self) -> bool:
        return self.play("thruster")
