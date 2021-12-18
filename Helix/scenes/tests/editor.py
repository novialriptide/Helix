"""
Helix: Flight Test (c) 2021 Andrew Hong
This code is licensed under MIT license (see LICENSE for details)
"""
import sys
import pygame

from Helix.SakuyaEngine.scene import Scene

class Editor(Scene):
    def on_awake(self) -> None:
        pygame.joystick.init()
        try:
            self.joystick = pygame.joystick.Joystick(0)
            print(f"Console Controller Detected! [{self.joystick.get_name()}]")
        except:
            self.joystick = None

    def update(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        
        self.client.screen.fill((0,0,0))
        