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

from Helix.data.entity.ado import ADO
from Helix.data.entity.berserk import BERSERK

class PathSelector:
    def __init__(self) -> None:
        self.points = []
        self._destroy_queue = False
    
    def set_point(self, point: Tuple[int, int]) -> None:
        self.points.append(point)
    
    def draw(self, surface) -> str:
        if len(self.points) > 1:
            for i in range(len(self.points) - 1):
                pygame.draw.line(surface, (255, 255, 255), self.points[i], self.points[i + 1])

class Stage:
    def __init__(self, name: str, entities: List[str]) -> None:
        self.name = name
        self.time = 0
        self.max_time = 60000
        
        self.paths = {}
        self.waves = {}
    
    def save(self) -> None:
        path = "Helix\\data\\stages\\"
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
        self.spawn_points = [
            pygame.Vector2(int(win_size.x * 1/10), int(win_size.y * 1/7)),
            pygame.Vector2(int(win_size.x * 3/10), int(win_size.y * 1/7)),
            pygame.Vector2(int(win_size.x * 5/10), int(win_size.y * 1/7)),
            pygame.Vector2(int(win_size.x * 7/10), int(win_size.y * 1/7)),
            pygame.Vector2(int(win_size.x * 9/10), int(win_size.y * 1/7)),

            pygame.Vector2(int(win_size.x * 1/10), int(win_size.y * 1.75/7)),
            pygame.Vector2(int(win_size.x * 3/10), int(win_size.y * 1.75/7)),
            pygame.Vector2(int(win_size.x * 5/10), int(win_size.y * 1.75/7)),
            pygame.Vector2(int(win_size.x * 7/10), int(win_size.y * 1.75/7)),
            pygame.Vector2(int(win_size.x * 9/10), int(win_size.y * 1.75/7)),

            pygame.Vector2(int(win_size.x * 1/10), int(win_size.y * 2.5/7)),
            pygame.Vector2(int(win_size.x * 3/10), int(win_size.y * 2.5/7)),
            pygame.Vector2(int(win_size.x * 5/10), int(win_size.y * 2.5/7)),
            pygame.Vector2(int(win_size.x * 7/10), int(win_size.y * 2.5/7)),
            pygame.Vector2(int(win_size.x * 9/10), int(win_size.y * 2.5/7)),
        ]
        
        self.menu_size = (self.screen.get_width(), 128)
        self.menu = pygame.Surface(self.menu_size)
        self.menu_pos = (0, win_size.y - self.menu.get_height())
        self.draw_menu = False

        radius = 10
        self.spawn_point_rects = []
        for s in self.spawn_points:
            self.spawn_point_rects.append(
                pygame.Rect(s - pygame.Vector2(radius, radius), (radius * 2, radius * 2))
            )
        
        self.stage_name = ""
        self.stage = Stage(stage_name, ["ADO", "BERSERK"])
        self.default_lifetime = 10000

        self.loaded_enemies = [ADO, BERSERK]
        self.selected_enemy_key = 0
        self.selected_enemy_img = self.loaded_enemies[self.selected_enemy_key].sprite
        
        self.path_selector = None
        self.selected_axis = "up"
        self.selected_path_key = 0
        
        self.buttons = [
            Button(pygame.Rect(0, 32, 16, 16), [{"func": self.select_enemy, "args": [-1], "kwargs": {}}], color = (100, 0, 0)),
            Button(pygame.Rect(16, 32, 16, 16), [{"func": self.select_enemy, "args": [1], "kwargs": {}}], color = (0, 100, 0)),
            
            Button(pygame.Rect(32, 32, 16, 16), [{"func": self.select_path, "args": [-1], "kwargs": {}}], color = (100, 0, 0)),
            Button(pygame.Rect(48, 32, 16, 16), [{"func": self.select_path, "args": [1], "kwargs": {}}], color = (0, 100, 0))
        ]
        
    def axis_points(self, axis: str) -> Tuple[int, int]:
        mp = pygame.mouse.get_pos()
        win_size = self.client.original_window_size
        if axis == "up":
            return (mp.x, 0)
        if axis == "down":
            return (mp.x, win_size.y)
        if axis == "left":
            return (0, mp.y)
        if axis == "right":
            return (win_size.x, mp.y)
        
    def update_enemy_sprite(self):
        self.selected_enemy_img = self.loaded_enemies[self.selected_enemy_key].sprite
        self.selected_enemy_img = pygame.transform.scale(self.selected_enemy_img, (32, 32))
        
    def select_enemy(self, movement: int) -> None:
        if -1 < movement + self.selected_enemy_key < len(self.loaded_enemies):
            self.selected_enemy_key += movement
            self.update_enemy_sprite()
            
    def select_path(self, movement: int) -> None:
        if -1 < movement + self.selected_path_key < len(self.stage.paths):
            self.selected_path_key += movement
        
    def get_path_id(self) -> None:
        return list(self.stage.paths.keys())[self.selected_path_key]
    
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
                        self.stage.waves[str(self.stage.time)][self.get_path_id()] = new_data
                        print(f"Added new wave + enemy ({enemy_key}) to path ({self.selected_path_key})")
                        
                    self.stage.waves[str(self.stage.time)][self.get_path_id()]["enemies"].append(self.selected_enemy_key)
                    
                if event.key == pygame.K_SPACE:
                    # Play stage
                    pass
                if event.key == pygame.K_UP:
                    self.selected_axis = "up"
                if event.key == pygame.K_DOWN:
                    self.selected_axis = "down"
                if event.key == pygame.K_LEFT:
                    self.selected_axis = "left"
                if event.key == pygame.K_RIGHT:
                    self.selected_axis = "right"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.path_selector is not None:
                    if len(self.path_selector.points) == 2:
                        self.path_selector.set_point(self.axis_points(self.selected_axis))
                        self.path_selector._destroy_queue = True

                    if len(self.path_selector.points) == 1:
                        self.path_selector.set_point((pygame.mouse.get_pos().x, pygame.mouse.get_pos().y))

                    if len(self.path_selector.points) == 0:
                        self.path_selector.set_point(self.axis_points(self.selected_axis))
            if event.type == pygame.MOUSEWHEEL:
                if self.stage.time + event.y >= 0:
                    self.stage.time += event.y

    def update(self) -> None:
        win_size = self.client.window_size
        self.inputs()
        self.screen.fill((15, 15, 15))
        self.menu.fill((5, 5, 5))
        for r in self.spawn_point_rects:
            pygame.draw.rect(self.screen, (255, 0, 0), r)
        
        # Draw path maker
        if self.path_selector is not None:
            if len(self.path_selector.points) == 0:
                pygame.draw.line(self.screen, (100, 0, 0), self.axis_points(self.selected_axis), pygame.mouse.get_pos())
            if len(self.path_selector.points) == 1:
                pygame.draw.line(self.screen, (100, 0, 0), self.path_selector.points[-1], pygame.mouse.get_pos())
            if len(self.path_selector.points) == 2:
                pygame.draw.line(self.screen, (100, 0, 0), self.path_selector.points[-1], self.axis_points(self.selected_axis))
            self.path_selector.draw(self.screen)
            
            if self.path_selector._destroy_queue:
                path_id = ''.join(random.choices(string.ascii_lowercase, k=16))
                print(f"New path id created: {path_id}")
                self.stage.paths[path_id] = {"paths": self.path_selector.points}
                self.path_selector = None
        
        # Draw loaded paths
        for p in self.stage.paths:
            path = self.stage.paths[p]["paths"]
            if len(p) > 1:
                for i in range(len(path) - 1):
                    color1 = (0, 200, 0)
                    color2 = (200, 200, 200)
                    if p == list(self.stage.paths.keys())[self.selected_path_key]:
                        color1 = (0, 230, 0)
                        color2 = (0, 230, 230)
                    if i == 0:
                        pygame.draw.line(self.screen, color1, path[i], path[i + 1])
                    else:
                        pygame.draw.line(self.screen, color2, path[i], path[i + 1])
        
        # Draw selected enemy menu
        pygame.draw.rect(self.menu, (212, 5, 212), (0, 0, 32, 32))
        self.menu.blit(self.selected_enemy_img, (0, 0))
        for b in self.buttons:
            pygame.draw.rect(self.menu, b.color, b.rect)
            pygame.draw.rect(self.menu, (255, 255, 255), b.rect, width = 1)
            if b.is_pressing_mousedown_instant(pygame.mouse.get_pos() - self.menu_pos):
                b.execute()
                
        # Draw stage menu
        pygame.draw.rect(self.menu, (75, 75, 75), (0, self.menu.get_height() - 10, self.menu.get_width(), 8))
        pygame.draw.rect(self.menu, (0, 125, 0), (0, self.menu.get_height() - 10, self.menu.get_width() * (self.stage.time / self.stage.max_time), 8))
        
        if self.draw_menu:
            self.screen.blit(self.menu, self.menu_pos)

        
        pygame.display.set_caption(f"{self.client.window_name} (time: {self.stage.time})")