import sys
import pygame

from copy import copy

from Helix.Sakuya.waves import WaveManager, load_wave_file
from Helix.Sakuya.entity import Entity
from Helix.Sakuya.animation import Animation
from Helix.Sakuya.scene import Scene
from Helix.Sakuya.math import Vector
from Helix.Sakuya.particles import Particles

from Helix.buttons import KEYBOARD, NS_CONTROLLER
from Helix.playercontroller import PlayerController
from Helix.enemy import EnemyEntity, EnemyController
from Helix.images import player_sprites, enemy_sprites, projectile_sprites

class Start(Scene):
    def __init__(self, client):
        super().__init__(client)

    def on_awake(self) -> None:
        win_size = self.client.original_window_size
        pygame.joystick.init()
        try:
            self.joystick = pygame.joystick.Joystick(0)
            print(f"Console Controller Detected! [{self.joystick.get_name()}]")
        except:
            self.joystick = None

        self.wave_manager = WaveManager(30000)
        self.wave_manager.spawn_points = [
            Vector(int(win_size.x * 1/5), int(win_size.y * 1/4)),
            Vector(int(win_size.x * 1/3), int(win_size.y * 1/7)),
            Vector(int(win_size.x * 1/2), int(win_size.y * 1/7)),
            Vector(int(win_size.x * 2/3), int(win_size.y * 1/7)),
            Vector(int(win_size.x * 4/5), int(win_size.y * 1/4))
        ]

        projectile_anim = Animation(
            "projectile_anim",
            projectile_sprites,
            fps = 2
        )

        self.projectile_entity = Entity(None, Vector(0, 0))
        self.projectile_entity.anim_add(projectile_anim)
        self.projectile_entity.anim_set("projectile_anim")


        enemy_idle_anim = Animation(
            "enemy_idle_anim",
            enemy_sprites,
            fps = 1.5
        )

        self.enemy_entity = EnemyEntity(EnemyController, Vector(0, 0), has_rigidbody = True)
        self.enemy_entity.anim_add(copy(enemy_idle_anim))
        self.enemy_entity.anim_set("enemy_idle_anim")

        player_idle_anim = Animation(
            "player_idle_anim", 
            player_sprites,
            fps = 2
        )

        self.player_entity = Entity(PlayerController, Vector(win_size.x/2, win_size.y/2), has_rigidbody = True)
        self.player_entity.anim_add(player_idle_anim)
        self.player_entity.anim_set("player_idle_anim")
        player_rect = self.player_entity.rect
        self.player_entity.particle_systems = [
            Particles(
                Vector(0, 5),
                colors = [
                    (249, 199, 63),
                    (255, 224, 70),
                    (255, 78, 65)
                ],
                offset = Vector(player_rect.width/2, player_rect.height * 2/3),
                particles_num = 10,
                spread = 1
            )
        ]
        self.entities = [
            self.player_entity
        ]
        self.wave_manager.entities = [
            self.enemy_entity
        ]

        self.wave = load_wave_file("Helix\waves\w1.wave", self.wave_manager, self)

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

            if event.type == pygame.JOYBUTTONDOWN:
                if self.joystick.get_button(NS_CONTROLLER["left"]) == 1:
                    controller.is_moving_left = True
                if self.joystick.get_button(NS_CONTROLLER["right"]) == 1:
                    controller.is_moving_right = True
                if self.joystick.get_button(NS_CONTROLLER["up"]) == 1:
                    controller.is_moving_up = True
                if self.joystick.get_button(NS_CONTROLLER["down"]) == 1:
                    controller.is_moving_down = True

            if event.type == pygame.JOYBUTTONUP:
                if self.joystick.get_button(NS_CONTROLLER["left"]) == 0:
                    controller.is_moving_left = False
                if self.joystick.get_button(NS_CONTROLLER["right"]) == 0:
                    controller.is_moving_right = False
                if self.joystick.get_button(NS_CONTROLLER["up"]) == 0:
                    controller.is_moving_up = False
                if self.joystick.get_button(NS_CONTROLLER["down"]) == 0:
                    controller.is_moving_down = False
                

        self.client.screen.fill((0,0,0))

        for ps in self.player_entity.particle_systems:
            for p in ps.particles:
                self.client.screen.set_at((int(p.position.x), int(p.position.y)), p.color)

        for e in self.entities:
            if isinstance(e, EnemyEntity):
                e.shoot(Vector(0, 0), self.projectile_entity, 0, 0.7)

            e.update(self.client.delta_time)
            self.client.screen.blit(e.sprite, e.position.to_list())

        for sp in self.wave_manager.spawn_points:
            self.client.screen.set_at(sp.to_list(), (255,255,255))