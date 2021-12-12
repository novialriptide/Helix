"""
Helix: Flight Test (c) 2021 Andrew Hong
This code is licensed under MIT license (see LICENSE for details)
"""
from Helix.SakuyaEngine.events import EventSystem, RepeatEvent, WaitEvent
from Helix.SakuyaEngine.waves import WaveManager
from Helix.SakuyaEngine.entity import Entity
from Helix.SakuyaEngine.math import vector2_move_toward

import pygame

spawn_animations = [
    {"spawn_position_offset": pygame.math.Vector2(0, -100),
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

        def move_spawn_func(entity: Entity, target: pygame.math.Vector2):
            # Event that will move the entity to its target position upon spawning.
            entity.position = vector2_move_toward(entity.position, target - e.center_offset, entity.speed * delta_time())
            return entity.position != target - e.center_offset

        def move_func(_entity: Entity, _target: pygame.math.Vector2):
            # Event that will move the entity to its eventual deletion.
            _entity.position = vector2_move_toward(_entity.position, _target - e.center_offset, _entity.speed * delta_time())
            if _entity.position == _target - e.center_offset:
                _entity._is_destroyed = True
            return _entity.position != _target - e.center_offset

        def move_despawn_func(entity: Entity, spawn_anim: int, spawn_key: int):
            # Event that will wait until it's time for it to despawn and execute the despawn movement.
            move_back_event = RepeatEvent("move_enemy", move_func, args=[
                entity, spawn_anim["spawn_position_offset"] + self.spawn_points[spawn_key]
            ])
            event_system._methods.append(move_back_event)

        spawn_anim = spawn_animations[spawn_anim]
        e.position = spawn_anim["spawn_position_offset"] - e.center_offset + self.spawn_points[spawn_key]
        event = RepeatEvent("move_enemy", move_spawn_func, args=[e, self.spawn_points[spawn_key]])
        event_system._methods.append(event)

        if lifetime != 0:
            wait_moveback_enemy = WaitEvent("wait_moveback_enemy", lifetime, move_despawn_func, args=[e, spawn_anim, spawn_key])
            event_system._methods.append(wait_moveback_enemy)

        return e