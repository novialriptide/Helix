"""
Helix: Flight Test (c) 2021 Andrew Hong
This code is licensed under GNU LESSER GENERAL PUBLIC LICENSE (see LICENSE for details)
"""
from copy import copy
import sys
import pygame
import random

from SakuyaEngine.scene import Scene, ScrollBackgroundSprite
from SakuyaEngine.waves import WaveManager, load_stage_json
from SakuyaEngine.effect_circle import EnlargingCircle
from SakuyaEngine.errors import SceneNotActiveError
from SakuyaEngine.lights import light, shadow
from SakuyaEngine.effect_rain import Rain

from Helix.playercontroller import SecondaryController
from Helix.abilties.target_fire import TargetFire
from Helix.buttons import KEYBOARD, NS_CONTROLLER
from Helix.entity.berserk import BERSERK
from Helix.entity.helix import HELIX
from Helix.entity.ado import ADO
from Helix.const import *


class Ocean(Scene):
    def on_awake(self) -> None:
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
        self.wave_manager = WaveManager()

        self.player_entity = copy(HELIX)
        self.player_entity.position = (
            pygame.Vector2(win_size.x / 2, win_size.y * (2 / 3))
            - self.player_entity.center_offset
        )
        self.player_entity.anim_set("idle_anim")
        self.player_entity.clock = self.clock
        self.entities.append(self.player_entity)

        self.points = 0

        self.wave_manager.entities = [ADO, BERSERK]

        for e in self.wave_manager.entities:
            e.clock = self.clock

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

        load_stage_json("Helix/stages/startup.json", self.wave_manager, self)

        HELIX.controller.is_moving_left = False
        HELIX.controller.is_moving_right = False
        HELIX.controller.is_moving_up = False
        HELIX.controller.is_moving_down = False

        self.secondary_controller = SecondaryController()

        self.font_color = (255, 255, 255)
        self.font0 = pygame.freetype.SysFont("Arial", 5)

        self.camera.shake(-1, 1)

        self.target_ability = TargetFire(0, self, self.secondary_controller)
        self.target_ability.start(HELIX.center_position)

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
        controller2 = self.secondary_controller
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
                if event.key == KEYBOARD["up2"]:
                    controller2.is_moving_up = True
                if event.key == KEYBOARD["down2"]:
                    controller2.is_moving_down = True
                if event.key == KEYBOARD["left2"]:
                    controller2.is_moving_left = True
                if event.key == KEYBOARD["right2"]:
                    controller2.is_moving_right = True
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
                if event.key == KEYBOARD["up2"]:
                    controller2.is_moving_up = False
                if event.key == KEYBOARD["down2"]:
                    controller2.is_moving_down = False
                if event.key == KEYBOARD["left2"]:
                    controller2.is_moving_left = False
                if event.key == KEYBOARD["right2"]:
                    controller2.is_moving_right = False
                if event.key == KEYBOARD["A"]:
                    controller1.is_shooting = False
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
                if self.joystick.get_button(NS_CONTROLLER["A"]) == 0:
                    controller1.is_shooting = False
                if self.joystick.get_button(NS_CONTROLLER["start"]) == 0:
                    self.pause()

    def update(self) -> None:
        self.input()
        controller = self.player_entity.controller

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
        if controller.is_shooting:
            bs = self.player_entity.bullet_spawners[0]
            if bs.can_shoot:
                self.bullets.append(bs.shoot_with_firerate(-90))

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
            self.screen.blit(b.sprite, b.position + self.camera.position)
            light(
                self.screen,
                b.center_position + self.camera.position,
                (20, 0, 20),
                10,
                brightness=3,
            )
            # pygame.draw.rect(self.screen, (0, 255, 0), b.custom_hitbox, 1)

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
            self.screen.blit(e.sprite, e.position + self.camera.position)
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

        self.target_ability.draw(offset=self.camera.position)

        self.screen.blit(random_noise, (rand_pos))

        # for e in self.entities: pygame.draw.rect(self.screen, (0, 255, 0), e.custom_hitbox, 1)
        # for e in self.bullets: pygame.draw.rect(self.screen, (0, 255, 0), e.custom_hitbox, 1)

        # self.screen.blit(self.font0.render(f"points: {self.points}", fgcolor = self.font_color, size = 25)[0], (0, 0))
        self.target_ability.update(self.client.delta_time)

        self.wave_manager.update()
        self.event_system.update()
        self.advance_frame(self.client.delta_time, collision_rects=self.collision_rects)
