"""
Helix: Flight Test (c) 2021 Andrew Hong
This code is licensed under GNU LESSER GENERAL PUBLIC LICENSE (see LICENSE for details)
"""
import sys
import pygame
import json

from SakuyaEngine.scene import Scene
from SakuyaEngine.text import text2

from Helix.buttons import KEYBOARD, NS_CONTROLLER
from Helix.const import font5x3

class Dialogue(Scene):
    def on_awake(self, **kwargs) -> None:
        """Handles the Dialogue scene.

        Parameters:
            msgs (List[str]): List of messages that will be said.
            char_data (dict): Character data for the person speaking.
            expression (str): The expression upon awake.

        """
        pygame.joystick.init()
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            print(f"Console Controller Detected! [{self.joystick.get_name()}]")
        
        char_data = json.load(open(kwargs["char_data"]))
        
        self.font_size = 10
        self.msgs = kwargs["msgs"]
        self.char_name = char_data["name"]
        self.portaits = char_data["portaits"]
        self._expression = kwargs["expression"]
        self.exit_scene = kwargs["exit_scene"]
        self.msg_index = 0
        self._portait = pygame.image.load(self.portaits[self.expression]).convert_alpha()
        self.text = text2(self.msg, self.font_size, font5x3, (255, 255, 255))

    @property
    def msg(self) -> str:
        return self.msgs[self.msg_index]

    @property
    def expression(self) -> str:
        return self._expression
    
    @expression.setter
    def expression(self, value: str) -> None:
        self._expression = value
        self._portait = pygame.image.load(self.portaits[self._expression]).convert_alpha()

    @property
    def portait(self) -> pygame.Surface:
        return self._portait

    def input(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYUP:
                if event.key == KEYBOARD["A"]:
                    self.next_msg()

            if event.type == pygame.JOYBUTTONUP:
                if self.joystick.get_button(NS_CONTROLLER["A"]) == 0:
                    self.next_msg()

    def exit(self) -> None:
        self.exit_scene.paused = False
        self.client.remove_scene(self.name)
    
    def next_msg(self) -> None:
        self.msg_index += 1
        if self.msg_index == len(self.msgs):
            self.exit()
        try:
            self.text = text2(self.msg, self.font_size, font5x3, (255, 255, 255))
        except IndexError:
            pass

    def update(self) -> None:
        self.input()

        portait_rect = self.portait.get_rect()
        box = pygame.Surface((248, 64))
        box.blit(self.portait, (0, 0))
        box.blit(self.text, (portait_rect.width, 6))
        
        self.screen.blit(box, (4, self.screen.get_height() - box.get_height() - 4))