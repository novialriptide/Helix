"""
Helix: Flight Test (c) 2021 Andrew Hong
This code is licensed under MIT license (see LICENSE for details)
"""
import pygame

# Keyboard + Mouse
KEYBOARD = {
    "up": pygame.K_UP, 
    "left": pygame.K_LEFT, 
    "down": pygame.K_DOWN, 
    "right": pygame.K_RIGHT, 
    "A": pygame.K_z,
    "B": pygame.K_x,
    "X": pygame.K_a,
    "Y": pygame.K_s,
    "select": None,
    "start": pygame.K_ESCAPE
}

# Nintendo Switch
NS_CONTROLLER = {
    "up": 11, 
    "left": 13, 
    "down": 12, 
    "right": 14, 
    "A": 0,
    "B": 1,
    "X": None,
    "Y": None,
    "select": 4,
    "start": 6
}