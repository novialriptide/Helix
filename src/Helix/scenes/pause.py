"""
Helix: Flight Test (c) 2021 Andrew Hong
This code is licensed under GNU LESSER GENERAL PUBLIC LICENSE (see LICENSE for details)
"""
import sys
import pygame

from SakuyaEngine.scene import SubScene

from Helix.buttons import KEYBOARD, NS_CONTROLLER


class Pause(SubScene):
    def on_awake(self, **kwargs) -> None:
        pygame.joystick.init()
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            print(f"Console Controller Detected! [{self.joystick.get_name()}]")

        self.exit_scene = kwargs["exit_scene"]

        self.background = self.exit_scene.screen.copy()
        self.pause_bg = pygame.Surface(self.screen.get_size())
        self.pause_bg.fill((0, 0, 0))
        self.pause_bg.set_alpha(128)

    def input(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYUP:
                if event.key == KEYBOARD["start"]:
                    self.exit()

            if event.type == pygame.JOYBUTTONUP:
                if self.joystick.get_button(NS_CONTROLLER["start"]) == 0:
                    self.exit()

    def update(self) -> None:
        self.input()

        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.pause_bg, (0, 0))
