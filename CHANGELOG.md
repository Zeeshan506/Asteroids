# Changelog

All notable changes to the Asteroids project are documented in this file.
The project follows Spec-Driven Development (SDD) with strict separation between specification contracts and feature implementations.

---

## [Unreleased] - 2026-10-10

### 📋 Specification & Planning Changes
- **Project Constitution**: Established [specs/mission.md](file:///home/zeshan6a/Projects/bootdotdev/asteroids/specs/mission.md), [specs/tech-stack.md](file:///home/zeshan6a/Projects/bootdotdev/asteroids/specs/tech-stack.md), and [specs/roadmap.md](file:///home/zeshan6a/Projects/bootdotdev/asteroids/specs/roadmap.md).
- **Phase 0 Specification ([specs/2026-10-10-phase-0-foundation-test-harness/](file:///home/zeshan6a/Projects/bootdotdev/asteroids/specs/2026-10-10-phase-0-foundation-test-harness/))**:
  - Authored `requirements.md`, `plan.md`, and `validation.md` for headless test harness setup (`pytest`), collision/physics unit testing, and modularity verification (`AC-0.1` through `AC-0.6`).
- **Phase 1 Specification ([specs/2026-10-10-phase-1-sprite-rendering-asset-integration/](file:///home/zeshan6a/Projects/bootdotdev/asteroids/specs/2026-10-10-phase-1-sprite-rendering-asset-integration/))**:
  - Authored `requirements.md`, `plan.md`, and `validation.md` for asset loader caching, 2D sprite rendering for player ship and 3 asteroid tiers, and space background rendering (`AC-1.1` through `AC-1.6`).
- **Phase 2 Specification ([specs/2026-10-10-phase-2-scoring-lives-game-loop-state/](file:///home/zeshan6a/Projects/bootdotdev/asteroids/specs/2026-10-10-phase-2-scoring-lives-game-loop-state/))**:
  - Authored `requirements.md`, `plan.md`, and `validation.md` for tiered scoring (20/50/100), player lives (3 lives), respawn invulnerability with flicker, game over state, in-game restart (`R` key), and on-screen HUD (`AC-2.1` through `AC-2.7`).
- **Phase 3 Specification ([specs/2026-10-10-phase-3-audio-and-polish/](file:///home/zeshan6a/Projects/bootdotdev/asteroids/specs/2026-10-10-phase-3-audio-and-polish/))**:
  - Authored `requirements.md`, `plan.md`, and `validation.md` for sound effects with graceful headless fallback, screen edge wrap-around, persistent high score (`highscore.json`), and game pause toggle (`AC-3.1` through `AC-3.6`).
- **Roadmap Synchronization**: Updated [specs/roadmap.md](file:///home/zeshan6a/Projects/bootdotdev/asteroids/specs/roadmap.md) setting all 4 phases to `Specification Status: Ready`, `Implementation Status: Not Started`, and `Validation Status: Pending`.

### 🚀 Feature Implementations
- **Phase 0: Foundation & Headless Test Harness ([specs/2026-10-10-phase-0-foundation-test-harness/](file:///home/zeshan6a/Projects/bootdotdev/asteroids/specs/2026-10-10-phase-0-foundation-test-harness/))**:
  - Configured `pytest` runner and dependencies via `uv` in `pyproject.toml` and `uv.lock` (`AC-0.1`).
  - Implemented headless test environment runner with dummy SDL video/audio drivers in `tests/conftest.py` (`AC-0.2`).
  - Implemented baseline headless collision mathematics unit tests in `tests/test_collision.py` (`AC-0.3`).
  - Implemented player mechanics, rotation, directional movement, and cooldown gating tests in `tests/test_player.py` (`AC-0.4`).
  - Implemented asteroid splitting logic, radius decay, speed scaling, and min-radius boundary tests in `tests/test_asteroid.py` (`AC-0.5`).
  - Added shot mechanics tests in `tests/test_shot.py`.
  - Implemented modularity audit script (`scripts/check_line_counts.py`) and automated verification in `tests/test_modularity.py` enforcing the <= 300 lines constraint across all files (`AC-0.6`).
  - Successfully passed independent QA investigation audit (37 tests passing, 0 failures).
  - Validated by user acceptance and marked ready for merge (`AC-0.1` through `AC-0.6` complete).
- **Phase 1: Sprite Rendering & Asset Integration ([specs/2026-10-10-phase-1-sprite-rendering-asset-integration/](file:///home/zeshan6a/Projects/bootdotdev/asteroids/specs/2026-10-10-phase-1-sprite-rendering-asset-integration/))**:
  - Implemented `asset_loader.py` with caching dictionary and path resolution for textures (`spaceship.png`, `asteriods_big.png`, `asteriods_mid.png`, `asteriods_small.png`, `background.png`) (`AC-1.1`).
  - Integrated 1280x720 scaled space background blitting in `main.py` render loop (`AC-1.2`).
  - Implemented rotated sprite rendering for `Player` in `player.py` centered on `self.position` aligned with forward physics heading (`AC-1.3`).
  - Implemented tier-specific scaled asteroid sprite rendering and split child propagation in `asteroid.py` (`AC-1.4`).
  - Preserved pure Euclidean vector collision detection in `CircleShape.collides_with` without distortion from bounding rects (`AC-1.5`).
  - Ensured single-load caching for smooth 60 FPS performance without per-frame file I/O (`AC-1.6`).
  - Authored comprehensive test suite in `tests/test_asset_loader.py` (55 tests passing, 0 regressions).
  - Successfully passed Independent QA audit with `QA VERDICT: PASSED`.
  - Scaled player / spaceship size by 1.5x (`PLAYER_RADIUS = 30`, sprite diameter 60px) per user feedback.
  - Validated by user manual acceptance and merged into `main` (`AC-1.1` through `AC-1.6` complete).
- **Phase 2: Scoring, Lives & Game Loop State ([specs/2026-10-10-phase-2-scoring-lives-game-loop-state/](file:///home/zeshan6a/Projects/bootdotdev/asteroids/specs/2026-10-10-phase-2-scoring-lives-game-loop-state/))**:
  - Implemented `GameStateManager` tracking tiered score (20/50/100), 3 player lives, respawn invulnerability timers, and restart actions (`AC-2.1`, `AC-2.2`).
  - Implemented player respawn at screen center with 2.0-second invulnerability and high-frequency flicker (`AC-2.3`, `AC-2.4`).
  - Implemented clean `GAME_OVER` transition upon exhausting 3 lives, pausing dynamic world updates (`AC-2.5`).
  - Added in-game restart handler (`R` key) resetting score, lives, asteroids, shots, and player without process restart (`AC-2.6`).
  - Implemented `hud.py` rendering score (top-left), lives (top-right), and centered Game Over banner (`AC-2.7`).
  - Authored unit test suite in `tests/test_game_state.py` (72 tests passing, 0 regressions).
  - Successfully passed Independent QA audit with `QA VERDICT: PASSED`.
  - Validated by user manual acceptance and merged into `main` (`AC-2.1` through `AC-2.7` complete).
