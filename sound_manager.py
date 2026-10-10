"""Defensive audio management module for sound effects, background music, and independent volume controls."""

import os
from typing import Optional

import pygame


class SoundManager:
    """Manages audio initialization, background music, sound effects, and independent volume controls."""

    DEFAULT_MUSIC_VOLUME: float = 0.20
    DEFAULT_SFX_VOLUME: float = 0.50

    def __init__(self, assets_dir: Optional[str] = None) -> None:
        self.enabled: bool = False
        self.muted: bool = False
        self.music_volume: float = self.DEFAULT_MUSIC_VOLUME
        self.sfx_volume: float = self.DEFAULT_SFX_VOLUME
        self.bg_music_playing: bool = False
        self._sounds: dict[str, pygame.mixer.Sound] = {}

        if assets_dir is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            assets_dir = os.path.join(base_dir, "assets", "music")
        self.assets_dir = assets_dir

        self._init_mixer()
        if self.enabled:
            self._load_sounds()
            self.start_bg_music()

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
        }

        for name, filename in sound_mappings.items():
            path = os.path.join(self.assets_dir, filename)
            if os.path.isfile(path):
                try:
                    sound = pygame.mixer.Sound(path)
                    sound.set_volume(self.sfx_volume)
                    self._sounds[name] = sound
                except (pygame.error, Exception):
                    pass

    def start_bg_music(self, loop: int = -1) -> bool:
        """Start playing background music continuously on loop at low volume."""
        if not self.enabled:
            return False

        bg_path = os.path.join(self.assets_dir, "bg_music.mp3")
        if not os.path.isfile(bg_path):
            return False

        try:
            pygame.mixer.music.load(bg_path)
            vol = 0.0 if self.muted else self.music_volume
            pygame.mixer.music.set_volume(vol)
            pygame.mixer.music.play(loop)
            self.bg_music_playing = True
            return True
        except (pygame.error, Exception):
            self.bg_music_playing = False
            return False

    def stop_bg_music(self) -> None:
        """Stop background music."""
        if self.enabled and self.bg_music_playing:
            try:
                pygame.mixer.music.stop()
                self.bg_music_playing = False
            except (pygame.error, Exception):
                pass

    def set_music_volume(self, volume: float) -> float:
        """Set background music volume independently (clamped between 0.0 and 1.0)."""
        self.music_volume = max(0.0, min(1.0, round(volume, 2)))
        if self.enabled:
            try:
                effective_vol = 0.0 if self.muted else self.music_volume
                pygame.mixer.music.set_volume(effective_vol)
            except (pygame.error, Exception):
                pass
        return self.music_volume

    def set_sfx_volume(self, volume: float) -> float:
        """Set sound effects volume independently (clamped between 0.0 and 1.0)."""
        self.sfx_volume = max(0.0, min(1.0, round(volume, 2)))
        if self.enabled:
            effective_vol = 0.0 if self.muted else self.sfx_volume
            for sound in self._sounds.values():
                try:
                    sound.set_volume(effective_vol)
                except (pygame.error, Exception):
                    pass
        return self.sfx_volume

    def change_music_volume(self, delta: float) -> float:
        """Adjust background music volume by delta."""
        return self.set_music_volume(self.music_volume + delta)

    def change_sfx_volume(self, delta: float) -> float:
        """Adjust sound effects volume by delta."""
        return self.set_sfx_volume(self.sfx_volume + delta)

    def toggle_mute(self) -> bool:
        """Toggle mute state on or off for all audio streams."""
        self.muted = not self.muted
        if self.enabled:
            try:
                pygame.mixer.music.set_volume(0.0 if self.muted else self.music_volume)
            except (pygame.error, Exception):
                pass
            eff_sfx = 0.0 if self.muted else self.sfx_volume
            for sound in self._sounds.values():
                try:
                    sound.set_volume(eff_sfx)
                except (pygame.error, Exception):
                    pass
        return self.muted

    @property
    def is_active(self) -> bool:
        """Return True if audio is enabled and unmuted."""
        return self.enabled and not self.muted

    def play(self, sound_name: str) -> bool:
        """Play requested sound effect if active."""
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
        return False
