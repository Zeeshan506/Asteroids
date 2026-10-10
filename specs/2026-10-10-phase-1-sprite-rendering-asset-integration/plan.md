# Implementation Plan: Phase 1 - Sprite Rendering & Asset Integration

## Overview & Architecture Approach
This phase introduces 2D graphical rendering into the game. A dedicated `asset_loader.py` module manages texture loading, caching, and dimension scaling. `Player` and `Asteroid` entities are updated to blit these cached surfaces centered on their physics positions (`self.position`), using `pygame.transform.rotate` with center-rect anchoring to avoid angular jitter. Pure vector collision logic remains intact.

## Task Groups

### Group 1: Asset Loader Module
- [x] Task 1.1: Create `asset_loader.py` with caching dictionary for loaded and scaled surfaces.
- [x] Task 1.2: Implement `load_image(filename: str, size: tuple[int, int] | None = None) -> pygame.Surface` resolving paths relative to project root.
- [x] Task 1.3: Add helper methods `get_asteroid_surface(radius: float) -> pygame.Surface` and `get_player_surface() -> pygame.Surface`.
- [x] Task 1.4: Add unit tests in `tests/test_asset_loader.py` verifying cache hits, path resolution, and surface dimensions.

### Group 2: Background Rendering Integration
- [x] Task 2.1: Load and scale `background.png` to `(SCREEN_WIDTH, SCREEN_HEIGHT)` in `main.py` via `asset_loader`.
- [x] Task 2.2: Replace `screen.fill("black")` with `screen.blit(background_surface, (0, 0))` in the render loop.

### Group 3: Player Sprite Rendering
- [x] Task 3.1: Update `Player.__init__` to acquire base player texture from `asset_loader`.
- [x] Task 3.2: Update `Player.draw` to rotate base texture by `-self.rotation` (or aligned angle offset) and blit using `rect = rotated_surf.get_rect(center=self.position)`.
- [x] Task 3.3: Verify player heading visually matches bullet trajectory and forward movement vector.

### Group 4: Asteroid Sprite Rendering & Tier Mapping
- [x] Task 4.1: Update `Asteroid.__init__` to retrieve tier-matched surface (`asteriods_big.png`, `asteriods_mid.png`, `asteriods_small.png`) scaled to `(radius * 2, radius * 2)`.
- [x] Task 4.2: Update `Asteroid.draw` to blit scaled surface centered on `self.position`.
- [x] Task 4.3: Ensure `Asteroid.split` instantiates child asteroids with correct tier-matched sprites upon division.

### Group 5: Validation & Modularity Audit
- [x] Task 5.1: Run headless test suite to ensure collision math and state updates are completely unregressed.
- [x] Task 5.2: Verify all modified and new files remain strictly under 300 lines.
