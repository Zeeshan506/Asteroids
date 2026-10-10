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
)
from shot import Shot


class Player(CircleShape):
    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shot_countdown_timer = 0.0
        self.image = get_player_surface()

    # in the Player class
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
        if self.image is not None:
            rotated_surf = pygame.transform.rotate(self.image, 180 - self.rotation)
            rect = rotated_surf.get_rect(center=self.position)
            screen.blit(rotated_surf, rect)
        else:
            pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)

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

    def move(self, dt) -> None:
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt
        self.position += rotated_with_speed_vector

    def shoot(self):
        new_shot = Shot(self.position.x, self.position.y)
        new_shot.velocity = (
            pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
        )
