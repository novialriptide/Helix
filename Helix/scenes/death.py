"""
Helix: Flight Test (c) 2021 Andrew Hong
This code is licensed under MIT license (see LICENSE for details)
"""
import sys
import pygame

from Helix.SakuyaEngine.scene import Scene
from Helix.SakuyaEngine.text import text

class Death(Scene):
    def __init__(self, client):
        super().__init__(client)

    def on_awake(self) -> None:
        pygame.joystick.init()
        try:
            self.joystick = pygame.joystick.Joystick(0)
            print(f"Console Controller Detected! [{self.joystick.get_name()}]")
        except:
            self.joystick = None

    def update(self) -> None:
        win_size = self.client.original_window_size
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        self.client.screen.fill((0,0,0))
        game_over_text = text("gae owr", 25, "Arial", (255, 255, 255))
        self.client.screen.blit(game_over_text, (win_size.x/2, win_size.y/2))