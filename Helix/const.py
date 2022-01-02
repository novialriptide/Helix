"""
Helix: Flight Test (c) 2021 Andrew Hong
This code is licensed under GNU LESSER GENERAL PUBLIC LICENSE (see LICENSE for details)
"""
import pygame

from Helix.SakuyaEngine.tile import split_image

DEFAULT_COLORKEY = (255,0,252)

player_sprites = split_image(
    pygame.image.load("Helix\\sprites\\helix_idle_anim.png").convert_alpha(),
    16, 16
)

vignette_overlay = pygame.image.load("Helix\\sprites\\vignette_overlay.png").convert_alpha()
vignette_overlay.set_alpha(10)
noise_overlay = pygame.image.load("Helix\\sprites\\noise_overlay.png").convert_alpha()
noise_overlay.set_alpha(4)
pygame_powered_logo = pygame.image.load("Helix\\sprites\\pygame_powered.png").convert_alpha()

font5x3 = "Helix\\fonts\\bit5x3.ttf"
font5x5 = "Helix\\fonts\\bit5x5.ttf"

explosion_colors = [
    [249, 199, 63],
    [255, 244, 70],
    [255, 78, 65],
    [89, 89, 89]
]

start_button = pygame.image.load("Helix\\sprites\\button_start.png").convert_alpha()
endless_button = pygame.image.load("Helix\\sprites\\button_endless.png").convert_alpha()
try_again_button = pygame.image.load("Helix\\sprites\\button_try_again.png").convert_alpha()

game_logo = pygame.image.load("Helix\\sprites\\game_logo.png").convert_alpha()