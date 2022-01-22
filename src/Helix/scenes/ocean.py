"""
Helix: Flight Test (c) 2021 Andrew Hong
This code is licensed under GNU LESSER GENERAL PUBLIC LICENSE (see LICENSE for details)
"""
from copy import copy
from distutils.spawn import spawn
from math import degrees
import sys
import pygame
import random

# just make the game have enemies come from all directions and just shoot..

from SakuyaEngine.scene import Scene, ScrollBackgroundSprite
from SakuyaEngine.effect_circle import EnlargingCircle
from SakuyaEngine.errors import SceneNotActiveError
from SakuyaEngine.lights import light, shadow
from SakuyaEngine.events import RepeatEvent
from SakuyaEngine.effect_rain import Rain
from SakuyaEngine.math import get_angle

from Helix.playercontroller import SecondaryController
from Helix.buttons import KEYBOARD, NS_CONTROLLER
from Helix.entity.berserk import BERSERK
from Helix.entity.helix import HELIX
from Helix.entity.ado import ADO
from Helix.const import *


class Ocean(Scene):
    def spawn_enemies(self, num) -> None:
        enemies = [ADO, BERSERK]
        
        win_size = pygame.Vector2(self.client.screen.get_size())
        for i in range(num):
            enemy = random.choice(enemies).copy()
            enemy.position = pygame.Vector2(random.randint(20, win_size.x - 20), random.randint(20, win_size.y - 20))
            enemy.target_position = pygame.Vector2(random.randint(20, win_size.x - 20), random.randint(20, win_size.y - 20))
            enemy.clock = self.clock
            self.entities.append(enemy)
    
    def on_awake(self) -> None:
        win_size = pygame.Vector2(self.client.screen.get_size())
        pygame.joystick.init()
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            print(f"Console Controller Detected! [{self.joystick.get_name()}]")

        self.scroll_bgs.append(
            ScrollBackgroundSprite(
                pygame.image.load("Helix/sprites/ocean_scroll_dark.png").convert(),
                pygame.Vector2(0, 6),
                infinite=True,
            )
        )


        win_size = self.client.original_window_size

        self.player_entity = HELIX
        self.player_entity.position = (
            pygame.Vector2(win_size.x / 2, win_size.y * (2 / 3))
            - self.player_entity.center_offset
        )
        self.player_entity.anim_set("idle_anim")
        self.player_entity.clock = self.clock
        self.entities.append(self.player_entity)

        self.points = 0

        screen_width, screen_height = self.screen.get_width(), self.screen.get_height()
        self.collision_rects = [
            pygame.Rect(0, 0, 4, screen_height),
            pygame.Rect(0, 0, screen_width, 4),
            pygame.Rect(screen_width - 4, 0, 4, screen_height),
            pygame.Rect(0, screen_height - 4, screen_width, 4),
        ]

        self.rain = Rain(
            1,
            self.screen,
            self.effects,
            velocity=pygame.Vector2(3, 3),
            length=8,
            color=[200, 200, 200],
        )

        HELIX.controller.is_moving_left = False
        HELIX.controller.is_moving_right = False
        HELIX.controller.is_moving_up = False
        HELIX.controller.is_moving_down = False

        self.secondary_controller = SecondaryController()

        self.font_color = (255, 255, 255)
        self.font0 = pygame.freetype.SysFont("Arial", 5)

        self.camera.shake(-1, 1)
        
        def spawn_en():
            self.spawn_enemies(4)
            return True
        
        event_spawn = RepeatEvent("spawn_enemies", spawn_en, wait_time=5000)
        spawn_en()
        self.event_system.add(event_spawn)

    def add_dialogue(self, **kwargs) -> None:
        """Adds a Dialogue scene.

        Parameters:
            msgs (List[str]): List of messages that will be said.
            char_data (dict): Character data for the person speaking.
            expression (str): The expression upon awake.

        """
        self.paused = True
        self.client.add_scene("Dialogue", exit_scene=self, **kwargs)

    def pause(self) -> None:
        self.paused = True
        self.clock.pause()

    def input(self) -> None:
        controller1 = self.player_entity.controller
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == KEYBOARD["left1"]:
                    controller1.is_moving_left = True
                if event.key == KEYBOARD["right1"]:
                    controller1.is_moving_right = True
                if event.key == KEYBOARD["up1"]:
                    controller1.is_moving_up = True
                if event.key == KEYBOARD["down1"]:
                    controller1.is_moving_down = True
                if event.key == KEYBOARD["A"]:
                    controller1.is_shooting = True
            if event.type == pygame.KEYUP:
                if event.key == KEYBOARD["left1"]:
                    controller1.is_moving_left = False
                    self.player_entity.velocity.x = 0
                if event.key == KEYBOARD["right1"]:
                    controller1.is_moving_right = False
                    self.player_entity.velocity.x = 0
                if event.key == KEYBOARD["up1"]:
                    controller1.is_moving_up = False
                    self.player_entity.velocity.y = 0
                if event.key == KEYBOARD["down1"]:
                    controller1.is_moving_down = False
                    self.player_entity.velocity.y = 0
                if event.key == KEYBOARD["start"]:
                    self.client.add_scene("Pause", exit_scene=self)
                    self.pause()
                if event.key == KEYBOARD["select"]:
                    self.client.add_scene("Components", exit_scene=self)
                    self.pause()

            if event.type == pygame.JOYBUTTONDOWN:
                if self.joystick.get_button(NS_CONTROLLER["left1"]) == 1:
                    controller1.is_moving_left = True
                if self.joystick.get_button(NS_CONTROLLER["right1"]) == 1:
                    controller1.is_moving_right = True
                if self.joystick.get_button(NS_CONTROLLER["up1"]) == 1:
                    controller1.is_moving_up = True
                if self.joystick.get_button(NS_CONTROLLER["down1"]) == 1:
                    controller1.is_moving_down = True
                if self.joystick.get_button(NS_CONTROLLER["A"]) == 1:
                    controller1.is_shooting = True

            if event.type == pygame.JOYBUTTONUP:
                if self.joystick.get_button(NS_CONTROLLER["left1"]) == 0:
                    controller1.is_moving_left = False
                    self.player_entity.velocity.x = 0
                if self.joystick.get_button(NS_CONTROLLER["right1"]) == 0:
                    controller1.is_moving_right = False
                    self.player_entity.velocity.x = 0
                if self.joystick.get_button(NS_CONTROLLER["up1"]) == 0:
                    controller1.is_moving_up = False
                    self.player_entity.velocity.y = 0
                if self.joystick.get_button(NS_CONTROLLER["down1"]) == 0:
                    controller1.is_moving_down = False
                    self.player_entity.velocity.y = 0
                if self.joystick.get_button(NS_CONTROLLER["start"]) == 0:
                    self.pause()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                controller1.is_shooting = True
                
            if event.type == pygame.MOUSEBUTTONUP:
                controller1.is_shooting = False

    def update(self) -> None:
        self.input()
        controller = self.player_entity.controller

        # Controller movement
        m = self.player_entity.controller.movement
        if m.magnitude() != 0:
            m.normalize_ip()
        self.player_entity.velocity = (
            self.player_entity.controller.movement * self.player_entity.speed
        )

        self.draw_scroll_bg()

        # Render shadows
        shadow_offset = pygame.Vector2(6, 6)
        for e in self.entities:
            shadow(
                self.screen,
                e.center_position,
                25,
                int(e.rect.width / 2 * 5 / 6),
                offset=shadow_offset + self.camera.position,
            )

        # Render effects
        self.rain.draw(self.screen, offset=self.camera.position)
        self.rain.update(self.client.delta_time)

        for ef in self.effects:
            ef.draw(self.screen, offset=self.camera.position)

        for p in self.particle_systems:
            p.render(self.screen, offset=self.camera.position)
            p.update(self.client.delta_time)

        # Player shooting
        player_angle = degrees(
            get_angle(self.player_entity.center_position, self.client.mouse_pos)
        )
        self.player_entity.angle = player_angle

        if controller.is_shooting:
            bs = self.player_entity.bullet_spawners[0]
            if bs.can_shoot:
                self.bullets.append(bs.shoot_with_firerate(player_angle))

        # Test for collisions with player
        collided = self.test_collisions_rect(self.player_entity)
        for c in collided:
            if "enemy_bullet" in c.tags:
                try:
                    self.client.replace_scene("Ocean", "Death")
                    break
                except SceneNotActiveError:
                    pass
                self.bullets.remove(c)

        for b in self.bullets:
            rect = b.rect

            # Delete bullet if out of screen's view
            if (
                b.position.y < -rect.height
                or b.position.y > self.screen.get_height()
                or b.position.x + rect.width < 0
                or b.position.x > self.screen.get_width()
            ):
                b._destroy_queue = True

            # Draw bullet + lights
            self.screen.blit(b.sprite, b.abs_position + self.camera.position)
            light(
                self.screen,
                b.center_position + self.camera.position,
                (20, 0, 20),
                10,
                brightness=3,
            )

        for e in self.entities:
            if "enemy" in e.tags:
                collided = self.test_collisions_rect(e)
                for c in collided:
                    if "player_bullet" in c.tags:
                        e.current_health -= c.damage
                        self.bullets.remove(c)

                        if e.current_health <= 0:
                            self.effects.append(
                                EnlargingCircle(
                                    e.center_position,
                                    random.choice(explosion_colors),
                                    2,
                                    500,
                                    8,
                                )
                            )
                            self.points += e.points_upon_death
                            e._destroy_queue = True

            # Render Entity Particles
            e.particle_systems[0].particles_num = int(
                ((e.max_health - e.current_health) / e.max_health) * 10
            )
            for ps in e.particle_systems:
                ps.render(self.screen, offset=self.camera.position)
            # Draw Enemy
            self.screen.blit(e.sprite, e.abs_position + self.camera.position)
            # TODO: Implement this in Entity
            if e.draw_healthbar:
                bar_length = e.rect.width * 0.7
                bar_pos = (
                    e.center_position
                    + e.healthbar_position_offset
                    - pygame.Vector2(bar_length / 2 - 1, e.rect.height * (2 / 3))
                    + self.camera.position
                )

                display_hp = int(
                    (e.healthbar.display_health / e.max_health) * bar_length
                )
                if display_hp % 2 == 1:
                    bar_pos.x -= 1
                    display_hp += 1
                pygame.draw.rect(
                    self.screen,
                    (0, 230, 0),
                    pygame.Rect(bar_pos.x, bar_pos.y, display_hp, 1),
                )
                pygame.draw.rect(
                    self.screen,
                    (0, 190, 0),
                    pygame.Rect(bar_pos.x, bar_pos.y + 1, display_hp, 1),
                )

        self.screen.blit(vignette_overlay, (0, 0))
        rand_pos = random.randint(-int(random_noise_size[0] / 3), 0), random.randint(
            -int(random_noise_size[1] / 3), 0
        )

        self.screen.blit(random_noise, (rand_pos))

        self.event_system.update()
        self.advance_frame(self.client.delta_time, collision_rects=self.collision_rects)
