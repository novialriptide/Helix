"""
Helix: Flight Test (c) 2021 Andrew Hong
This code is licensed under MIT license (see LICENSE for details)
"""
from Helix.SakuyaEngine.events import EventSystem, WaitEvent
from Helix.SakuyaEngine.waves import WaveManager
from Helix.SakuyaEngine.entity import Entity

import pygame

spawn_animations = [
    {"spawn_position_offset": pygame.Vector2(0, -100),
    "allowed_spawnpoints": [0, 1, 2, 3, 4]}
]

class HelixWaves(WaveManager):
    def spawn(
        self,
        entity_key: int,
        spawn_key: int,
        spawn_anim: int,
        lifetime: int,
        event_system: EventSystem,
        delta_time: float
    ) -> Entity:
        e = self.entities[entity_key].copy()

        def move_despawn_func(entity: Entity, spawn_anim: int, spawn_key: int):
            # Event that will wait until it's time for it to despawn and execute the despawn movement.
            entity.target_position = spawn_anim["spawn_position_offset"] + self.spawn_points[spawn_key]

        spawn_anim = spawn_animations[spawn_anim]
        e.position = spawn_anim["spawn_position_offset"] - e.center_offset + self.spawn_points[spawn_key]
        e.target_position = self.spawn_points[spawn_key] - e.center_offset

        if lifetime != 0:
            wait_moveback_enemy = WaitEvent("wait_moveback_enemy", lifetime, move_despawn_func, args=[e, spawn_anim, spawn_key])
            event_system._methods.append(wait_moveback_enemy)

        return e