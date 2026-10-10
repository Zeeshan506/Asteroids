# Feature Requirements: Phase 3 - Audio & Polish

## 1. Context & Business Intent
As described in [specs/mission.md](file:///home/zeshan6a/Projects/bootdotdev/asteroids/specs/mission.md) and [specs/roadmap.md](file:///home/zeshan6a/Projects/bootdotdev/asteroids/specs/roadmap.md), arcade space combat requires tactile acoustic feedback, classic screen wrap-around boundaries, and persistent high scores across play sessions. This phase delivers audio feedback for weapons and collisions, classic screen boundary wrapping, persistent high-score storage, and gameplay polish.

## 2. Scope
### In-Scope
- Audio Management (`sound_manager.py`):
  - Safe initialization of `pygame.mixer` with robust fallback when sound drivers are absent (e.g. headless containers, missing ALSA devices).
  - Sound effects for:
    - Laser shot fire (`shoot`)
    - Asteroid destruction / split (`asteroid_hit`)
    - Player ship explosion (`player_hit`)
    - Thruster thrust acceleration (`thruster`)
  - Audio mute toggle via `M` keyboard shortcut.
- Screen Boundary Wrap-Around:
  - Spaceship wrapping: exiting any screen edge wraps the ship to the opposing screen edge (left ↔ right, top ↔ bottom).
  - Asteroids wrapping or lifetime boundary management.
  - Shots boundary cleanup (shots despawn when exiting the screen bounds to prevent off-screen accumulation).
- High Score Persistence (`high_score_manager.py`):
  - Read and write high score to a local JSON file (`highscore.json`).
  - Update high score whenever current score exceeds it.
  - Display "HIGH SCORE: [score]" in the HUD.
- Gameplay Polish:
  - Game pause toggle via `P` key with "PAUSED" overlay text.

### Out-of-Scope (Non-Goals)
- Background music soundtrack loops (focused on crisp retro sound effects).
- Cloud leaderboards or networked score submissions.
- Complex particle physics systems.

## 3. Constraints & Dependencies
- Pygame mixer module (`pygame.mixer`).
- Audio playback must never crash the game if audio output is unavailable or muted.
- High score persistence must be resilient to corrupt or missing `highscore.json` files.
- Modularity rule: sound logic and persistence logic must be separated into discrete modules (`sound_manager.py`, `high_score_manager.py`) strictly under 300 lines each.

## 4. Acceptance Criteria
- [ ] **AC-3.1**: `sound_manager.py` initializes without errors; if no audio hardware is found, it silently disables sound without crashing.
- [ ] **AC-3.2**: Sound effects trigger upon firing shots, splitting asteroids, player death, and thruster input.
- [ ] **AC-3.3**: Pressing `M` toggles all audio on and off cleanly during gameplay.
- [ ] **AC-3.4**: Player ship wraps around all screen boundaries seamlessly (horizontal and vertical edges).
- [ ] **AC-3.5**: High score persists to `highscore.json` and survives game restarts; displayed prominently on HUD.
- [ ] **AC-3.6**: Pressing `P` toggles pause state, freezing movement and rendering a "PAUSED" indicator.

## 5. Edge Cases & Error Handling
- **Headless / dummy audio driver**: `pygame.mixer.init()` failing or unavailable must be caught gracefully (`try...except pygame.error`) with an internal `enabled = False` flag.
- **Corrupt `highscore.json`**: If the JSON file contains malformed data or negative numbers, fallback to score 0 and overwrite on next save.
- **Wrapping edge stutter**: Position wrapping must take entity radius into account or wrap smoothly at edge boundaries without bouncing loops.
