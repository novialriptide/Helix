from typing import List

from Helix.SakuyaEngine.controllers import BaseController
from Helix.SakuyaEngine.entity import Entity
from Helix.SakuyaEngine.math import Vector
from Helix.SakuyaEngine.particles import Particles

"""This handles the AI for a basic enemy

--- Modes ------------------------------------------------------------------
 * Attack       | Always tries to stay at a 
                | safe distance towards its target. 
                | Randomly shoots bullets.
 * Sacrifice    | If the owner's health is low, it
                | will sacrifice itself by suicide-
                | bombing itself towards the target
                | like a Minecraft Creeper.
"""

class EnemyController(BaseController):
    def __init__(self) -> None:
        super().__init__(0.8)

class EnemyEntity(Entity):
    def __init__(
        self,
        position: Vector,
        has_collision: bool = True,
        has_rigidbody: bool = False,
        fire_rate: bool = 0,
        scale: int = 1,
        particle_systems: List[Particles] = [],
        custom_hitbox_size: Vector = Vector(0, 0),
        name: str = None
    ):
        super().__init__(
            EnemyController,
            position,
            has_collision = has_collision,
            has_rigidbody = has_rigidbody,
            scale = scale,
            particle_systems = particle_systems,
            obey_gravity = False,
            fire_rate = fire_rate,
            custom_hitbox_size = custom_hitbox_size,
            name = name
        )
        self.is_combat_ready = False
        
