"""
Helix: Flight Test (c) 2021 Andrew Hong
This code is licensed under GNU LESSER GENERAL PUBLIC LICENSE (see LICENSE for details)
"""
from typing import List, Tuple

import json
import sys
import pygame
import string
import random

from SakuyaEngine.scene import Scene
from SakuyaEngine.button import Button

from Helix.entity.ado import ADO
from Helix.entity.berserk import BERSERK


class PathSelector:
    def __init__(self) -> None:
        self.points = []
        self._destroy_queue = False

    def set_point(self, point: Tuple[int, int]) -> None:
        self.points.append(point)

    def draw(self, surface) -> str:
        if len(self.points) > 1:
            for i in range(len(self.points) - 1):
                pygame.draw.line(
                    surface, (255, 255, 255), self.points[i], self.points[i + 1]
                )


class Stage:
    def __init__(self, name: str, entities: List[str]) -> None:
        self.name = name
        self.time = 0
        self.max_time = 60000

        self.paths = {}
        self.waves = {}

    def save(self) -> None:
        path = "Helix/stages/"
        print(self.__dict__)
        with open(path + f"{self.name}.json", "w") as outfile:
            json.dump(self.__dict__, outfile)
            # use pickle to dump this


class Editor(Scene):
    def on_awake(self) -> None:
        pygame.joystick.init()
        try:
            self.joystick = pygame.joystick.Joystick(0)
            print(f"Console Controller Detected! [{self.joystick.get_name()}]")
        except:
            self.joystick = None

        stage_name = input("Stage name > ")

        win_size = self.client.original_window_size

        self.menu_size = (self.screen.get_width(), 128)
        self.menu = pygame.Surface(self.menu_size)
        self.menu_pos = (0, win_size.y - self.menu.get_height())
        self.draw_menu = False

        radius = 10

        self.stage_name = ""
        self.stage = Stage(stage_name, ["ADO", "BERSERK"])
        self.default_lifetime = 10000

        self.loaded_enemies = [ADO, BERSERK]
        self.selected_enemy_key = 0
        self.selected_enemy_img = self.loaded_enemies[self.selected_enemy_key].sprite

        self.path_selector = None
        self.selected_axis = "up1"
        self.selected_path_key = 0

        self.buttons = [
            Button(
                pygame.Rect(0, 32, 16, 16),
                [{"func": self.select_enemy, "args": [-1], "kwargs": {}}],
                color=(100, 0, 0),
            ),
            Button(
                pygame.Rect(16, 32, 16, 16),
                [{"func": self.select_enemy, "args": [1], "kwargs": {}}],
                color=(0, 100, 0),
            ),
            Button(
                pygame.Rect(32, 32, 16, 16),
                [{"func": self.select_path, "args": [-1], "kwargs": {}}],
                color=(100, 0, 0),
            ),
            Button(
                pygame.Rect(48, 32, 16, 16),
                [{"func": self.select_path, "args": [1], "kwargs": {}}],
                color=(0, 100, 0),
            ),
        ]

    def axis_points(self, axis: str) -> Tuple[int, int]:
        mp = pygame.Vector2(self.client.mouse_pos)
        win_size = self.client.original_window_size
        if axis == "up1":
            return (mp.x, 0)
        if axis == "down1":
            return (mp.x, win_size.y)
        if axis == "left1":
            return (0, mp.y)
        if axis == "right1":
            return (win_size.x, mp.y)

    def update_enemy_sprite(self):
        self.selected_enemy_img = self.loaded_enemies[self.selected_enemy_key].sprite
        self.selected_enemy_img = pygame.transform.scale(
            self.selected_enemy_img, (32, 32)
        )

    def select_enemy(self, movement: int) -> None:
        if -1 < movement + self.selected_enemy_key < len(self.loaded_enemies):
            self.selected_enemy_key += movement
            self.update_enemy_sprite()

    def select_path(self, movement: int) -> None:
        if -1 < movement + self.selected_path_key < len(self.stage.paths):
            self.selected_path_key += movement

    def get_path_id(self) -> None:
        return list(self.stage.paths.keys())[self.selected_path_key]

    def draw_path(self, path_id: str, color1, color2, width: int = 1) -> None:
        path = self.stage.paths[path_id]["paths"]
        pygame.draw.line(self.screen, color1, path[0], path[1], width=width)
        pygame.draw.line(self.screen, color2, path[1], path[2], width=width)

    def inputs(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if self.path_selector is not None:
                    if event.key == pygame.K_ESCAPE:
                        self.path_selector = None
                if event.key == pygame.K_c:
                    # Copy
                    pass
                if event.key == pygame.K_v:
                    # Paste
                    pass
                if event.key == pygame.K_h:
                    # Hide/unhide menu
                    self.draw_menu = not self.draw_menu
                if event.key == pygame.K_s:
                    # Save
                    self.stage.save()
                if event.key == pygame.K_n:
                    # New path
                    self.path_selector = PathSelector()
                if event.key == pygame.K_m:
                    # Mag snap
                    pass
                if event.key == pygame.K_BACKSPACE:
                    # Delete
                    pass
                if event.key == pygame.K_RETURN:
                    # Add enemy to path
                    enemy_key = self.selected_enemy_key
                    new_data = {"enemies": []}

                    if str(self.stage.time) not in self.stage.waves.keys():
                        self.stage.waves[str(self.stage.time)] = {}

                    if self.get_path_id() not in self.stage.waves[str(self.stage.time)]:
                        self.stage.waves[str(self.stage.time)][
                            self.get_path_id()
                        ] = new_data
                        print(
                            f"Added new wave + enemy ({enemy_key}) to path ({self.selected_path_key})"
                        )

                    self.stage.waves[str(self.stage.time)][self.get_path_id()][
                        "enemies"
                    ].append(self.selected_enemy_key)

                if event.key == pygame.K_SPACE:
                    # Play stage
                    pass
                if event.key == pygame.K_UP:
                    self.selected_axis = "up1"
                if event.key == pygame.K_DOWN:
                    self.selected_axis = "down1"
                if event.key == pygame.K_LEFT:
                    self.selected_axis = "left1"
                if event.key == pygame.K_RIGHT:
                    self.selected_axis = "right1"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.path_selector is not None:
                    if len(self.path_selector.points) == 2:
                        self.path_selector.set_point(
                            self.axis_points(self.selected_axis)
                        )
                        self.path_selector._destroy_queue = True

                    if len(self.path_selector.points) == 1:
                        self.path_selector.set_point(self.client.mouse_pos)

                    if len(self.path_selector.points) == 0:
                        self.path_selector.set_point(
                            self.axis_points(self.selected_axis)
                        )
            if event.type == pygame.MOUSEWHEEL:
                if self.stage.time + event.y >= 0:
                    self.stage.time += event.y

    def update(self) -> None:
        self.inputs()
        self.screen.fill((15, 15, 15))
        self.menu.fill((5, 5, 5))

        # Draw path maker
        if self.path_selector is not None:
            if len(self.path_selector.points) == 0:
                pygame.draw.line(
                    self.screen,
                    (100, 0, 0),
                    self.axis_points(self.selected_axis),
                    self.client.mouse_pos,
                )
            if len(self.path_selector.points) == 1:
                pygame.draw.line(
                    self.screen,
                    (100, 0, 0),
                    self.path_selector.points[-1],
                    self.client.mouse_pos,
                )
            if len(self.path_selector.points) == 2:
                pygame.draw.line(
                    self.screen,
                    (100, 0, 0),
                    self.path_selector.points[-1],
                    self.axis_points(self.selected_axis),
                )
            self.path_selector.draw(self.screen)

            if self.path_selector._destroy_queue:
                path_id = "".join(random.choices(string.ascii_lowercase, k=16))
                print(f"New path id created: {path_id}")
                self.stage.paths[path_id] = {"paths": self.path_selector.points}
                self.path_selector = None

        # Draw loaded paths
        for p in self.stage.paths:
            self.draw_path(p, (0, 100, 50), (200, 200, 200))

        # Draw selected path
        try:
            selected_path_id = list(self.stage.paths.keys())[self.selected_path_key]
            self.draw_path(selected_path_id, (0, 230, 0), (0, 230, 230), width=2)

        except IndexError:
            pass

        # Draw selected enemy menu
        pygame.draw.rect(self.menu, (212, 5, 212), (0, 0, 32, 32))
        self.menu.blit(self.selected_enemy_img, (0, 0))
        for b in self.buttons:
            pygame.draw.rect(self.menu, b.color, b.rect)
            pygame.draw.rect(self.menu, (255, 255, 255), b.rect, width=1)
            if b.is_pressing_mousedown_instant(
                pygame.Vector2(self.client.mouse_pos) - self.menu_pos
            ):
                b.execute()

        # Draw stage menu
        pygame.draw.rect(
            self.menu,
            (75, 75, 75),
            (0, self.menu.get_height() - 10, self.menu.get_width(), 8),
        )
        pygame.draw.rect(
            self.menu,
            (0, 125, 0),
            (
                0,
                self.menu.get_height() - 10,
                self.menu.get_width() * (self.stage.time / self.stage.max_time),
                8,
            ),
        )

        if self.draw_menu:
            self.screen.blit(self.menu, self.menu_pos)

        pygame.display.set_caption(
            f"{self.client.window_name} (time: {self.stage.time})"
        )
