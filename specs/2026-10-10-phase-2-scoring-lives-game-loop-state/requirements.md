# Feature Requirements: Phase 2 - Scoring, Lives & Game Loop State

## 1. Context & Business Intent
As specified in [specs/mission.md](file:///home/zeshan6a/Projects/bootdotdev/asteroids/specs/mission.md) and [specs/roadmap.md](file:///home/zeshan6a/Projects/bootdotdev/asteroids/specs/roadmap.md), the game currently terminates abruptly via `sys.exit()` upon player collision, without tracking score, managing player lives, or providing a game-over and restart workflow. This phase implements a complete arcade gameplay lifecycle: tracking points earned from destroying asteroids, managing player lives with respawn invulnerability, presenting an on-screen HUD, and transitioning cleanly between `PLAYING` and `GAME_OVER` states with an in-game restart mechanism (`R` key).

## 2. Scope
### In-Scope
- Implement a `GameState` manager (`game_state_manager.py`) tracking:
  - Game status: `PLAYING` vs `GAME_OVER`.
  - Current score with tiered point values (Large = 20 pts, Medium = 50 pts, Small = 100 pts).
  - Player lives counter (starting at 3 lives).
  - Invulnerability timer (2.0 seconds post-respawn) with flicker effect.
- Player respawn mechanics:
  - Center repositioning to `(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)`.
  - Velocity and orientation reset.
  - Immunity to asteroid collisions while invulnerable.
- Game Over and Restart:
  - Transition to `GAME_OVER` when lives reach 0.
  - Listen for `R` key during `GAME_OVER` to clear asteroid field, restore 3 lives, reset score to 0, and restart gameplay without restarting the process.
- On-Screen HUD (`hud.py`):
  - Render Score at top-left.
  - Render Lives count at top-right.
  - Render centered Game Over banner with final score and restart prompt.

### Out-of-Scope (Non-Goals)
- Persistent disk storage for high scores (deferred to Phase 3: Audio & Polish).
- Pause / resume menu state (ESC pause menu deferred to Phase 3).
- Graphical health bars or power-ups (Asteroids uses classic discrete lives).

## 3. Constraints & Dependencies
- Pygame font module (`pygame.font.Font` or `pygame.font.SysFont`).
- Pure headless testability: `GameStateManager` must be testable without an active display or font initialization.
- File modularity: state logic and HUD rendering must be separated into dedicated modules (`game_state_manager.py`, `hud.py`) ensuring all files remain under 300 lines.

## 4. Acceptance Criteria
- [ ] **AC-2.1**: Hitting or splitting an asteroid awards points based on size: 20 points for large, 50 points for medium, 100 points for small.
- [ ] **AC-2.2**: Player starts each game with 3 lives. Colliding with an asteroid decrements exactly 1 life.
- [ ] **AC-2.3**: When lives remain after collision, player respawns at screen center with 2.0 seconds of invulnerability.
- [ ] **AC-2.4**: While invulnerable, collisions with asteroids are ignored, and the ship visually flashes/flickers.
- [ ] **AC-2.5**: When lives reach 0, state transitions to `GAME_OVER` and dynamic gameplay updates cease.
- [ ] **AC-2.6**: Pressing `R` in `GAME_OVER` state resets score to 0, lives to 3, clears existing asteroids/shots, respawns the player, and returns to `PLAYING`.
- [ ] **AC-2.7**: HUD displays current score and lives during `PLAYING`, and displays "GAME OVER - Press R to Restart" during `GAME_OVER`.

## 5. Edge Cases & Error Handling
- **Rapid successive collisions**: Collisions must be rejected while the invulnerability timer is active (`invulnerability_timer > 0`).
- **Restart spam**: Pressing `R` while in `PLAYING` state must have no adverse effect.
- **Font fallback**: If default system font is unavailable, fallback gracefully to `pygame.font.get_default_font()` without crashing.
- **Headless tests**: `GameStateManager` methods (`add_score`, `lose_life`, `restart`) must run purely headlessly in pytest without initializing pygame display.
