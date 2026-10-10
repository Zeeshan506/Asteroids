# Validation & Merge Readiness: Phase 0 - Foundation & Headless Test Harness

## 1. Acceptance Criteria Verification Matrix

| AC ID | Description | Verification Method | Pass / Fail |
|---|---|---|---|
| AC-0.1 | `pytest` configured and runnable via `uv run pytest` | Automated Command: `uv run pytest` | [ ] |
| AC-0.2 | Headless execution without requiring graphical display | Automated Test: `pytest` runs under `SDL_VIDEODRIVER=dummy` | [ ] |
| AC-0.3 | Unit tests verify circle collision detection logic | Automated Test: `tests/test_collision.py` | [ ] |
| AC-0.4 | Unit tests verify player movement, rotation, and cooldown | Automated Test: `tests/test_player.py` | [ ] |
| AC-0.5 | Unit tests verify asteroid splitting mathematics | Automated Test: `tests/test_asteroid.py` | [ ] |
| AC-0.6 | Modularity audit confirms no file exceeds 300 lines | Automated Script: line count check script | [ ] |

## 2. Automated Test Suite
- `tests/test_collision.py`: Validates AC-0.3 (circle collision math).
- `tests/test_player.py`: Validates AC-0.4 (player mechanics).
- `tests/test_asteroid.py`: Validates AC-0.5 (asteroid splitting).
- `tests/test_shot.py`: Validates shot mechanics.
- `scripts/check_line_counts.py`: Validates AC-0.6 (modularity limit).

## 3. Manual Verification Checklist
1. Run `uv run pytest` from clean environment: verify all tests pass without GUI window flash.
2. Run line count check script: verify all tracked source files report <= 300 lines.
3. Check `git status` to ensure no transient files or caches are tracked.

## 4. Merge Readiness (Definition of Done)
- [ ] All task groups in `plan.md` marked complete.
- [ ] All ACs in `requirements.md` verified in matrix above.
- [ ] Automated tests pass without errors (`uv run pytest`).
- [ ] No file exceeds 300 lines limit.
