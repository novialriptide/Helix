from typing import List

from Helix.Sakuya.controllers import BaseController
from Helix.Sakuya.entity import Entity
from Helix.Sakuya.math import Vector
from Helix.Sakuya.particles import Particles

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
        super().__init__(0.3)

class EnemyEntity(Entity):
    def __init__(
        self,
        controller: BaseController,
        position: Vector,
        has_collision: bool = True,
        has_rigidbody: bool = False,
        scale: int = 1,
        particle_systems: List[Particles] = []
    ):
        super().__init__(
            controller,
            position,
            has_collision=has_collision,
            has_rigidbody=has_rigidbody,
            scale=scale,
            particle_systems=particle_systems
        )

    def move_to(self, target: Vector, distance: int) -> None:
        """Move towards a target
        
        Parameters:
            target: The target's position.
            distance: The target distance between itself and the target.

        """
        true_distance = target.x - self.position.x

        print(true_distance)
        if true_distance > 0 and abs(true_distance) > distance:
            self.controller.is_moving_right = True
            self.controller.is_moving_left = False

        if true_distance < 0 and abs(true_distance) > distance:
            self.controller.is_moving_right = False
            self.controller.is_moving_left = True