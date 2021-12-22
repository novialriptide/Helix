from Helix.SakuyaEngine.entity import Entity
from Helix.SakuyaEngine.bullets import Bullet, BulletSpawner
from Helix.SakuyaEngine.animation import Animation
from Helix.SakuyaEngine.particles import Particles
from Helix.SakuyaEngine.tile import split_image

from Helix.playercontroller import PlayerController

import pygame

HELIX = Entity(
    name = "Helix",
    tags = ["player"],
    max_health = 1,
    custom_hitbox_size = pygame.Vector2(3, 3),
    obey_gravity = False,
    update_bullet_spawners = False,
    speed = 2.5,
    draw_healthbar = False,
    controller = PlayerController,
    bullet_spawners = [
        BulletSpawner(
            Bullet(
                tags = ["player_bullet"],
                speed = 0,
                color = [255, 255, 0],
                damage = 2,
                custom_hitbox_size = pygame.Vector2(1, 1),
                static_sprite = split_image(
                    pygame.image.load("Helix\\sprites\\projectiles.png").convert_alpha(),
                    8, 8
                )[1]
            ),
            fire_rate = 100,
            bullet_speed = 15,
            bullet_lifetime = 1000,
            is_active = True
        )
    ],
    particle_systems = [
        Particles(
            pygame.Vector2(0, 2),
            colors = [
                [249, 199, 63],
                [255, 244, 70],
                [255, 78, 65]
            ],
            offset = pygame.Vector2(8, 4),
            particles_num = 0,
            spread = 1,
            lifetime = 500
        )
    ]
)

HELIX.anim_add(
    Animation(
        "idle_anim",
        split_image(
            pygame.image.load("Helix\\sprites\\helix_idle_anim.png").convert_alpha(),
            16, 16
        ),
        fps = 2
    )
)
HELIX.anim_set("idle_anim")