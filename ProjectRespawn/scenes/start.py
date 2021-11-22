import sys
import pygame

from ProjectRespawn.playercontroller import PlayerController
from ProjectRespawn.Sakuya.entity import Entity
from ProjectRespawn.Sakuya.animation import Animation
from ProjectRespawn.Sakuya.scene import Scene
from ProjectRespawn.Sakuya.math import Vector
from ProjectRespawn.buttons import BUTTONS

class Start(Scene):
    def __init__(self, client):
        super().__init__(client)

    def on_awake(self, **kwargs) -> None:
        player_placeholder = Animation("player_placeholder", [pygame.image.load("ProjectRespawn\sprites\guy.png")])
        self.player_entity = Entity(PlayerController, Vector(0, 0))
        self.player_entity.anim_add(player_placeholder)
        self.player_entity.anim_set("player_placeholder")
        self.entities = [
            self.player_entity
        ]

    def update(self, **kwargs) -> None:
        controller = self.player_entity.controller

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == BUTTONS["left"]:
                    controller.is_moving_left = True
                if event.key == BUTTONS["right"]:
                    controller.is_moving_right = True
                if event.key == BUTTONS["up"]:
                    controller.is_moving_up = True
                if event.key == BUTTONS["down"]:
                    controller.is_moving_down = True
            if event.type == pygame.KEYUP:
                if event.key == BUTTONS["left"]:
                    controller.is_moving_left = False
                if event.key == BUTTONS["right"]:
                    controller.is_moving_right = False
                if event.key == BUTTONS["up"]:
                    controller.is_moving_up = False
                if event.key == BUTTONS["down"]:
                    controller.is_moving_down = False

        self.client.screen.fill((0,0,0))

        for e in self.entities:
            e.update(1 / self.client.pg_clock.tick(60))

        for e in self.entities:
            pygame.draw.rect(
                self.client.screen,
                (255,255,255),
                e.rect
            )