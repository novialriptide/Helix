"""
Helix: Flight Test (c) 2021 Andrew Hong
This code is licensed under GNU LESSER GENERAL PUBLIC LICENSE (see LICENSE for details)
"""
import sys
import pygame

from SakuyaEngine.events import WaitEvent
from SakuyaEngine.scene import Scene

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
        self.event_system._methods.append(exit)
        self.startup_beep = pygame.mixer.Sound("Helix/audio/menu-chime-1.mp3")
        pygame.mixer.Sound.play(self.startup_beep)

    def update(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                self.exit_func()
            if event.type == pygame.JOYBUTTONDOWN:
                self.exit_func()
                
        self.screen.fill((15, 15, 15))
                
        pg_logo_rect = pygame_powered_logo.get_rect()
        self.screen.blit(pygame_powered_logo, (
            self.screen.get_width() / 2 - pg_logo_rect.width / 2,
            self.screen.get_height() / 2 - pg_logo_rect.height / 2
        ))
        
        self.event_system.update()

    def exit_func(self) -> None:
        self.client.replace_scene("Splash", "MainMenu")