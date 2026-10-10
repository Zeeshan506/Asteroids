# Feature Requirements: Phase 3 - Audio, Menu, Leaderboard & Polish

## 1. Context & Business Intent
As described in [specs/mission.md](file:///home/zeshan6a/Projects/bootdotdev/asteroids/specs/mission.md) and [specs/roadmap.md](file:///home/zeshan6a/Projects/bootdotdev/asteroids/specs/roadmap.md), arcade space combat requires tactile acoustic feedback, classic screen wrap-around boundaries, a clear navigation menu, and persistent leaderboard records across play sessions. This phase delivers audio feedback, screen boundary wrapping, a clear start menu, a local SQLite persistent database (`sqlite.db`) for high score and leaderboard tracking, and pause polish.

## 2. Scope
### In-Scope
- Audio Management (`sound_manager.py`):
  - Safe initialization of `pygame.mixer` with robust fallback when sound drivers are absent (e.g. headless containers, missing ALSA devices).
  - Background music playback (`assets/music/bg_music.mp3`) playing continuously on loop at low volume (default 0.20).
  - Separate volume controller for background music (`music_volume`).
  - Separate volume controller for sound effects (`sfx_volume`).
  - Sound effects for:
    - Laser shot fire (`shoot` using `assets/music/single_shot.mp3` or synthesized fallback)
    - Asteroid destruction / split (`asteroid_hit` using `assets/music/asteroid_destruction.mp3` or synthesized fallback)
    - Player ship explosion (`player_hit`)
  - Audio mute toggle via `M` keyboard shortcut.
- Screen Boundary Wrap-Around (`screen_wrap.py`):
  - Spaceship wrapping: exiting any screen edge wraps the ship to the opposing screen edge (left <-> right, top <-> bottom).
  - Shots boundary cleanup: shots despawn when exiting the screen bounds to prevent off-screen accumulation.
- Clear Menu System & Audio Settings (`menu.py`):
  - Distinct `MENU` state rendered before starting gameplay.
  - Interactive options: `START GAME`, `LEADERBOARD`, `AUDIO SETTINGS`, `QUIT`.
  - Audio Settings screen allowing independent volume adjustments for Music and SFX.
  - Simple keyboard navigation (Arrow Up/Down or W/S to select, ENTER or SPACE to confirm; shortcut keys: S=Start, L=Leaderboard, A=Audio, Q/ESC=Quit).
  - Ability to return to the Main Menu from Game Over, Leaderboard, or Audio Settings screen via ESC or M.
- Persistent Leaderboard (`leaderboard_manager.py`):
  - Local database storage using SQLite (`sqlite.db`).
  - Table `leaderboard` with columns: `id`, `player_name`, `score`, `created_at`.
  - Automatic creation and persistence of `sqlite.db` in repository root or configurable path.
  - Record scores when game finishes.
  - Retrieve top high scores (e.g., top 5 or 10 scores) sorted descending.
  - Persistent High Score display on HUD during active gameplay.
  - Dedicated Leaderboard view screen showing ranking, score, and date/time.
- Gameplay Polish:
  - Game pause toggle via `P` key with "PAUSED" overlay indicator.
  - Prevent game physics and entity updates while in `PAUSED` state.
  - Visual collision shield glow & boundary border around the player ship model matching its mathematical collision circle radius.

### Out-of-Scope (Non-Goals)
- Networked remote score synchronization or cloud authentication.
- Complex particle physics systems.

## 3. Constraints & Dependencies
- Pygame mixer module (`pygame.mixer`).
- Audio playback must never crash the game if audio output is unavailable or muted.
- SQLite standard library (`sqlite3` in Python stdlib).
- Database operations must be thread-safe, resilient to missing files, and ensure persistence across application restarts.
- Modularity rule: all modules must be strictly under 300 lines each.

## 4. Acceptance Criteria
- [x] **AC-3.1**: `sound_manager.py` initializes without errors; if no audio hardware is found, it silently disables sound without crashing.
- [x] **AC-3.2**: Sound effects trigger upon firing shots, splitting asteroids, and player death (no thrust movement sound).
- [x] **AC-3.3**: Pressing `M` toggles all audio on and off cleanly during gameplay.
- [x] **AC-3.4**: Player ship wraps around all screen boundaries seamlessly (horizontal and vertical edges).
- [x] **AC-3.5**: SQLite database `sqlite.db` stores leaderboard entries, ensures data persistence across sessions, and tracks all-time high score.
- [x] **AC-3.6**: Clear Menu system allows starting game, viewing the leaderboard, accessing audio settings, and quitting cleanly.
- [x] **AC-3.7**: Leaderboard view displays top scores persisted in `sqlite.db` with option to return to menu.
- [x] **AC-3.8**: Pressing `P` toggles pause state, freezing movement and rendering a "PAUSED" indicator.
- [x] **AC-3.9**: Background music plays continuously on loop at low volume (default 0.20) with safe fallback.
- [x] **AC-3.10**: Separate volume controls allow independently adjusting background music volume and sound effect volume.
- [x] **AC-3.11**: Player ship renders a visible energy glow and boundary border around the ship model matching its collision circle radius.

## 5. Edge Cases & Error Handling
- **Headless / dummy audio driver**: `pygame.mixer.init()` failing or unavailable must be caught gracefully (`try...except pygame.error`) with an internal `enabled = False` flag.
- **Missing or corrupted database**: `leaderboard_manager.py` handles fresh creation and catches schema errors cleanly.
- **Wrapping edge stutter**: Position wrapping must take entity radius into account or wrap smoothly at edge boundaries without bouncing loops.
