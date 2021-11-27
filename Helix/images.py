from Helix.Sakuya.tile import split_image

import pygame

player_sprites = split_image(
    pygame.image.load("Helix\sprites\ship.png"), 16, 16
)

enemy_sprites = split_image(
    pygame.image.load("Helix\sprites\ship3.png"), 32, 32
)

projectile_sprites = split_image(
    pygame.image.load("Helix\sprites\projectiles.png"), 8, 8
)