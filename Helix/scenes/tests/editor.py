"""
Helix: Flight Test (c) 2021 Andrew Hong
This code is licensed under MIT license (see LICENSE for details)
"""
import sys
import pygame

from Helix.SakuyaEngine.scene import Scene
from Helix.SakuyaEngine.button import Button

from Helix.wavemanager import HelixWaves
from Helix.data.entity.ado import ADO
from Helix.data.entity.berserk import BERSERK

class PathSelector:
    def __init__(self) -> None:
        self.points = []
        self._destroy_queue = False
    
    def set_point(self, point: pygame.Vector2) -> None:
        self.points.append(point)
    
    def draw(self, surface) -> str:
        if len(self.points) > 1:
            for i in range(len(self.points) - 1):
                pygame.draw.line(surface, (255, 255, 255), self.points[i], self.points[i + 1])

class Timeline:
    def __init__(self) -> None:
        self.time = 0

class Editor(Scene):
    def on_awake(self) -> None:
        pygame.joystick.init()
        try:
            self.joystick = pygame.joystick.Joystick(0)
            print(f"Console Controller Detected! [{self.joystick.get_name()}]")
        except:
            self.joystick = None

        win_size = self.client.original_window_size
        self.wave_manager = HelixWaves(0)
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
        
        radius = 10
        self.spawn_point_rects = []
        for s in self.spawn_points:
            self.spawn_point_rects.append(
                pygame.Rect(s - pygame.Vector2(radius, radius), (radius * 2, radius * 2))
            )
        
        self.stage_name = ""
        self.timeline = Timeline()
        
        self.loaded_paths = []
        self.loaded_enemies = [ADO, BERSERK]
        self.selected_enemy_key = 0
        self.selected_enemy_img = self.loaded_enemies[self.selected_enemy_key].sprite
        
        self.path_selector = None
        self.inital_axis = "up"
    
    def update_enemy_sprite(self):
        self.selected_enemy_img = self.loaded_enemies[self.selected_enemy_key].sprite
        self.selected_enemy_img = pygame.transform.scale(self.selected_enemy_img, (32, 32))
        
    def select_enemy(self, movement: int) -> None:
        if -1 < movement + self.selected_enemy_key < len(self.loaded_enemies):
            self.selected_enemy_key += movement
            self.update_enemy_sprite()
    
    def inputs(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    # Copy
                    pass
                if event.key == pygame.K_v:
                    # Paste
                    pass
                if event.key == pygame.K_s:
                    # Save
                    pass
                if event.key == pygame.K_n:
                    # New path
                    self.path_selector = PathSelector()
                if event.key == pygame.K_m:
                    # Mag snap
                    pass
                if event.key == pygame.K_BACKSPACE:
                    # Delete
                    pass
                if event.key == pygame.K_PLUS:
                    # Advance in timeline
                    pass
                if event.key == pygame.K_MINUS:
                    # Go back in timeline
                    pass
                if event.key == pygame.K_LEFT:
                    # Navigate selection enemies
                    self.select_enemy(-1)
                if event.key == pygame.K_RIGHT:
                    # Navigate selection enemies
                    self.select_enemy(1)
                if event.key == pygame.K_RETURN:
                    # Add enemy to path
                    pass
                if event.key == pygame.K_SPACE:
                    # Play stage
                    pass
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.path_selector is not None:
                    if len(self.path_selector.points) == 2:
                        if self.inital_axis == "up":
                            mp = self.client.mouse_position
                            self.path_selector.set_point(pygame.Vector2(mp.x, 0))
                            self.path_selector._destroy_queue = True

                    if len(self.path_selector.points) == 1:
                        self.path_selector.set_point(self.client.mouse_position)

                    if len(self.path_selector.points) == 0:
                        if self.inital_axis == "up":
                            mp = self.client.mouse_position
                            self.path_selector.set_point(pygame.Vector2(mp.x, 0))

    def update(self) -> None:
        win_size = self.client.original_window_size
        self.inputs()
        self.client.screen.fill((0,0,0))
        for r in self.spawn_point_rects:
            pygame.draw.rect(self.client.screen, (255, 0, 0), r)
        
        # Draw selected enemy
        self.client.screen.blit(self.selected_enemy_img, (0, win_size.y - self.selected_enemy_img.get_height()))
        
        if self.path_selector is not None:
            if 0 < len(self.path_selector.points) < 2:
                pygame.draw.line(self.client.screen, (255, 255, 255), self.path_selector.points[-1], self.client.mouse_position)
            self.path_selector.draw(self.client.screen)
            
            if self.path_selector._destroy_queue:
                self.loaded_paths.append(self.path_selector.points)
                self.path_selector = None
        
        for p in self.loaded_paths:
            if len(p) > 1:
                for i in range(len(p) - 1):
                    pygame.draw.line(self.client.screen, (255, 255, 255), p[i], p[i + 1])
        
        pygame.display.set_caption(f"{self.client.window_name} (time: {self.timeline.time})")