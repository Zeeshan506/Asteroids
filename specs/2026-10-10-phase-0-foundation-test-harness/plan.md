# Implementation Plan: Phase 0 - Foundation & Headless Test Harness

## Overview & Architecture Approach
This phase establishes the foundational test harness using `pytest` managed by `uv`. By configuring a headless dummy video driver and creating dedicated unit test modules for physics, player state, and asteroid logic, subsequent feature phases can rely on automated regression testing. Additionally, a modularity verification check ensures repository-wide compliance with the 300-line constraint.

## Task Groups

### Group 1: Dependency Management & Test Configuration
- [x] Task 1.1: Add `pytest` to `pyproject.toml` dependency specifications and lock dependencies via `uv lock`.
- [x] Task 1.2: Add `conftest.py` in `tests/` configuring headless environment variables (`SDL_VIDEODRIVER="dummy"`).
- [x] Task 1.3: Verify `uv run pytest` executes headlessly and returns exit code 0.

### Group 2: Core Physics & Collision Unit Tests
- [x] Task 2.1: Implement `tests/test_collision.py` testing `CircleShape.collides_with` across intersecting, tangent, and disjoint positions.
- [x] Task 2.2: Implement boundary tests for zero-radius and overlapping center points.

### Group 3: Entity Mechanics Headless Tests
- [x] Task 3.1: Implement `tests/test_player.py` testing rotation accumulation, forward movement vector math, and shoot cooldown decrements.
- [x] Task 3.2: Implement `tests/test_asteroid.py` testing `Asteroid.split` behavior, radius reduction, velocity changes, and minimum radius kill boundary.
- [x] Task 3.3: Implement `tests/test_shot.py` testing velocity application and position updates.

### Group 4: Quality & Modularity Tooling
- [x] Task 4.1: Create a lightweight line-count audit script (e.g. `scripts/check_line_counts.py`) checking all `.py` and `.md` files against the 300-line limit.
- [x] Task 4.2: Add line-count check verification to test suite or project command scripts.
