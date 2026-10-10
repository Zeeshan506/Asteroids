# Feature Requirements: Phase 1 - Sprite Rendering & Asset Integration

## 1. Context & Business Intent
As outlined in [specs/mission.md](file:///home/zeshan6a/Projects/bootdotdev/asteroids/specs/mission.md), the game currently renders simple vector wireframe lines using `pygame.draw.polygon` and `pygame.draw.circle`. High-quality graphical 2D sprites have been prepared in `assets/` (`spaceship.png`, `asteriods_big.png`, `asteriods_mid.png`, `asteriods_small.png`, and `background.png`). This phase integrates these sprite textures into the rendering pipeline to provide rich arcade visuals while preserving mathematical collision fidelity.

## 2. Scope
### In-Scope
- Create an `asset_loader.py` module responsible for loading, memoizing, and scaling sprite surfaces.
- Render `background.png` at `(0, 0)` scaled to `1280x720` resolution in the main game loop, replacing the black screen fill.
- Replace vector polygon rendering in `Player` with rotated sprite blitting of `spaceship.png` centered on `self.position`.
- Replace vector circle rendering in `Asteroid` with sprite blitting using tier-specific textures (`asteriods_big.png`, `asteriods_mid.png`, `asteriods_small.png`) scaled to each asteroid's bounding circle diameter (`radius * 2`).
- Ensure texture rotation and sprite positioning do not distort or offset the entity's mathematical collision circle (`CircleShape.collides_with`).
- Maintain smooth 60 FPS rendering performance.

### Out-of-Scope (Non-Goals)
- Multi-frame sprite animation or animated thruster flame effects (deferred to future polish).
- Parallax scrolling background (static full-screen background is the objective).
- Vector particle explosions (deferred to Phase 3 audio and polish).

## 3. Constraints & Dependencies
- Assets reside in `assets/` relative to project root.
- Pygame `pygame.transform.smoothscale` or `pygame.transform.scale` and `pygame.transform.rotate`.
- Image conversions must use `.convert_alpha()` (for entities) and `.convert()` (for background) after Pygame display initialization.
- Every source module must remain strictly under 300 lines.
- Headless unit tests must be able to test entities without crashing if display is not initialized (asset loading mocked or guarded).

## 4. Acceptance Criteria
- [x] **AC-1.1**: `asset_loader.py` loads and caches all 5 asset textures (`spaceship.png`, `asteriods_big.png`, `asteriods_mid.png`, `asteriods_small.png`, `background.png`) with robust relative path resolution.
- [x] **AC-1.2**: `background.png` renders smoothly at `(0, 0)` scaled to the screen resolution (`1280x720`).
- [x] **AC-1.3**: `Player.draw` blits `spaceship.png` rotated to match `self.rotation`, with the sprite rect centered exactly on `self.position`.
- [x] **AC-1.4**: `Asteroid.draw` blits `asteriods_big.png` for tier 3, `asteriods_mid.png` for tier 2, and `asteriods_small.png` for tier 1, scaled to `radius * 2` and centered on `self.position`.
- [x] **AC-1.5**: Circle collision logic (`CircleShape.collides_with`) continues to utilize pure vector distance math and is unaffected by sprite bounding boxes.
- [x] **AC-1.6**: Game loop runs smoothly at 60 FPS without memory leaks or per-frame file loading.

## 5. Edge Cases & Error Handling
- **Missing or corrupted asset files**: `asset_loader.py` must raise a clear descriptive `FileNotFoundError` or provide a fallback color surface if an asset fails to load.
- **Rotation jitter / offset drift**: When rotating the player sprite, `get_rect(center=self.position)` must be used to prevent position drift as the sprite bounding box expands during diagonal rotation angles.
- **Headless test execution**: If `pygame.display.get_surface()` is None or Pygame display is uninitialized, `draw()` calls in headless tests must not raise unhandled exceptions.
