import sys
import pygame
import math

from copy import copy

from Helix.SakuyaEngine.entity import Entity
from Helix.SakuyaEngine.animation import Animation
from Helix.SakuyaEngine.scene import Scene
from Helix.SakuyaEngine.math import Vector
from Helix.SakuyaEngine.particles import Particles
from Helix.SakuyaEngine.waves import load_wave_file

from Helix.wavemanager import HelixWaves
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

        self.wave_manager = HelixWaves(30000)
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
            fps = 0.05
        )

        self.projectile_entity = Entity(
            None,
            Vector(0, 0),
            custom_hitbox_size= Vector(3, 3)
        )
        self.projectile_entity.anim_add(copy(projectile_anim))
        self.projectile_entity.anim_set("projectile_anim")

        enemy_idle_anim = Animation(
            "enemy_idle_anim",
            enemy_sprites,
            fps = 1.5
        )

        self.enemy_entity = EnemyEntity(
            Vector(0, 0),
            has_rigidbody = True,
            fire_rate = 500,
            custom_hitbox_size = Vector(11, 11)
        )
        self.enemy_entity.anim_add(copy(enemy_idle_anim))
        self.enemy_entity.anim_set("enemy_idle_anim")

        player_idle_anim = Animation(
            "player_idle_anim", 
            player_sprites,
            fps = 2
        )

        self.player_entity = Entity(
            PlayerController,
            Vector(win_size.x/2, win_size.y/2),
            has_rigidbody = True,
            custom_hitbox_size = Vector(3, 3),
            obey_gravity = False
        )
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
                spread = 1,
                lifetime = 500
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
                    self.player_entity.velocity.x = 0
                if event.key == KEYBOARD["right"]:
                    controller.is_moving_right = False
                    self.player_entity.velocity.x = 0
                if event.key == KEYBOARD["up"]:
                    controller.is_moving_up = False
                    self.player_entity.velocity.y = 0
                if event.key == KEYBOARD["down"]:
                    controller.is_moving_down = False
                    self.player_entity.velocity.y = 0

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
                    self.player_entity.velocity.x = 0
                if self.joystick.get_button(NS_CONTROLLER["right"]) == 0:
                    controller.is_moving_right = False
                    self.player_entity.velocity.x = 0
                if self.joystick.get_button(NS_CONTROLLER["up"]) == 0:
                    controller.is_moving_up = False
                    self.player_entity.velocity.y = 0
                if self.joystick.get_button(NS_CONTROLLER["down"]) == 0:
                    controller.is_moving_down = False
                    self.player_entity.velocity.y = 0

        self.client.screen.fill((0,0,0))

        particles_rendered = 0

        for ps in self.player_entity.particle_systems:
            for p in ps.particles:
                self.client.screen.set_at((int(p.position.x), int(p.position.y)), p.color)
                particles_rendered += 1

        for e in self.entities:
            if isinstance(e, EnemyEntity):
                player_rect = self.player_entity.rect
                offset = Vector(e.rect.width/2, e.rect.height/2)
                delta_pos = (self.player_entity.position + Vector(player_rect.width/2, player_rect.height/2)) - (e.position + offset)
                angle = math.atan2(delta_pos.y, delta_pos.x)
                proj = e.shoot(offset, self.projectile_entity.copy(), angle, 2)
                if proj is not None:
                    proj.on_destroy(5000)
                    self.entities.append(proj)

            self.client.screen.blit(e.sprite, e.position.to_list())

            # draw hitboxes
            pygame.draw.rect(self.client.screen, (0, 255, 0), e.custom_hitbox, 1)

        for sp in self.wave_manager.spawn_points:
            self.client.screen.set_at(sp.to_list(), (255,255,255))

        if self.test_collisions(self.player_entity):
            self.client.replace_scene("Start", "Death")
        
        self.event_system.update(self.client.delta_time)
        self.advance_frame(self.client.delta_time)

        print(f"objects:{len(self.entities)} particles:{particles_rendered} fps:{int(self.client.current_fps)}")