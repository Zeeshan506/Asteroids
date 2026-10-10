# Implementation Plan: Phase 3 - Audio, Menu, Leaderboard & Polish

## Overview & Architecture Approach
This phase delivers the complete arcade presentation: tactile audio feedback, screen wrapping, a distinct main menu, a persistent local SQLite database (`sqlite.db`) for leaderboard rankings, and pause capabilities. Audio operations are isolated within `sound_manager.py` with defensive initialization. Database persistence is encapsulated in `leaderboard_manager.py`. Screen wrapping is managed via `screen_wrap.py`. Menu and leaderboard rendering are isolated in `menu.py`. Every module is strictly under 300 lines.

## Task Groups

### Group 1: Audio System Architecture
- [x] Task 1.1: Create `sound_manager.py` with defensive `pygame.mixer.init()` and fallback handling.
- [x] Task 1.2: Implement sound loading for `single_shot.mp3`, `asteroid_destruction.mp3`, player hit, and thruster.
- [x] Task 1.3: Add mute toggle logic (`toggle_mute()`) bound to keyboard shortcut `M`.
- [x] Task 1.4: Add headless unit tests in `tests/test_sound_manager.py` verifying fallback behavior and sound trigger APIs.

### Group 2: Screen Boundary Wrap-Around
- [x] Task 2.1: Implement screen wrapping utility module `screen_wrap.py` (`wrap_position(pos, width, height, margin)`).
- [x] Task 2.2: Integrate wrap-around into `Player.update` so the ship seamlessly reappears on opposing screen edges.
- [x] Task 2.3: Integrate boundary checking in `Shot.update` to kill shots that exit screen bounds.
- [x] Task 2.4: Add unit tests in `tests/test_screen_wrap.py` verifying coordinate wrapping across all 4 boundaries.

### Group 3: SQLite Local Database & Leaderboard Persistence
- [x] Task 3.1: Create `leaderboard_manager.py` handling SQLite connection to `sqlite.db`, table initialization (`leaderboard`), inserting entries, and fetching top scores.
- [x] Task 3.2: Integrate persistent high score retrieval into `GameStateManager` and HUD display.
- [x] Task 3.3: Automatically save final player score to `sqlite.db` on game over.
- [x] Task 3.4: Add unit tests in `tests/test_leaderboard_manager.py` verifying table creation, insertion, queries, and data persistence across instances.

### Group 4: Menu System & Navigation
- [x] Task 4.1: Extend `GameState` enum with `MENU` and `LEADERBOARD` states.
- [x] Task 4.2: Create `menu.py` with `draw_menu()` and `draw_leaderboard()` views with navigation handling.
- [x] Task 4.3: Support keyboard controls (Up/Down/Enter/Space, ESC to back, S to start, L for leaderboard, Q to quit).
- [x] Task 4.4: Add unit tests in `tests/test_menu.py` verifying menu state transitions and navigation inputs.

### Group 5: Game Loop Integration & Pause Polish
- [x] Task 5.1: Integrate `sound_manager`, `leaderboard_manager`, `menu`, and pause toggle into `main.py`.
- [x] Task 5.2: Add pause toggle (`P` key) in `game_state_manager.py` and draw "PAUSED" overlay in `hud.py`.
- [x] Task 5.3: Ensure physics and asteroid updates freeze during `PAUSED` state.

### Group 6: Automated Verification & Modularity Audit
- [x] Task 6.1: Run full headless automated test suite with pytest.
- [x] Task 6.2: Run `scripts/check_line_counts.py` ensuring every file is <= 300 lines.
- [x] Task 6.3: Export test run results to `.agents/test_run_output.txt`.
