# Validation & Merge Readiness: Phase 2 - Scoring, Lives & Game Loop State

## 1. Acceptance Criteria Verification Matrix

| AC ID | Description | Verification Method | Pass / Fail |
|---|---|---|---|
| AC-2.1 | Hitting asteroids awards tiered points (20, 50, 100) | Automated Test: `tests/test_game_state.py` | [ ] |
| AC-2.2 | Starting with 3 lives; collision decrements 1 life | Automated Test: `tests/test_game_state.py` | [ ] |
| AC-2.3 | Respawn at center with 2.0s invulnerability | Automated Test: `tests/test_game_state.py` | [ ] |
| AC-2.4 | Invulnerability ignores collision and flashes ship | Manual Verification: collide ship once and observe flicker | [ ] |
| AC-2.5 | 0 lives transitions state to GAME_OVER and halts updates | Automated Test: `tests/test_game_state.py` | [ ] |
| AC-2.6 | Pressing R resets state, lives, score, and restarts loop | Manual Verification: reach game over, press R to restart | [ ] |
| AC-2.7 | HUD renders score, lives, and Game Over banner | Manual Verification: inspect HUD during game and game over | [ ] |

## 2. Automated Test Suite
- `tests/test_game_state.py`: Validates AC-2.1, AC-2.2, AC-2.3, AC-2.5 (scoring logic, lives counter, timer decrements, game over transitions).
- `tests/test_collision.py`: Validates regression protection for collision detection.
- `scripts/check_line_counts.py`: Validates file length constraint (<= 300 lines).

## 3. Manual Verification Checklist
1. Launch game via `uv run main.py`.
2. Verify Score is displayed at 0 and Lives at 3 on the HUD.
3. Shoot large, medium, and small asteroids; observe score incrementing by 20, 50, and 100 respectively.
4. Collide with an asteroid: verify lives decrement to 2, ship respawns at center and flickers for 2 seconds while ignoring further collisions.
5. Deplete remaining lives: verify "GAME OVER" banner appears and asteroid movement halts.
6. Press `R`: verify score resets to 0, lives reset to 3, existing asteroids clear, and normal gameplay resumes.

## 4. Merge Readiness (Definition of Done)
- [ ] All task groups in `plan.md` marked complete.
- [ ] All ACs in `requirements.md` verified in matrix above.
- [ ] Automated tests pass without errors (`uv run pytest`).
- [ ] No file exceeds 300 lines limit.
