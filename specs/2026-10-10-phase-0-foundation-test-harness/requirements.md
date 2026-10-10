# Feature Requirements: Phase 0 - Foundation & Headless Test Harness

## 1. Context & Business Intent
According to [specs/mission.md](file:///home/zeshan6a/Projects/bootdotdev/asteroids/specs/mission.md) and [specs/tech-stack.md](file:///home/zeshan6a/Projects/bootdotdev/asteroids/specs/tech-stack.md), game logic, physics, and state transitions must be verifiable headlessly without requiring a graphical display or window manager. Currently, the project lacks an automated test framework and test runner configuration. This phase establishes the headless test framework (`pytest`) and baseline mathematical tests to support Spec-Driven Development (SDD) verification across all subsequent phases.

## 2. Scope
### In-Scope
- Add `pytest` dependency configuration to `pyproject.toml` and update `uv.lock`.
- Establish `tests/` directory structure for unit and regression testing.
- Implement headless environment setup allowing Pygame modules to run without an active display (`SDL_VIDEODRIVER=dummy`).
- Write headless tests for `CircleShape.collides_with` covering overlapping, touching, and distant circles.
- Write headless tests for `Player` rotation, movement vector math, and shot cooldown timing.
- Write headless tests for `Asteroid.split` mathematics (radius decay, child velocity angles).
- Create a line-count verification check to enforce the <= 300 lines-per-file constraint.

### Out-of-Scope (Non-Goals)
- Graphical rendering tests or display surface blit tests (deferred to Phase 1).
- Sound or audio mixer tests (deferred to Phase 3).
- End-to-end user input loop simulation (focus is on pure mathematical and state logic).

## 3. Constraints & Dependencies
- Python >= 3.13 with `uv` package manager.
- Pygame 2.6.1 (`pygame.math.Vector2`, `CircleShape`).
- All code and test files must remain strictly under 300 lines.
- Headless execution must succeed in CI or containerized environments without X11/Wayland.

## 4. Acceptance Criteria
- [x] **AC-0.1**: `pytest` is configured in `pyproject.toml` and executable via `uv run pytest`.
- [x] **AC-0.2**: Pytest runs headlessly without opening an OS window or failing on missing display devices.
- [x] **AC-0.3**: Automated tests in `tests/test_collision.py` verify circle collision detection with 100% mathematical precision.
- [x] **AC-0.4**: Automated tests in `tests/test_player.py` verify rotation calculations, directional movement vectors, and cooldown timers.
- [x] **AC-0.5**: Automated tests in `tests/test_asteroid.py` verify asteroid splitting logic, radius calculations, and speed scaling.
- [x] **AC-0.6**: Line count audit script or rule verifies all repository code and spec files conform to the <= 300 lines limit.

## 5. Edge Cases & Error Handling
- **Zero-distance collision**: Two circles with identical coordinates must evaluate as colliding without division-by-zero errors.
- **Minimum radius split**: An asteroid with radius `<= ASTEROID_MIN_RADIUS` must be destroyed without spawning children.
- **Headless Pygame initialization**: `pygame.init()` or submodules must handle `SDL_VIDEODRIVER=dummy` cleanly without raising display exceptions.
