"""
Helix: Flight Test (c) 2021 Andrew Hong
This code is licensed under GNU LESSER GENERAL PUBLIC LICENSE (see LICENSE for details)
"""
import sys
import pygame

from SakuyaEngine.scene import Scene
from SakuyaEngine.text import text2
from SakuyaEngine.button import Button

from Helix.buttons import KEYBOARD, NS_CONTROLLER
from Helix.const import *


class MainMenu(Scene):
    def __init__(self, client):
        super().__init__(client)

    def play_endless(self) -> None:
        self.client.add_scene("Ocean")
        self.client.remove_scene(self.name)

    def on_awake(self) -> None:
        pygame.joystick.init()
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)

        win_size = self.client.original_window_size
        self.start_button = Button(
            pygame.Rect(win_size.x / 2 - 32, win_size.y * (3 / 5) - 8, 64, 16),
            [{"func": self.play_endless, "args": [], "kwargs": {}}],
        )
        self.start_button.sprite = start_button

        self.selected_button = pygame.Vector2(0, 0)
        self.button_layout = [
            [self.start_button],
        ]

    def move_selection(self, movement: pygame.Vector2) -> None:
        columns = len(self.button_layout[int(self.selected_button.y)])
        rows = len(self.button_layout)

        test_vector = movement + self.selected_button

        if 0 < test_vector.x < columns:
            self.selected_button.x = test_vector.x

        if 0 < test_vector.y < rows:
            self.selected_button.y = test_vector.y

    def input(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYUP:
                if event.key == KEYBOARD["left"]:
                    self.move_selection(pygame.Vector2(-1, 0))
                if event.key == KEYBOARD["right"]:
                    self.move_selection(pygame.Vector2(1, 0))
                if event.key == KEYBOARD["down"]:
                    self.move_selection(pygame.Vector2(0, -1))
                if event.key == KEYBOARD["up"]:
                    self.move_selection(pygame.Vector2(0, 1))
                if event.key == KEYBOARD["A"]:
                    sel_button = self.button_layout[int(self.selected_button.y)][
                        int(self.selected_button.x)
                    ]
                    sel_button.execute()

    def update(self) -> None:
        self.input()

        win_size = self.client.original_window_size

        self.screen.fill((0, 0, 0))

        game_logo_rect = game_logo.get_rect()
        scaled_game_logo = pygame.transform.scale(
            game_logo, (game_logo_rect.width * 3, game_logo_rect.height * 3)
        )
        game_logo_rect = scaled_game_logo.get_rect()
        self.screen.blit(
            scaled_game_logo,
            (
                win_size.x / 2 - game_logo_rect.width / 2,
                win_size.y * (2 / 5) - game_logo_rect.height / 2,
            ),
        )

        for r in self.button_layout:
            for c in self.button_layout[len(r) - 1]:
                self.screen.blit(c.sprite, (c.rect.x, c.rect.y))
                if c.is_pressing_mousedown_instant(self.client.mouse_pos):
                    c.execute()
