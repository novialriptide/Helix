from SakuyaEngine.tile import split_image
from SakuyaEngine.bullets import Bullet

import pygame

player_big_bullet1 = Bullet(
    tags=["player_bullet"],
    speed=0,
    color=[255, 255, 0],
    damage=2,
    custom_hitbox_size=pygame.Vector2(1, 1),
    static_sprite=split_image(
        pygame.image.load("Helix/sprites/projectiles.png").convert_alpha(), 8, 8
    )[1],
    sound_upon_fire=pygame.mixer.Sound("Helix/audio/sound_laser_1.mp3"),
)

small_bullet1 = Bullet(
    tags=["enemy_bullet"],
    speed=0,
    color=[255, 255, 0],
    damage=2,
    custom_hitbox_size=pygame.Vector2(1, 1),
    static_sprite=split_image(
        pygame.image.load("Helix/sprites/projectiles2.png").convert_alpha(), 3, 3
    )[0],
)

big_bullet1 = Bullet(
    tags=["enemy_bullet"],
    speed=0,
    color=[255, 255, 0],
    damage=2,
    custom_hitbox_size=pygame.Vector2(3, 3),
    static_sprite=split_image(
        pygame.image.load("Helix/sprites/projectiles.png").convert_alpha(), 8, 8
    )[0],
)
