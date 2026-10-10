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
