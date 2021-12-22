"""
Helix: Flight Test (c) 2021 Andrew Hong
This code is licensed under MIT license (see LICENSE for details)
"""
import sys
import pygame

from Helix.SakuyaEngine.events import WaitEvent
from Helix.SakuyaEngine.scene import Scene

from Helix.const import pygame_powered_logo

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
            if event.type == pygame.KEYDOWN:
                self.exit_func()
            if event.type == pygame.JOYBUTTONDOWN:
                self.exit_func()
                
        self.client.screen.fill((15, 15, 15))
                
        pg_logo_rect = pygame_powered_logo.get_rect()
        self.client.screen.blit(pygame_powered_logo, (
            self.client.screen.get_width() / 2 - pg_logo_rect.width / 2,
            self.client.screen.get_height() / 2 - pg_logo_rect.height / 2
        ))

    def exit_func(self) -> None:
        self.client.replace_scene("Splash", "MainMenu")