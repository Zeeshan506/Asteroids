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
