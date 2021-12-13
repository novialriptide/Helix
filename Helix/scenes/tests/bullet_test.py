"""
Helix: Flight Test (c) 2021 Andrew Hong
This code is licensed under MIT license (see LICENSE for details)
"""
import sys
import pygame
import json
from types import SimpleNamespace
from copy import copy


from Helix.SakuyaEngine.entity import Entity
from Helix.SakuyaEngine.animation import Animation

from Helix.SakuyaEngine.scene import Scene
from Helix.SakuyaEngine.bullets import BulletSpawner, Bullet
from Helix.SakuyaEngine.text import text

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
        b = Bullet(None, 3, (255, 0, 0), 5, custom_hitbox_size = pygame.math.Vector2(2, 2), name = "bullet")

        self.bullet_spawner_test = BulletSpawner(
            b,
            iterations = 0, bullets_per_array = 3,
            total_bullet_arrays = 6, fire_rate = 700,
            spread_between_bullet_arrays = 60, spread_within_bullet_arrays = 57,
            bullet_lifetime = 1000, target = self.mp, is_active = True, aim = True,
            position = pygame.math.Vector2(win_size.x / 2, win_size.y / 2)
        )

    def update(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        new_pos = pygame.math.Vector2(pygame.mouse.get_pos())
        self.mp.position = new_pos
        print(self.bullet_spawner_test.target.position)

        self.client.screen.fill((0,0,0))

        for e in self.bullets:
            pygame.draw.rect(self.client.screen, (0, 255, 0), e.custom_hitbox, 1)
        
        self.bullets.extend(self.bullet_spawner_test.update(self.client.delta_time))
        self.advance_frame(self.client.delta_time)