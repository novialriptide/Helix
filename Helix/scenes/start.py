import sys
import pygame

from Helix.playercontroller import PlayerController
from Helix.Sakuya.entity import Entity
from Helix.Sakuya.animation import Animation
from Helix.Sakuya.scene import Scene
from Helix.Sakuya.math import Vector
from Helix.Sakuya.tile import split_image
from Helix.buttons import BUTTONS
from Helix.Sakuya.particles import Particles

class Start(Scene):
    def __init__(self, client):
        super().__init__(client)

    def on_awake(self) -> None:
        player_sprites = split_image(
            pygame.image.load("Helix\sprites\ship3.png"), 32, 32
        )

        projectile_sprites = split_image(
            pygame.image.load("Helix\sprites\projectiles.png"), 8, 8
        )

        player_placeholder = Animation(
            "player_placeholder", 
            [
                player_sprites[0],
                player_sprites[1],
            ], fps = 2
        )
        self.player_entity = Entity(PlayerController, Vector(0, 0), has_rigidbody = True)
        self.player_entity.anim_add(player_placeholder)
        self.player_entity.anim_set("player_placeholder")
        self.player_entity.enable_terminal_velocity = False
        self.entities = [
            self.player_entity
        ]
        player_rect = self.player_entity.rect
        self.particle_systems = [
            Particles(
                Vector(0, 5),
                colors=[(249,199,63), (255,224,70), (255, 78, 65)],
                offset=Vector(player_rect.width/2, player_rect.height * 2/3),
                particles_num=30
            )
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

        for ps in self.particle_systems:
            ps.update(self.client.delta_time, self.player_entity.position)
            for p in ps.particles:
                self.client.screen.set_at((int(p.position.x), int(p.position.y)), p.color)

        for e in self.entities:
            e.update(self.client.delta_time)
            self.client.screen.blit(e.sprite, e.position.to_list())