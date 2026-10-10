"""Player spaceship module with sprite rendering, flight physics, and screen wrapping."""

from typing import Optional

import pygame

from asset_loader import get_player_surface
from circleshape import CircleShape
from constants import (
    LINE_WIDTH,
    PLAYER_RADIUS,
    PLAYER_SHOOT_COOLDOWN_SECONDS,
    PLAYER_SHOOT_SPEED,
    PLAYER_SPEED,
    PLAYER_TURN_SPEED,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)
from screen_wrap import wrap_position
from shot import Shot
from sound_manager import SoundManager


class Player(CircleShape):
    def __init__(
        self,
        x: float,
        y: float,
        sound_manager: Optional[SoundManager] = None,
    ) -> None:
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0.0
        self.shot_countdown_timer = 0.0
        self.invulnerable = False
        self.image = get_player_surface()
        self.sound_manager: Optional[SoundManager] = sound_manager

    def triangle(self) -> list[pygame.Vector2]:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen: pygame.Surface) -> None:
        if screen is None:
            return
        if self.invulnerable and (pygame.time.get_ticks() // 100) % 2 == 0:
            return

        # Visual collision shield border & glow around ship model
        shield_size = int((self.radius + 6) * 2)
        shield_surf = pygame.Surface((shield_size, shield_size), pygame.SRCALPHA)
        center = (shield_size // 2, shield_size // 2)
        # Soft outer energy glow
        pygame.draw.circle(shield_surf, (0, 200, 255, 45), center, int(self.radius + 3), width=2)
        # Luminous collision boundary border
        border_color = (255, 215, 0, 180) if self.invulnerable else (100, 220, 255, 160)
        pygame.draw.circle(shield_surf, border_color, center, int(self.radius), width=1)
        shield_rect = shield_surf.get_rect(center=self.position)
        screen.blit(shield_surf, shield_rect)

        if self.image is not None:
            rotated_surf = pygame.transform.rotate(self.image, 180 - self.rotation)
            rect = rotated_surf.get_rect(center=self.position)
            screen.blit(rotated_surf, rect)
        else:
            pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)

    def respawn(self) -> None:
        """Reset player position to center and clear rotational / cooldown state."""
        self.position = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.rotation = 0.0
        self.shot_countdown_timer = 0.0
        self.invulnerable = True

    def rotate(self, dt: float) -> None:
        self.rotation += PLAYER_TURN_SPEED * dt

    def update(self, dt: float) -> None:
        keys = pygame.key.get_pressed()
        self.shot_countdown_timer -= dt

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            if self.shot_countdown_timer <= 0:
                self.shot_countdown_timer = PLAYER_SHOOT_COOLDOWN_SECONDS
                self.shoot()

        self.position = wrap_position(self.position)

    def move(self, dt: float) -> None:
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt
        self.position += rotated_with_speed_vector

    def shoot(self) -> Shot:
        new_shot = Shot(self.position.x, self.position.y)
        new_shot.velocity = (
            pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
        )
        if self.sound_manager is not None:
            self.sound_manager.play_shoot()
        return new_shot
