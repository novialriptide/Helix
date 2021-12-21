"""
Helix: Flight Test (c) 2021 Andrew Hong
This code is licensed under MIT license (see LICENSE for details)
"""
import sys
import pygame

from Helix.SakuyaEngine.scene import Scene
from Helix.SakuyaEngine.button import Button

from Helix.wavemanager import HelixWaves

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
        
        def add_enemy(enemy_name: str, vector: pygame.Vector2, time: int):
            pass
        
        radius = 10
        self.spawn_point_buttons = []
        for s in self.spawn_points:
            self.spawn_point_buttons.append(
                Button(pygame.Rect(s - pygame.Vector2(radius, radius), (radius * 2, radius * 2)), methods=[
                    {"func": add_enemy, "args": [], "kwargs": []}
                ])
            )
        
        self.stage_name = ""
        self.timeline = Timeline()

    def update(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        
        self.client.screen.fill((0,0,0))
        for s in self.spawn_point_buttons:
            pygame.draw.rect(self.client.screen, (255, 0, 0), s.rect)
            if s.is_pressing_mousedown_instant(self.client.mouse_position):
                pygame.draw.rect(self.client.screen, (0, 255, 0), s.rect)
        
        pygame.display.set_caption(f"{self.client.window_name} (time: {self.timeline.time})")