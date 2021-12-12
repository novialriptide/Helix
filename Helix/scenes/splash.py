"""
Helix: Flight Test (c) 2021 Andrew Hong
This code is licensed under MIT license (see LICENSE for details)
"""
import sys
from Helix.SakuyaEngine.events import WaitEvent
import pygame

from Helix.SakuyaEngine.scene import Scene

from Helix.const import pygame_powered_logo, flg_logo2

class Splash(Scene):
    def on_awake(self) -> None:
        pygame.mixer.init()
        pygame.joystick.init()
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            print(f"Console Controller Detected! [{self.joystick.get_name()}]")

        self.duration = 3000
        exit = WaitEvent("transition_to_start", self.duration, self.exit_func)
        self.client.event_system.add(exit)
        self.startup_beep = pygame.mixer.Sound("Helix\\audio\\menu-chime-1.mp3")
        pygame.mixer.Sound.play(self.startup_beep)

    def update(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        self.client.screen.fill((0, 0, 0))
        flg_logo_rect = flg_logo2.get_rect()
        self.client.screen.blit(flg_logo2, (
            self.client.screen.get_width() / 2 - flg_logo_rect.width / 2,
            self.client.screen.get_height() * (1 / 2) - flg_logo_rect.height / 2,
        ))

        pg_logo_rect = pygame_powered_logo.get_rect()
        pg_logo_rect.width *= 1/32
        pg_logo_rect.height *= 1/32
        _pg_logo = pygame.transform.scale(pygame_powered_logo, pg_logo_rect.size)
        self.client.screen.blit(_pg_logo, (
            self.client.screen.get_width() / 2 - pg_logo_rect.width / 2,
            self.client.screen.get_height() * (3.8 / 6) - pg_logo_rect.height / 2
        ))

    def exit_func(self) -> None:
        self.client.replace_scene("Splash", "Start")