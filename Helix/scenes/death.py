"""
Helix: Flight Test (c) 2021 Andrew Hong
This code is licensed under GNU LESSER GENERAL PUBLIC LICENSE (see LICENSE for details)
"""
import sys
import pygame

from SakuyaEngine.scene import Scene
from SakuyaEngine.text import text2
from SakuyaEngine.button import Button

from Helix.const import *
from Helix.buttons import KEYBOARD

class Death(Scene):
    def __init__(self, client):
        super().__init__(client)

    def retry(self) -> None:
        # add reset scene here
        self.client.add_scene("Ocean")
        self.client.remove_scene(self.name)

    def on_awake(self) -> None:
        pygame.joystick.init()
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            
        win_size = self.client.original_window_size
        self.try_again_button = Button(
            pygame.Rect(win_size.x / 2 - 32, win_size.y * (3 / 5) - 8, 64, 16),
            [{"func": self.retry, "args": [], "kwargs": {}}], key = KEYBOARD["A"]
        )
        self.try_again_button.sprite = try_again_button

    def update(self) -> None:
        win_size = self.client.original_window_size
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        self.screen.fill((0, 0, 0))
        
        b = self.try_again_button
        self.screen.blit(b.sprite, (b.rect.x, b.rect.y))
        if b.is_pressing_mouseup_instant(self.client.mouse_position):
            b.execute()