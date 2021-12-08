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
from Helix.SakuyaEngine.math import Vector
from Helix.SakuyaEngine.scene import Scene
from Helix.SakuyaEngine.bullets import BulletSpawner, Bullet
from Helix.SakuyaEngine.text import text

from Helix.images import projectile_sprites

class BulletTest(Scene):
    def __init__(self, client):
        super().__init__(client)

    def on_awake(self) -> None:
        win_size = self.client.original_window_size
        pygame.joystick.init()
        try:
            self.joystick = pygame.joystick.Joystick(0)
            print(f"Console Controller Detected! [{self.joystick.get_name()}]")
        except:
            self.joystick = None

        b_anim = Animation(
            "b_anim",
            [projectile_sprites[0], projectile_sprites[1], projectile_sprites[2]],
            fps = 4
        )

        e = Entity(custom_hitbox_size = Vector(3, 3), position = Vector(win_size.x / 2, win_size.y / 2))
        b = Bullet(None, 3, (255, 0, 0), 5, custom_hitbox_size = Vector(2, 2), name = "bullet")
        b.anim_add(copy(b_anim))
        b.anim_set("b_anim")

        self.bullet_spawner_test = BulletSpawner(
            e, b, self.entities,
            iterations = 3, bullets_per_array = 3,
            total_bullet_arrays = 6, fire_rate = 700,
            spread_between_bullet_arrays = 60, spread_within_bullet_arrays = 57,
            bullet_lifetime = 1000, bullet_curve = 2
        )

    def update(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        self.client.screen.fill((0,0,0))

        for e in self.entities:
            pygame.draw.rect(self.client.screen, (0, 255, 0), e.custom_hitbox, 1)

        fps = text(f"fps: {int(self.client.pg_clock.get_fps())}", 10, "Arial", (0, 255, 0))
        object_count = text(f"object count: {len(self.entities)}", 10, "Arial", (0, 255, 0))
        self.client.screen.blit(fps, (0, 0))
        self.client.screen.blit(object_count, (0, 10))
        
        self.bullet_spawner_test.update(self.client.delta_time)
        self.advance_frame(self.client.delta_time)