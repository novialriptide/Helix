"""
Helix: Flight Test (c) 2021 Andrew Hong
This code is licensed under MIT license (see LICENSE for details)
"""
import sys
import pygame

from Helix.SakuyaEngine.scene import Scene

from Helix.buttons import KEYBOARD, NS_CONTROLLER

class Pause(Scene):
    def on_awake(self, **kwargs) -> None:
        pygame.joystick.init()
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            print(f"Console Controller Detected! [{self.joystick.get_name()}]")
        
        self.exit_scene = kwargs["scene"]

    def exit(self) -> None:
        self.exit_scene.paused = False
        self.client.remove_scene(self.name)

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