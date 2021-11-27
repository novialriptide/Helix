import sys
import pygame

from copy import copy

from Helix.playercontroller import PlayerController
from Helix.enemy import EnemyEntity, EnemyController
from Helix.Sakuya.entity import Entity
from Helix.Sakuya.animation import Animation
from Helix.Sakuya.scene import Scene
from Helix.Sakuya.math import Vector
from Helix.Sakuya.tile import split_image
from Helix.buttons import KEYBOARD
from Helix.Sakuya.particles import Particles

class Start(Scene):
    def __init__(self, client):
        super().__init__(client)

    def on_awake(self) -> None:
        pygame.joystick.init()

        player_sprites = split_image(
            pygame.image.load("Helix\sprites\ship3.png"), 32, 32
        )

        enemy_sprites = split_image(
            pygame.image.load("Helix\sprites\ship.png"), 16, 16
        )

        projectile_sprites = split_image(
            pygame.image.load("Helix\sprites\projectiles.png"), 8, 8
        )

        enemy_idle_anim = Animation(
            "enemy_idle_anim",
            enemy_sprites,
            fps = 2
        )

        self.enemy_entity = EnemyEntity(EnemyController, Vector(0, 0), has_rigidbody = True)
        self.enemy_entity.anim_add(enemy_idle_anim)
        self.enemy_entity.anim_set("enemy_idle_anim")

        player_idle_anim = Animation(
            "player_idle_anim", 
            player_sprites,
            fps = 2
        )
        win_size = self.client.original_window_size
        self.player_entity = Entity(PlayerController, Vector(win_size.x/2, win_size.y/2), has_rigidbody = True)
        self.player_entity.anim_add(player_idle_anim)
        self.player_entity.anim_set("player_idle_anim")
        player_rect = self.player_entity.rect
        self.player_entity.particle_systems = [
            Particles(
                Vector(0, 5),
                colors=[(249,199,63), (255,224,70), (255, 78, 65)],
                offset=Vector(player_rect.width/2, player_rect.height * 2/3),
                particles_num=30
            )
        ]
        self.entities = [
            self.player_entity,
            copy(self.enemy_entity)
        ]

    def update(self) -> None:
        controller = self.player_entity.controller

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == KEYBOARD["left"]:
                    controller.is_moving_left = True
                if event.key == KEYBOARD["right"]:
                    controller.is_moving_right = True
                if event.key == KEYBOARD["up"]:
                    controller.is_moving_up = True
                if event.key == KEYBOARD["down"]:
                    controller.is_moving_down = True
            if event.type == pygame.KEYUP:
                if event.key == KEYBOARD["left"]:
                    controller.is_moving_left = False
                    #self.player_entity.velocity.x = 0
                if event.key == KEYBOARD["right"]:
                    controller.is_moving_right = False
                    #self.player_entity.velocity.x = 0
                if event.key == KEYBOARD["up"]:
                    controller.is_moving_up = False
                    #self.player_entity.velocity.y = 0
                if event.key == KEYBOARD["down"]:
                    controller.is_moving_down = False
                    #self.player_entity.velocity.y = 0

        self.client.screen.fill((0,0,0))

        for ps in self.player_entity.particle_systems:
            for p in ps.particles:
                self.client.screen.set_at((int(p.position.x), int(p.position.y)), p.color)

        for e in self.entities:
            if isinstance(e, EnemyEntity):
                e.move_to(self.player_entity.position, 10)
                print(e.controller.is_moving_left, e.controller.is_moving_right)

            e.update(self.client.delta_time)
            self.client.screen.blit(e.sprite, e.position.to_list())