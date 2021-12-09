"""
Helix: Flight Test (c) 2021 Andrew Hong
This code is licensed under MIT license (see LICENSE for details)
"""
import pygame

from Helix.SakuyaEngine.tile import split_image

player_sprites = split_image(
    pygame.image.load("Helix\\sprites\\helix_idle_anim.png"), 16, 16
)

pygame_powered_logo = pygame.image.load("Helix\\sprites\\pygame_powered.png")

font5x3 = "Helix\\fonts\\bit5x3.ttf"
font5x5 = "Helix\\fonts\\bit5x5.ttf"