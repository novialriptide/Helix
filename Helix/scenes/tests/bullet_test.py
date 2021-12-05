"""
Helix: Flight Test (c) 2021 Andrew Hong
This code is licensed under MIT license (see LICENSE for details)
"""
import sys
import pygame

from Helix.SakuyaEngine.math import Vector
from Helix.SakuyaEngine.scene import Scene
from Helix.SakuyaEngine.bullets import BulletSpawner, Bullet

class BulletTest(Scene):
    def __init__(self, client):
        super().__init__(client)

    def on_awake(self) -> None:
        pygame.joystick.init()
        try:
            self.joystick = pygame.joystick.Joystick(0)
            print(f"Console Controller Detected! [{self.joystick.get_name()}]")
        except:
            self.joystick = None

        self.bullet_spawner_test = BulletSpawner(
            None, Vector(0, 0), None, iterations = 0, bullets_per_array = 4, total_bullet_arrays = 6, fire_rate = 500
        )

    def update(self) -> None:
        win_size = self.client.original_window_size
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        self.client.screen.fill((0,0,0))

        self.bullet_spawner_test.update(self.client.delta_time)