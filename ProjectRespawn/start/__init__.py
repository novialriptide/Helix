import sys
import pygame

from ProjectRespawn import Sakuya
from ProjectRespawn.Sakuya.scene import Scene

class Start(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_awake(self) -> None:
        print("Awakening")

    def update(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        print("s")