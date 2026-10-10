# Implementation Plan: Phase 2 - Scoring, Lives & Game Loop State

## Overview & Architecture Approach
This phase introduces game state tracking and user feedback. To keep modules focused and under the 300-line limit, business logic is encapsulated in `game_state_manager.py` (managing score, lives, invulnerability timers, and restart actions), while rendering is isolated in `hud.py`. The `main.py` game loop coordinates event routing, collision response via the state manager, and HUD drawing.

## Task Groups

### Group 1: Game State Manager Foundation
- [x] Task 1.1: Create `game_state_manager.py` with `GameState` enum (`PLAYING`, `GAME_OVER`) and `GameStateManager` class.
- [x] Task 1.2: Implement score methods (`add_asteroid_score(radius: float)`) mapping asteroid sizes to point tiers (20, 50, 100).
- [x] Task 1.3: Implement lives management (`lose_life() -> bool`) managing remaining lives and invulnerability countdown (2.0s).
- [x] Task 1.4: Implement `restart()` method resetting score to 0, lives to 3, and state to `PLAYING`.
- [x] Task 1.5: Add unit tests in `tests/test_game_state.py` covering score additions, life decrements, invulnerability transitions, and restarts.

### Group 2: Player Respawn & Invulnerability Integration
- [x] Task 2.1: Add `respawn()` method to `Player` resetting position to `(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)` and rotation to 0.
- [x] Task 2.2: Add `is_invulnerable` flag or timer check to player collision handling in `main.py`.
- [x] Task 2.3: Implement visual flicker in `Player.draw` during invulnerability (alternate blit visibility or alpha modulation).

### Group 3: Game Over & In-Game Restart
- [x] Task 3.1: Update collision loop in `main.py`: when player collides with an asteroid, call `state_manager.lose_life()`; if lives reach 0, transition to `GAME_OVER`.
- [x] Task 3.2: When `GAME_OVER`, freeze asteroid and player updates while continuing display render.
- [x] Task 3.3: Handle `pygame.KEYDOWN` for `pygame.K_r` to trigger state reset and clear active sprite groups (`asteroids.empty()`, `shots.empty()`).

### Group 4: HUD & UI Rendering
- [x] Task 4.1: Create `hud.py` initializing font rendering.
- [x] Task 4.2: Implement `draw_hud(screen, state_manager)` drawing score (top-left) and remaining lives (top-right).
- [x] Task 4.3: Implement `draw_game_over(screen, state_manager)` drawing centered "GAME OVER", final score, and "Press R to Restart".

### Group 5: Validation & Modularity Audit
- [x] Task 5.1: Run headless test suite to verify scoring, life loss, and restart logic headlessly.
- [x] Task 5.2: Check all file line counts ensuring adherence to the <= 300 lines limit.
