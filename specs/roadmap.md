# Project Roadmap & Implementation Phases

## Phasing Strategy
The project follows Spec-Driven Development (SDD) with small, testable, and incremental phases. Each phase is specified under `specs/` with dedicated requirements, implementation plans, and validation suites before code is written. All specifications are maintained on the `replanning` branch.

## Phase Overview

| Phase | Title | Objective | Specification Path | Acceptance Criteria | Specification Status | Implementation Status | Validation Status |
|---|---|---|---|---|---|---|---|
| Phase 0 | Foundation & Headless Test Harness | Establish SDD specs, headless test harness (`pytest`), and modularity boundaries | [Phase 0 Spec](./2026-10-10-phase-0-foundation-test-harness/) | AC-0.1 through AC-0.6 | Ready | Implemented | Validated |
| Phase 1 | Sprite Rendering & Asset Integration | Replace vector shapes with 2D sprite textures from `assets/` (ship, asteroids, background) | [Phase 1 Spec](./2026-10-10-phase-1-sprite-rendering-asset-integration/) | AC-1.1 through AC-1.6 | Ready | Implemented | Validated |
| Phase 2 | Scoring, Lives & Game Loop State | Add score tracking, lives counter, respawn immunity, and game over / restart UI | [Phase 2 Spec](./2026-10-10-phase-2-scoring-lives-game-loop-state/) | AC-2.1 through AC-2.7 | Ready | Implemented | Validated |
| Phase 3 | Audio & Polish | Sound effects (laser, explosions, thrust), screen boundaries wrap-around, and high score persistence | [Phase 3 Spec](./2026-10-10-phase-3-audio-and-polish/) | AC-3.1 through AC-3.6 | Ready | Not Started | Pending |

---

### Phase 0: Foundation & Headless Test Harness
- Specification: [specs/2026-10-10-phase-0-foundation-test-harness/](file:///home/zeshan6a/Projects/bootdotdev/asteroids/specs/2026-10-10-phase-0-foundation-test-harness/)
  - [Requirements](file:///home/zeshan6a/Projects/bootdotdev/asteroids/specs/2026-10-10-phase-0-foundation-test-harness/requirements.md)
  - [Plan](file:///home/zeshan6a/Projects/bootdotdev/asteroids/specs/2026-10-10-phase-0-foundation-test-harness/plan.md)
  - [Validation](file:///home/zeshan6a/Projects/bootdotdev/asteroids/specs/2026-10-10-phase-0-foundation-test-harness/validation.md)
- [x] Task 0.1: Configure `pytest` dependency in `pyproject.toml` and lock via `uv lock`.
- [x] Task 0.2: Configure headless environment runner (`SDL_VIDEODRIVER="dummy"` in `conftest.py`).
- [x] Task 0.3: Add baseline headless test suite covering circle collision logic, player movement/rotation, and asteroid splitting.
- [x] Task 0.4: Add line-count audit script checking <= 300 lines rule.
- **Deliverable / Verification**: Fully functioning headless test harness executing cleanly with `uv run pytest`.

### Phase 1: Sprite Rendering & Asset Integration
- Specification: [specs/2026-10-10-phase-1-sprite-rendering-asset-integration/](file:///home/zeshan6a/Projects/bootdotdev/asteroids/specs/2026-10-10-phase-1-sprite-rendering-asset-integration/)
  - [Requirements](file:///home/zeshan6a/Projects/bootdotdev/asteroids/specs/2026-10-10-phase-1-sprite-rendering-asset-integration/requirements.md)
  - [Plan](file:///home/zeshan6a/Projects/bootdotdev/asteroids/specs/2026-10-10-phase-1-sprite-rendering-asset-integration/plan.md)
  - [Validation](file:///home/zeshan6a/Projects/bootdotdev/asteroids/specs/2026-10-10-phase-1-sprite-rendering-asset-integration/validation.md)
- [x] Task 1.1: Create `asset_loader.py` with caching for images (`spaceship.png`, asteroids, `background.png`).
- [x] Task 1.2: Render scaled `background.png` (1280x720) in main loop.
- [x] Task 1.3: Integrate rotated sprite blitting for `Player` centered on `self.position`.
- [x] Task 1.4: Integrate tier-scaled sprite blitting for `Asteroid` across big, mid, and small tiers.
- **Deliverable / Verification**: Game renders visual 2D sprites smoothly at 60 FPS while preserving existing mathematical collision accuracy.

### Phase 2: Scoring, Lives & Game Loop State
- Specification: [specs/2026-10-10-phase-2-scoring-lives-game-loop-state/](file:///home/zeshan6a/Projects/bootdotdev/asteroids/specs/2026-10-10-phase-2-scoring-lives-game-loop-state/)
  - [Requirements](file:///home/zeshan6a/Projects/bootdotdev/asteroids/specs/2026-10-10-phase-2-scoring-lives-game-loop-state/requirements.md)
  - [Plan](file:///home/zeshan6a/Projects/bootdotdev/asteroids/specs/2026-10-10-phase-2-scoring-lives-game-loop-state/plan.md)
  - [Validation](file:///home/zeshan6a/Projects/bootdotdev/asteroids/specs/2026-10-10-phase-2-scoring-lives-game-loop-state/validation.md)
- [x] Task 2.1: Implement `GameStateManager` tracking score (20/50/100 tiered points) and lives (3 lives).
- [x] Task 2.2: Implement player respawn with 2.0s invulnerability period and visual flicker.
- [x] Task 2.3: Implement `GAME_OVER` transition and in-game restart handler (`R` key).
- [x] Task 2.4: Render on-screen HUD (Score, Lives, and Game Over banner) in `hud.py`.
- **Deliverable / Verification**: Full arcade gameplay loop playable from start to game-over to restart.

### Phase 3: Audio & Polish
- Specification: [specs/2026-10-10-phase-3-audio-and-polish/](file:///home/zeshan6a/Projects/bootdotdev/asteroids/specs/2026-10-10-phase-3-audio-and-polish/)
  - [Requirements](file:///home/zeshan6a/Projects/bootdotdev/asteroids/specs/2026-10-10-phase-3-audio-and-polish/requirements.md)
  - [Plan](file:///home/zeshan6a/Projects/bootdotdev/asteroids/specs/2026-10-10-phase-3-audio-and-polish/plan.md)
  - [Validation](file:///home/zeshan6a/Projects/bootdotdev/asteroids/specs/2026-10-10-phase-3-audio-and-polish/validation.md)
- [ ] Task 3.1: Implement `sound_manager.py` with defensive mixer init, sound effects, and mute toggle (`M`).
- [ ] Task 3.2: Implement screen wrap-around boundary math for player spaceship.
- [ ] Task 3.3: Implement persistent high score storage (`highscore.json`) and HUD display.
- [ ] Task 3.4: Implement game pause toggle (`P` key) with paused overlay.
- **Deliverable / Verification**: Polished arcade experience with audio feedback, screen wrapping, and persistent high scores.
