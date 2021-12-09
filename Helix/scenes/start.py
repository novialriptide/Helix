"""
Helix: Flight Test (c) 2021 Andrew Hong
This code is licensed under MIT license (see LICENSE for details)
"""
import sys
import pygame
import math

from Helix.SakuyaEngine.entity import load_entity_json
from Helix.SakuyaEngine.scene import Scene
from Helix.SakuyaEngine.math import Vector
from Helix.SakuyaEngine.particles import Particles
from Helix.SakuyaEngine.waves import load_wave_file
from Helix.SakuyaEngine.errors import EntityNotInScene, SceneNotActiveError
from Helix.SakuyaEngine.bullets import BulletSpawner, Bullet
from Helix.SakuyaEngine.text import text

from Helix.wavemanager import HelixWaves
from Helix.buttons import KEYBOARD, NS_CONTROLLER
from Helix.playercontroller import PlayerController

class Start(Scene):
    def on_awake(self) -> None:
        win_size = self.client.original_window_size
        pygame.joystick.init()
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            print(f"Console Controller Detected! [{self.joystick.get_name()}]")
        
        # Load sounds
        pygame.mixer.init()
        pygame.mixer.set_num_channels(64)
        self.laser_1 = pygame.mixer.Sound("Helix\\audio\\laser-1.mp3")

        self.wave_manager = HelixWaves(30000)
        self.wave_manager.spawn_points = [
            Vector(int(win_size.x * 1/5), int(win_size.y * 1/4)),
            Vector(int(win_size.x * 1/3), int(win_size.y * 1/7)),
            Vector(int(win_size.x * 1/2), int(win_size.y * 1/7)),
            Vector(int(win_size.x * 2/3), int(win_size.y * 1/7)),
            Vector(int(win_size.x * 4/5), int(win_size.y * 1/4))
        ]

        self.particle_systems = [
            Particles(
                Vector(-0.5, -0.5),
                colors = [
                    (255, 255, 255),
                    (100, 100, 100)
                ],
                particles_num = 10,
                spread = 5,
                lifetime = 1000,
                position = Vector(win_size.x, -10)
            )
        ]

        self.player_entity = load_entity_json("Helix\\data\\entity\\helix.json")
        self.player_entity.position = Vector(win_size.x/2, win_size.y/2)
        self.player_entity.controller = PlayerController()
        self.player_entity.anim_set("idle_anim")
        player_rect = self.player_entity.rect
        self.player_entity.particle_systems = [
            Particles(
                Vector(0, 5),
                colors = [
                    (249, 199, 63),
                    (255, 224, 70),
                    (255, 78, 65)
                ],
                offset = Vector(
                    player_rect.width/2,
                    player_rect.height * 1/4
                ),
                particles_num = 10,
                spread = 1,
                lifetime = 1000
            )
        ]

        self.entities = [
            self.player_entity
        ]
        self.enemies = []

        player_bullet1 = Bullet(
            speed = 4,
            color = (255, 255, 0),
            damage = 7,
            custom_hitbox_size = Vector(1, 1)
        )
        offset = Vector(
            self.player_entity.rect.width/2, 
            self.player_entity.rect.height/2
        )
        player_bs1 = BulletSpawner(
            player_bullet1,
            starting_angle = -90, fire_rate = 100, 
            bullet_speed = 7
        )
        self.player_entity.bullet_spawners.append(player_bs1)

        self.wave_manager.entities = [
            load_entity_json("Helix\\data\\entity\\ado.json")
        ]

        load_wave_file("Helix\waves\w1.wave", self.wave_manager, self)

    def input(self) -> None:
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
                if event.key == KEYBOARD["A"]:
                    controller.is_shooting = True
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
                if event.key == KEYBOARD["A"]:
                    controller.is_shooting = False

            if event.type == pygame.JOYBUTTONDOWN:
                if self.joystick.get_button(NS_CONTROLLER["left"]) == 1:
                    controller.is_moving_left = True
                if self.joystick.get_button(NS_CONTROLLER["right"]) == 1:
                    controller.is_moving_right = True
                if self.joystick.get_button(NS_CONTROLLER["up"]) == 1:
                    controller.is_moving_up = True
                if self.joystick.get_button(NS_CONTROLLER["down"]) == 1:
                    controller.is_moving_down = True
                if self.joystick.get_button(NS_CONTROLLER["A"]) == 1:
                    controller.is_shooting = True

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
                if self.joystick.get_button(NS_CONTROLLER["A"]) == 0:
                    controller.is_shooting = False

    def update(self) -> None:
        self.input()
        controller = self.player_entity.controller

        self.client.screen.fill((0, 0, 0))

        particles_rendered = 0
        # Player shooting
        if controller.is_shooting:
            bs = self.player_entity.bullet_spawners[0]
            if bs.can_shoot:
                self.bullets.append(bs.shoot_with_firerate(-90))
                pygame.mixer.Sound.play(self.laser_1)
        for ps in self.player_entity.particle_systems:
            for p in ps.particles:
                self.client.screen.set_at((int(p.position.x), int(p.position.y)), p.color)
                particles_rendered += 1

        # Test for collisions
        try:
            collided = self.test_collisions(self.player_entity)
            for c in collided:
                if c.name == "enemy_projectiles":
                    try:
                        self.client.replace_scene("Start", "Death")
                    except SceneNotActiveError:
                        pass
                    self.entities.remove(c)
            
            for e in self.enemies:
                collided = self.test_collisions(e)
                for c in collided:
                    if c.name == "player_projectiles":
                        self.entities.remove(c)
        except EntityNotInScene:
            pass

        for e in self.entities:
            if e.sprite is not None:
                self.client.screen.blit(e.sprite, e.position.to_list())
            if e.name == "enemy":
                player_rect = self.player_entity.rect
                offset = Vector(e.rect.width/2, e.rect.height/2)
                delta_pos = (self.player_entity.position + Vector(player_rect.width/2, player_rect.height/2)) - (e.position + offset)
                angle = math.atan2(delta_pos.y, delta_pos.x)
                proj = e.shoot(offset, self.projectile_entity1.copy(), angle, 2)
                if proj is not None:
                    proj.destroy(3000)
                    self.entities.insert(0, proj)

        # for sp in self.wave_manager.spawn_points: self.client.screen.set_at(sp.to_list(), (255,255,255))

        # for e in self.entities: pygame.draw.rect(self.client.screen, (0, 255, 0), e.custom_hitbox, 1)

        for b in self.bullets: pygame.draw.rect(self.client.screen, (0, 255, 0), b.custom_hitbox, 1)
        
        for p in self.particle_systems:
            p.render(self.client.screen)
            p.update(self.client.delta_time)

        self.event_system.update(self.client.delta_time)
        self.advance_frame(self.client.delta_time)

        fps = text(f"fps: {int(self.client.pg_clock.get_fps())}", 10, "Arial", (0, 255, 0))
        object_count = text(f"object count: {len(self.entities)}", 10, "Arial", (0, 255, 0))
        self.client.screen.blit(fps, (0, 0))
        self.client.screen.blit(object_count, (0, 10))

        #print(f"objects:{len(self.entities)} particles:{particles_rendered} fps:{int(self.client.current_fps)}")
        #print(f"events:{len(self.event_system._methods)}")
    
    def advance_frame(self, delta_time: float):
        for entity in self.entities[:]:
            entity.update(delta_time)
            if entity._is_destroyed:
                self.entities.remove(entity)
                if entity in self.enemies:
                    self.enemies.remove(entity)

            # Update Bullet Spawners
            # TODO: Move this in the Entity.update()
            for bs in entity.bullet_spawners:
                bs.position = entity.position + entity.center_position
                if entity.update_bullet_spawners:
                    self.bullets.extend(bs.update(delta_time))

        for bullet in self.bullets[:]:
            bullet.update(delta_time)
            if bullet._is_destroyed:
                self.bullets.remove(bullet)
                