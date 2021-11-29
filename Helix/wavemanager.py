from Helix.SakuyaEngine.events import EventSystem, RepeatEvent, WaitEvent
from Helix.SakuyaEngine.waves import WaveManager
from Helix.SakuyaEngine.entity import Entity
from Helix.SakuyaEngine.math import Vector

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
        lifetime: int,
        event_system: EventSystem,
        delta_time: float
    ) -> Entity:
        e = self.entities[entity_key].copy()
        e.position = spawn_animations[spawn_anim]["spawn_position_offset"] - e.center_position

        def move_spawn_func(entity: Entity, target: Vector):
            entity.position = entity.position.move_toward(target - e.center_position, entity.controller.speed * delta_time())
            return entity.position != target - e.center_position
            
        event = RepeatEvent("move_enemy", move_spawn_func, args=[e, self.spawn_points[spawn_key]])
        event_system._methods.append(event)

        def move_despawn_func(entity: Entity, spawn_anim: int):
            def move_func(_entity: Entity, _target: Vector):
                _entity.position = _entity.position.move_toward(_target - e.center_position, _entity.controller.speed * delta_time())
                if _entity.position == _target - e.center_position:
                    _entity._is_destroyed = True
                return _entity.position != _target - e.center_position
            
            move_back_event = RepeatEvent("move_enemy", move_func, args=[entity, spawn_animations[spawn_anim]["spawn_position_offset"]])
            event_system._methods.append(move_back_event)
            
        if lifetime != 0:
            wait_moveback_enemy = WaitEvent("wait_moveback_enemy", lifetime, move_despawn_func, args=[e, spawn_anim])
            event_system._methods.append(wait_moveback_enemy)

        return e