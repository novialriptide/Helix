from SakuyaEngine.scene import Scene
from SakuyaEngine.controllers import BaseController

from Helix.abilties.ability import Ability

import pygame


class TargetFire(Ability):
    def __init__(self, cooldown: int, scene: Scene, controller: BaseController) -> None:
        super().__init__(cooldown, scene)

        self.selected_targets = []
        self.color1 = (24, 123, 43)
        self.controller = controller
        self.position = None
        self.speed = 3

    def start(self, position: pygame.Vector2) -> None:
        self.position = position
        self.active = True
        self.scene.client.delta_time_modifier = 0.25

    def draw(self, offset=pygame.Vector2(0, 0)) -> None:
        pygame.draw.circle(self.scene.screen, self.color1, self.position + offset, 3)
        for t in self.selected_targets:
            pygame.draw.circle(
                self.scene.screen,
                self.color1,
                t.center_position + offset,
                t.custom_hitbox_size.x,
                width=3,
            )  # draw a spinning rect or triangle

    def update(self, delta_time: float) -> None:
        delta_time /= self.scene.client.delta_time_modifier
        if self.active:
            m = self.controller.movement
            if m.magnitude() != 0:
                m.normalize_ip()
            m *= self.speed * delta_time
            self.position += m
            for e in self.scene.entities:
                if (
                    e.custom_hitbox.collidepoint(self.position)
                    and "player" not in e.tags
                    and e not in self.selected_targets
                ):
                    self.selected_targets.append(e)

        # print(self.selected_targets)
