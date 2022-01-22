from typing import List

from SakuyaEngine.entity import Entity
from SakuyaEngine.clock import Clock

import pygame
import random

core_png = pygame.image.load("Helix/sprites/core.png").convert_alpha()

core_component = Entity("core", static_sprite=core_png)
registered_components = [
    Entity("sub1", static_sprite=core_png),
    Entity("sub2", static_sprite=core_png),
    Entity("sub3", static_sprite=core_png),
    Entity("sub4", static_sprite=core_png),
    Entity("sub5", static_sprite=core_png),
    Entity("sub6", static_sprite=core_png),
    Entity("sub7", static_sprite=core_png),
    Entity("sub8", static_sprite=core_png),
]


class BossEntity(Entity):
    def __init__(
        self,
        seed: str,
        component_sum: int,
        name: str = None,
        tags: List[str] = [],
        scale: int = 1,
        position: pygame.Vector2 = pygame.Vector2(0, 0),
        speed: float = 0,
        target_position: pygame.Vector2 or None = None,
        disable_bulletspawner_while_movement: bool = True,
        clock: Clock or None = None,
    ):
        super().__init__(
            name=name,
            tags=tags,
            scale=scale,
            position=position,
            speed=speed,
            target_position=target_position,
            disable_bulletspawner_while_movement=disable_bulletspawner_while_movement,
            clock=clock,
        )

        self.seed = seed
        self.component_sum = component_sum
        self.components = [{"x": 0, "y": 0, "compon": core_component}]

        random.seed(self.seed)
        for c in range(self.component_sum):
            last_component = self.components[-1]
            rand_com = random.choice(registered_components)
            pos = [0, 0]
            chance = random.randint(0, 1) == 1
            if chance:
                pos[1] = random.randint(-1, 1)
            
            if pos[1] == 0 or not chance:
                pos[0] = random.randint(-1, 1)
            
            self.components.append(
                {
                    "x": pos[0] + last_component["x"],
                    "y": pos[1] + last_component["y"],
                    "compon": rand_com,
                }
            )

    def draw(self, surface: pygame.Surface) -> None:
        for c in self.components:
            sprite = c["compon"].sprite
            width, height = sprite.get_size()
            surface.blit(
                sprite, self.abs_position + pygame.Vector2(c["x"] * width, c["y"] * height)
            )
