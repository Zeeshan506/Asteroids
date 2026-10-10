# Technology Stack & Architectural Constraints

## 1. Agreed Technologies & Frameworks
- **Language / Runtime**: Python >= 3.13 (managed via `.python-version` and `pyproject.toml`)
- **Primary Framework**: Pygame 2.6.1 (`pygame.sprite.Sprite`, `pygame.math.Vector2`)
- **Package & Dependency Manager**: `uv` (`uv.lock`)
- **Testing Framework**: `pytest` for unit and regression testing of core logic
- **Data Stores / Telemetry**: Lightweight JSON Lines logging (`game_events.jsonl`, `game_state.jsonl`)

## 2. Architectural Decisions & Patterns
- **Entity & Sprite System**: Game entities inherit from `CircleShape` / `pygame.sprite.Sprite` and participate in Pygame sprite groups (`updatable`, `drawable`, `asteroids`, `shots`).
- **Separation of Logic & Presentation**:
  - Physics and collision calculations remain pure mathematical operations (circle-circle collision via radii and vectors).
  - Rendering utilizes sprite surfaces with centered blitting aligned to bounding circles.
- **Directory Layout**:
  - `/` (root): Core executable scripts and modular entity modules (`main.py`, `player.py`, `asteroid.py`, etc.).
  - `assets/`: Static image textures (`spaceship.png`, `asteriods_*.png`, `background.png`).
  - `specs/`: SDD constitution, requirements, plans, and validation records.
  - `tests/`: Automated pytest suites verifying physics, collision logic, and state transitions headlessly.

## 3. Engineering Constraints & Rules
- **File Modularity Limit**: Strict project constraint: no code or spec file may exceed 300 lines (excluding generated lockfiles). Large classes or managers must be decomposed into small, focused submodules.
- **Type Annotations**: Use Python standard type hints (`typing`) on function signatures and class definitions.
- **Headless Testing**: Game mechanics must be verifiable without opening a GUI window (mocking display surface or testing pure mathematical/state helper functions).
- **Asset Integrity**: Asset paths must be resolved robustly relative to the project root or asset directory without hardcoded absolute paths.

## 4. Deployment & Infrastructure
- **Platform Targets**: Cross-platform desktop (Linux, macOS, Windows).
- **Execution**: Direct launch via `uv run main.py` or `python3 main.py`.
- **CI / Quality Checks**: Syntax checks, pytest execution, and line-length audit scripts.

## 5. Decision Log
- **2026-10-10 - Pygame with uv**: Retained Pygame 2.6.1 and Python 3.13 with `uv` for minimal dependencies and fast execution.
- **2026-10-10 - Strict 300-Line Limit**: Mandated module decomposition to prevent context exhaustion and maintain readability for autonomous agents.
- **2026-10-10 - Asset-backed 2D Sprites**: Decided to replace initial vector outlines with the prepared sprite textures in `assets/`.
