"""
Helix: Flight Test (c) 2021 Andrew Hong
This code is licensed under GNU LESSER GENERAL PUBLIC LICENSE (see LICENSE for details)
"""
import sys
import pygame
import math

from SakuyaEngine.entity import Entity
from SakuyaEngine.animation import Animation

from SakuyaEngine.scene import Scene
from SakuyaEngine.bullets import BulletSpawner, Bullet
from SakuyaEngine.text import text

class BulletTest(Scene):
    def on_awake(self) -> None:
        win_size = self.client.original_window_size
        pygame.joystick.init()
        try:
            self.joystick = pygame.joystick.Joystick(0)
            print(f"Console Controller Detected! [{self.joystick.get_name()}]")
        except:
            self.joystick = None

        self.mp = Entity()
        b = Bullet(
            None,
            3,
            (255, 0, 0),
            5,
            custom_hitbox_size = pygame.Vector2(2, 2),
            name = "bullet"
        )

        self.bullet_spawner_test = BulletSpawner(
            b,
            iterations = 0, bullets_per_array = 2,
            total_bullet_arrays = 10, fire_rate = 50,
            bullet_lifetime = 1000, target = self.mp, is_active = True, aim = True,
            position = pygame.Vector2(win_size.x / 2, win_size.y / 2),
            spread_between_bullet_arrays = 36, spread_within_bullet_arrays = 40,
            bullet_curve = 2, spin_rate = 10
        )

    def update(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        new_pos = pygame.Vector2(pygame.mouse.get_pos())
        self.mp.position = new_pos
        
        self.screen.fill((0,0,0))

        for e in self.bullets:
            pygame.draw.rect(self.screen, (0, 255, 0), e.custom_hitbox, 1)
        
        self.bullets.extend(self.bullet_spawner_test.update(self.client.delta_time))
        self.advance_frame(self.client.delta_time)
        pygame.display.set_caption(f"{self.client._window_name} (fps: {int(self.client.pg_clock.get_fps())})")