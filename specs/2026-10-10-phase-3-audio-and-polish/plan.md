# Implementation Plan: Phase 3 - Audio & Polish

## Overview & Architecture Approach
This phase completes the arcade experience by layering sound effects, screen wrapping, high-score persistence, and pause capabilities. Audio operations are isolated within `sound_manager.py` with defensive initialization. Persistence is handled by `high_score_manager.py`. Screen wrap math is implemented as a clean modular utility, ensuring complete decoupling and keeping every module under 300 lines.

## Task Groups

### Group 1: Audio System Architecture
- [ ] Task 1.1: Create `sound_manager.py` with defensive `pygame.mixer.init()` and fallback handling.
- [ ] Task 1.2: Implement sound synthesis or lightweight audio loading for `laser`, `explosion`, `hit`, and `thruster`.
- [ ] Task 1.3: Add mute toggle logic (`toggle_mute()`) bound to keyboard shortcut `M`.
- [ ] Task 1.4: Add headless unit tests in `tests/test_sound_manager.py` verifying fallback behavior when mixer is uninitialized.

### Group 2: Screen Boundary Wrap-Around
- [ ] Task 2.1: Implement screen wrapping utility function or method `wrap_position(pos, width, height, margin) -> pygame.Vector2`.
- [ ] Task 2.2: Integrate wrap-around into `Player.update` so the ship seamlessly reappears on opposing screen edges.
- [ ] Task 2.3: Integrate boundary checking in `Shot.update` to kill shots that exit screen bounds.
- [ ] Task 2.4: Add unit tests in `tests/test_screen_wrap.py` verifying coordinate wrapping across all 4 boundaries.

### Group 3: High Score Persistence
- [ ] Task 3.1: Create `high_score_manager.py` managing loading, updating, and saving `highscore.json`.
- [ ] Task 3.2: Integrate high-score checks into `game_state_manager.py` when score increments.
- [ ] Task 3.3: Update `hud.py` to display "HIGH SCORE: [score]" centered or alongside current score.
- [ ] Task 3.4: Add unit tests in `tests/test_high_score.py` testing serialization, deserialization, and corrupted JSON recovery.

### Group 4: Pause State & UI Polish
- [ ] Task 4.1: Add `PAUSED` state to `game_state_manager.py` toggled by `P` key.
- [ ] Task 4.2: Add "PAUSED" text overlay in `hud.py` when game is paused.
- [ ] Task 4.3: Prevent game physics and entity updates while in `PAUSED` state.

### Group 5: Validation & Modularity Audit
- [ ] Task 5.1: Run full headless automated test suite.
- [ ] Task 5.2: Check all repository files against the 300 lines limit.
