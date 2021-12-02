"""
Helix: Flight Test (c) 2021 Andrew Hong
This code is licensed under MIT license (see LICENSE for details)
"""
import sys
from Helix.SakuyaEngine.events import WaitEvent
import pygame

from Helix.SakuyaEngine.scene import Scene

from Helix.images import pygame_powered_logo

class Splash(Scene):
    def on_awake(self) -> None:
        self.duration = 3000
        exit = WaitEvent("transition_to_start", self.duration, self.exit_func)
        self.client.event_system.add(exit)

    def update(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        self.client.screen.fill((0,0,0))
        pg_logo_rect = pygame_powered_logo.get_rect()
        pg_logo_rect.width *= 1/16
        pg_logo_rect.height *= 1/16
        pg_logo = pygame.transform.scale(pygame_powered_logo, pg_logo_rect.size)
        self.client.screen.blit(pg_logo, (
            self.client.screen.get_width() / 2 - pg_logo_rect.width / 2,
            self.client.screen.get_height() / 2 - pg_logo_rect.height / 2
        ))

    def exit_func(self) -> None:
        self.client.replace_scene("Splash", "Start")