# Project Mission & Guiding Principles

## 1. Core Purpose & Philosophy
The Asteroids project is an authentic, engaging 2D arcade space shooter inspired by the classic Asteroids arcade game. The goal is to provide players with responsive, satisfying space piloting and shooting gameplay, featuring clean physics, progressive asteroid splitting, and crisp 2D sprite presentation.

## 2. Stakeholder Alignment
- **Primary Stakeholders**: Players.
- **Core Expectation**: Smooth, fun, responsive, and bug-free arcade experience that runs out of the box with zero friction, responsive controls, and clear visual feedback.

## 3. Target Audience & User Personas
- **Arcade Enthusiasts & Casual Gamers**: Players seeking a fast-paced, pick-up-and-play retro action game on desktop.
- **Player Workflow**:
  1. Launch game from terminal/executable.
  2. Pilot the spaceship using intuitive keyboard controls (rotate, thrust, shoot).
  3. Dodge and shoot asteroids, which break down into smaller, faster fragments.
  4. Track survival score, manage lives, and seamlessly restart upon game over.

## 4. Current Goals & Objectives
- Deliver a complete, stable, and fun Asteroids game loop.
- Transition existing vector/wireframe rendering to graphic 2D sprites from the `assets/` directory.
- Provide a clear scoring system, lives management, and game-over/restart state machine.
- Maintain a clean, modular, and testable codebase adhering strictly to the <= 300 lines-per-file constraint.

## 5. Scope Boundaries
### In Scope
- Core spaceship mechanics (rotation, inertia/thrust, boundaries/wrapping, shooting with cooldown).
- Asteroid spawning, field management, collision detection, and multi-tier splitting (large -> medium -> small).
- 2D asset integration: spaceship, 3 asteroid sizes, and space background.
- Score tracking, lives count, and game-over / restart states.
- Automated testing harness for headless game math and state transitions.

### Out of Scope / Non-Goals
- Online multiplayer or networked leaderboards.
- Complex story mode or multi-level campaigns.
- 3D graphics or heavy external game engines (Godot, Unity).
- Microtransactions or external user accounts.

## 6. Guiding Principles
- **Fast & Responsive Controls**: Input latency must feel instantaneous; physics should balance arcade momentum and tight maneuverability.
- **Extreme Modularity**: Prefer many small, focused modules over monolithic classes or files; never exceed 300 lines per file.
- **Headless Testability**: Game logic, collision math, and score/state progressions should be decoupled from the Pygame display loop so they can be unit-tested headlessly.
- **Simplicity Over Overengineering**: Build straightforward, maintainable Python code without unnecessary framework abstractions.
- **Lean & Efficient Verification**: Main agent captures full test execution once to an artifact file; independent QA audits from the file and executes targeted tests only when an issue is detected to avoid duplicate execution waste.
