import sys
import pygame

from Helix.playercontroller import PlayerController
from Helix.Sakuya.entity import Entity
from Helix.Sakuya.animation import Animation
from Helix.Sakuya.scene import Scene
from Helix.Sakuya.math import Vector
from Helix.buttons import BUTTONS

class Start(Scene):
    def __init__(self, client):
        super().__init__(client)

    def on_awake(self, **kwargs) -> None:
        player_placeholder = Animation("player_placeholder", [pygame.image.load("Helix\sprites\guy.png")])
        self.player_entity = Entity(PlayerController, Vector(0, 0), has_rigidbody = True)
        self.player_entity.anim_add(player_placeholder)
        self.player_entity.anim_set("player_placeholder")
        self.player_entity.enable_terminal_velocity = False
        self.entities = [
            self.player_entity
        ]

    def update(self) -> None:
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
                    #self.player_entity.velocity.x = 0
                if event.key == BUTTONS["right"]:
                    controller.is_moving_right = False
                    #self.player_entity.velocity.x = 0
                if event.key == BUTTONS["up"]:
                    controller.is_moving_up = False
                    #self.player_entity.velocity.y = 0
                if event.key == BUTTONS["down"]:
                    controller.is_moving_down = False
                    #self.player_entity.velocity.y = 0

        self.client.screen.fill((0,0,0))
        # self.client.screen.blit(pygame.image.load("C:\\Users\\novia\\Desktop\\s9 _m6_Black_Photo_Upright_Studio_Bundle_440x440.png"), (0,0))

        for e in self.entities:
            e.update(self.client.delta_time)

        for e in self.entities:
            pygame.draw.rect(
                self.client.screen,
                (255,255,255),
                e.rect
            )