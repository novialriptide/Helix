from Helix.Sakuya.events import EventSystem, RepeatEvent
from Helix.Sakuya.waves import WaveManager
from Helix.Sakuya.entity import Entity
from Helix.Sakuya.math import Vector

spawn_animations = [
    {"spawn_position_offset": Vector(0, 0),
    "allowed_spawnpoints": [0, 1, 2, 3, 4]}
]

class HelixWaves(WaveManager):
    def spawn(
        self,
        entity_key: int,
        spawn_key: int,
        spawn_anim: int,
        event_system: EventSystem,
        delta_time: float
    ) -> Entity:
        e = self.entities[entity_key].copy()
        e.position = spawn_animations[spawn_anim]["spawn_position_offset"] - e.center_position

        def event_func(entity: Entity, target: Vector):
            entity.position = entity.position.move_toward(target - e.center_position, entity.controller.speed * delta_time())
            return entity.position != target
            
        event = RepeatEvent("move_enemy", event_func, args=[e, self.spawn_points[spawn_key]])
        event_system._methods.append(event)

        return e