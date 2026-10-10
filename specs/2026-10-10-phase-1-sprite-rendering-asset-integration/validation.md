# Validation & Merge Readiness: Phase 1 - Sprite Rendering & Asset Integration

## 1. Acceptance Criteria Verification Matrix

| AC ID | Description | Verification Method | Pass / Fail |
|---|---|---|---|
| AC-1.1 | `asset_loader.py` loads and caches all 5 asset textures | Automated Test: `tests/test_asset_loader.py` | [ ] |
| AC-1.2 | `background.png` renders smoothly at 1280x720 | Manual Verification: launch game & inspect background | [ ] |
| AC-1.3 | `Player.draw` blits rotated spaceship sprite aligned to heading | Manual Verification: rotate ship 360 degrees & fire | [ ] |
| AC-1.4 | `Asteroid.draw` blits appropriate tiered sprite for each size | Manual Verification: check large, mid, small asteroids | [ ] |
| AC-1.5 | Circle collision detection remains mathematically intact | Automated Test: `tests/test_collision.py` | [ ] |
| AC-1.6 | Game maintains smooth 60 FPS performance | Manual Verification: check clock tick / FPS counter | [ ] |

## 2. Automated Test Suite
- `tests/test_asset_loader.py`: Validates AC-1.1 (asset loading, caching, scaling).
- `tests/test_collision.py`: Validates AC-1.5 (regression test confirming collision math is unaffected).
- `scripts/check_line_counts.py`: Validates file length constraint (<= 300 lines).

## 3. Manual Verification Checklist
1. Launch game via `uv run main.py`.
2. Verify space background is drawn without distortion across the full 1280x720 window.
3. Pilot spaceship: rotate in all directions, verify sprite nose matches flight direction and shot origin.
4. Shoot asteroids: verify big asteroid displays `asteriods_big.png`, medium fragments display `asteriods_mid.png`, and smallest fragments display `asteriods_small.png`.
5. Observe collision: verify collision triggers when ship touches asteroid edge, exactly as before.

## 4. Merge Readiness (Definition of Done)
- [ ] All task groups in `plan.md` marked complete.
- [ ] All ACs in `requirements.md` verified in matrix above.
- [ ] Automated tests pass without errors (`uv run pytest`).
- [ ] No file exceeds 300 lines limit.
