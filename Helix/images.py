"""
Helix: Flight Test (c) 2021 Andrew Hong
This code is licensed under MIT license (see LICENSE for details)
"""
import pygame

from Helix.SakuyaEngine.tile import split_image

projectile_sprites = split_image(
    pygame.image.load("Helix\\sprites\\projectiles.png"), 8, 8
)

player_sprites = split_image(
    pygame.image.load("Helix\\sprites\\ship.png"), 16, 16
)

enemy_sprites = split_image(
    pygame.image.load("Helix\\sprites\\ado_idle_anim.png"), 32, 32
)

pygame_powered_logo = pygame.image.load("Helix\\sprites\\pygame_powered.png")