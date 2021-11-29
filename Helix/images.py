from Helix.SakuyaEngine.tile import split_image

import pygame

projectile_sprites = split_image(
    pygame.image.load("Helix\sprites\projectiles.png"), 8, 8
)

player_sprites = split_image(
    pygame.image.load("Helix\sprites\ship.png"), 16, 16
)

enemy_sprites = split_image(
    pygame.image.load("Helix\sprites\enemy1_FINAL.png"), 32, 32
)