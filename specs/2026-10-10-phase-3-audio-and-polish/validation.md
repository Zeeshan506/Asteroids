# Validation & Merge Readiness: Phase 3 - Audio & Polish

## 1. Acceptance Criteria Verification Matrix

| AC ID | Description | Verification Method | Pass / Fail |
|---|---|---|---|
| AC-3.1 | Safe mixer initialization with silent fallback if hardware is absent | Automated Test: `tests/test_sound_manager.py` | [ ] |
| AC-3.2 | Sound triggers for shots, explosions, collisions, and thrusters | Manual Verification: play game with audio output | [ ] |
| AC-3.3 | Pressing M toggles audio mute | Manual Verification: toggle M during sound playback | [ ] |
| AC-3.4 | Player ship wraps around all screen edges | Automated Test: `tests/test_screen_wrap.py` | [ ] |
| AC-3.5 | High score persists to `highscore.json` and updates HUD | Automated Test: `tests/test_high_score.py` | [ ] |
| AC-3.6 | Pressing P toggles pause state and overlay | Manual Verification: press P during game | [ ] |

## 2. Automated Test Suite
- `tests/test_sound_manager.py`: Validates AC-3.1 (safe mixer init, fallback, mute state).
- `tests/test_screen_wrap.py`: Validates AC-3.4 (boundary coordinate wrapping math).
- `tests/test_high_score.py`: Validates AC-3.5 (high score save, load, and corruption handling).
- `scripts/check_line_counts.py`: Validates file length constraint (<= 300 lines).

## 3. Manual Verification Checklist
1. Launch game via `uv run main.py`.
2. Fire weapon: verify laser audio triggers.
3. Accelerate: verify thruster hum triggers.
4. Collide or destroy asteroid: verify explosion audio triggers.
5. Press `M`: verify all sounds mute; press `M` again to unmute.
6. Fly ship past the right screen boundary: verify ship emerges seamlessly on the left.
7. Fly ship past the top screen boundary: verify ship emerges seamlessly at the bottom.
8. Score points exceeding current high score: verify High Score on HUD updates immediately.
9. Close and relaunch game: verify persisted High Score is reloaded.
10. Press `P`: verify game freezes and "PAUSED" appears; press `P` again to resume.

## 4. Merge Readiness (Definition of Done)
- [ ] All task groups in `plan.md` marked complete.
- [ ] All ACs in `requirements.md` verified in matrix above.
- [ ] Automated tests pass without errors (`uv run pytest`).
- [ ] No file exceeds 300 lines limit.
