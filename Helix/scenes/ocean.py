"""
Helix: Flight Test (c) 2021 Andrew Hong
This code is licensed under MIT license (see LICENSE for details)
"""
import sys
import pygame

from Helix.SakuyaEngine.scene import Scene, ScrollBackgroundSprite
from Helix.SakuyaEngine.waves import load_wave_file
from Helix.SakuyaEngine.errors import SceneNotActiveError
from Helix.SakuyaEngine.lights import spotlight
from Helix.SakuyaEngine.effects import EnlargingCircle

from Helix.wavemanager import HelixWaves
from Helix.buttons import KEYBOARD, NS_CONTROLLER
from Helix.playercontroller import PlayerController
from Helix.const import *

from Helix.data.entity.helix import HELIX
from Helix.data.entity.ado import ADO
from Helix.data.entity.berserk import BERSERK

class Ocean(Scene):
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

        self.scroll_bgs.append(
            ScrollBackgroundSprite(
                pygame.image.load("Helix\\sprites\\ocean_scroll.png").convert(),
                pygame.Vector2(0, 2), infinite = True
            )
        )

        self.wave_manager = HelixWaves(30000)
        self.wave_manager.spawn_points = [
            pygame.Vector2(int(win_size.x * 1/10), int(win_size.y * 1/7)),
            pygame.Vector2(int(win_size.x * 3/10), int(win_size.y * 1/7)),
            pygame.Vector2(int(win_size.x * 5/10), int(win_size.y * 1/7)),
            pygame.Vector2(int(win_size.x * 7/10), int(win_size.y * 1/7)),
            pygame.Vector2(int(win_size.x * 9/10), int(win_size.y * 1/7)),
            pygame.Vector2(int(win_size.x * 1/10), int(win_size.y * 2.5/7)),
            pygame.Vector2(int(win_size.x * 3/10), int(win_size.y * 2.5/7)),
            pygame.Vector2(int(win_size.x * 5/10), int(win_size.y * 2.5/7)),
            pygame.Vector2(int(win_size.x * 7/10), int(win_size.y * 2.5/7)),
            pygame.Vector2(int(win_size.x * 9/10), int(win_size.y * 2.5/7)),
        ]
        self.wave_manager.despawn_points = [
            pygame.Vector2(int(win_size.x * 1/10), int(win_size.y)),
            pygame.Vector2(int(win_size.x * 3/10), int(win_size.y)),
            pygame.Vector2(int(win_size.x * 5/10), int(win_size.y)),
            pygame.Vector2(int(win_size.x * 7/10), int(win_size.y)),
            pygame.Vector2(int(win_size.x * 9/10), int(win_size.y)),
            pygame.Vector2(int(win_size.x * 1/10), int(win_size.y)),
            pygame.Vector2(int(win_size.x * 3/10), int(win_size.y)),
            pygame.Vector2(int(win_size.x * 5/10), int(win_size.y)),
            pygame.Vector2(int(win_size.x * 7/10), int(win_size.y)),
            pygame.Vector2(int(win_size.x * 9/10), int(win_size.y)),
        ]
        
        self.player_entity = HELIX
        self.player_entity.position = pygame.Vector2(win_size.x/2, win_size.y * (2 / 3)) - self.player_entity.center_offset
        self.player_entity.controller = PlayerController()
        self.player_entity.anim_set("idle_anim")

        self.entities.append(self.player_entity)

        self.wave_manager.entities = [
            ADO, BERSERK
        ]

        screen_width, screen_height = self.client.screen.get_width(), self.client.screen.get_height()
        self.collision_rects = [
            pygame.Rect(0, 0, 4, screen_height),
            pygame.Rect(0, 0, screen_width, 4),
            pygame.Rect(screen_width - 4, 0, 4, screen_height),
            pygame.Rect(0, screen_height - 4, screen_width, 4)
        ]

        load_wave_file("Helix\waves\w1.wave", self.wave_manager, self)

    def add_dialogue(self, **kwargs) -> None:
        """Adds a Dialogue scene.

        Parameters:
            msgs (List[str]): List of messages that will be said.
            char_data (dict): Character data for the person speaking.
            expression (str): The expression upon awake.

        """
        self.paused = True
        self.client.add_scene("Dialogue", exit_scene = self, **kwargs)

    def pause(self) -> None:
        self.paused = True
        self.client.add_scene("Pause", exit_scene = self)

    def input(self) -> None:
        controller = self.player_entity.controller
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.add_dialogue(
                        msgs = ["Bro, what the fuck are you doing?"],
                        char_data = "Helix\\data\\characters\\eunji.json",
                        expression = "unsure"
                    )
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
                if event.key == KEYBOARD["start"]:
                    self.pause()

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
                if self.joystick.get_button(NS_CONTROLLER["start"]) == 0:
                    self.pause()

    def update(self) -> None:
        self.input()
        controller = self.player_entity.controller

        self.draw_scroll_bg()

        # Player shooting
        if controller.is_shooting:
            bs = self.player_entity.bullet_spawners[0]
            if bs.can_shoot:
                self.bullets.append(bs.shoot_with_firerate(-90))
                pygame.mixer.Sound.play(self.laser_1)

        # Test for collisions with player
        collided = self.test_collisions_rect(self.player_entity)
        for c in collided:
            if "enemy_bullet" in c.tags:
                try:
                    self.client.replace_scene("Ocean", "Death")
                except SceneNotActiveError:
                    pass
                self.bullets.remove(c)

        for b in self.bullets:
            rect = b.rect

            # Delete bullet if out of screen's view
            if b.position.y < - rect.height or b.position.y > self.client.screen.get_height() or b.position.x + rect.width < 0 or b.position.x > self.client.screen.get_width():
                b._destroy_queue = True
                
            # Draw bullet + lights
            self.client.screen.blit(b.sprite, b.position + self.camera.position)
            spotlight(self.client.screen, b.position + b.center_offset + self.camera.position, (20, 0, 20), 10)
            #pygame.draw.rect(self.client.screen, (0, 255, 0), b.custom_hitbox, 1)

        for e in self.entities:
            if "enemy" in e.tags:
                collided = self.test_collisions_rect(e)
                for c in collided:
                    if "player_bullet" in c.tags:
                        e.current_health -= c.damage
                        self.bullets.remove(c)

                        if e.current_health <= 0:
                            self.effects.append(
                                EnlargingCircle(e.position + e.center_offset, (255, 255, 255), 2, 500, 8)
                            )
                            e._destroy_queue = True

            # Render Player Particles
            e.particle_systems[0].particles_num = int(
                ((e.max_health - e.current_health) / e.max_health) * 10
            )
            for ps in e.particle_systems:
                ps.render(self.client.screen, offset = self.camera.position)
            # Draw
            self.client.screen.blit(e.sprite, e.position + self.camera.position)
            # TODO: Implement this in Entity
            if e.draw_healthbar:
                bar_length = e.rect.width * 0.7
                bar_pos = e.position + e.healthbar_position_offset + e.center_offset - pygame.Vector2(bar_length / 2 - 1, e.rect.height * (2 / 3)) + self.camera.position
                display_hp = (e.healthbar.display_health / e.max_health) * bar_length
                pygame.draw.rect(self.client.screen, (0, 230, 0), pygame.Rect(
                    bar_pos.x, bar_pos.y, display_hp, 1
                ))
                pygame.draw.rect(self.client.screen, (0, 190, 0), pygame.Rect(
                    bar_pos.x, bar_pos.y + 1, display_hp, 1
                ))
        
        # Render effects
        for ef in self.effects:
            ef.draw(self.client.screen, offset = self.camera.position)

        # for sp in self.wave_manager.spawn_points: self.client.screen.set_at((int(sp.x), int(sp.y)), (255,255,255))
        # for e in self.entities: pygame.draw.rect(self.client.screen, (0, 255, 0), e.custom_hitbox, 1)
        # for e in self.bullets: pygame.draw.rect(self.client.screen, (0, 255, 0), e.custom_hitbox, 1)

        for p in self.particle_systems:
            p.render(self.client.screen, offset = self.camera.position)
            p.update(self.client.delta_time)

        self.event_system.update()
        self.advance_frame(self.client.delta_time, collision_rects = self.collision_rects)

        pygame.display.set_caption(f"{self.client._window_name} (fps: {int(self.client.pg_clock.get_fps())}, bullets: {int(len(self.bullets))}, entities: {len(self.entities)})")