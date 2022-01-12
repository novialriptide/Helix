"""
Helix: Flight Test (c) 2021 Andrew Hong
This code is licensed under GNU LESSER GENERAL PUBLIC LICENSE (see LICENSE for details)
"""
import pygame

# Keyboard + Mouse
KEYBOARD = {
    "up1": pygame.K_UP,
    "left1": pygame.K_LEFT,
    "down1": pygame.K_DOWN,
    "right1": pygame.K_RIGHT,
    "up2": pygame.K_w,
    "left2": pygame.K_a,
    "down2": pygame.K_s,
    "right2": pygame.K_d,
    "A": pygame.K_z,
    "B": pygame.K_x,
    "X": None,
    "Y": None,
    "select": pygame.K_q,
    "start": pygame.K_ESCAPE,
}

# Nintendo Switch
NS_CONTROLLER = {
    "up1": 11,
    "left1": 13,
    "down1": 12,
    "right1": 14,
    "A": 0,
    "B": 1,
    "X": None,
    "Y": None,
    "select": 4,
    "start": 6,
}
