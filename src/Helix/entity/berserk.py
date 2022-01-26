from SakuyaEngine.entity import Entity
from SakuyaEngine.bullets import Bullet, BulletSpawner
from SakuyaEngine.animation import Animation
from SakuyaEngine.effect_particles import Particles
from SakuyaEngine.tile import split_image

from Helix.entity.helix import HELIX
from Helix.const_bullets import *

import pygame

BERSERK = Entity(
    name="Berserk",
    tags=["enemy"],
    max_health=8,
    custom_hitbox_size=pygame.Vector2(8, 8),
    speed=1,
    bullet_spawners=[
        BulletSpawner(
            small_bullet1,
            iterations=4,
            bullets_per_array=1,
            total_bullet_arrays=1,
            fire_rate=400,
            spread_between_bullet_arrays=0,
            spread_within_bullet_arrays=20,
            bullet_lifetime=10000,
            bullet_speed=1,
            aim=True,
            target=HELIX,
            is_active=True,
            wait_until_reset=4000,
            repeat=True,
        )
    ],
    particle_systems=[
        Particles(
            pygame.Vector2(0, 0),
            colors=[[249, 199, 63], [255, 244, 70], [255, 78, 65]],
            offset=pygame.Vector2(8, 8),
            particles_num=0,
            spread=1,
            lifetime=500,
        )
    ],
)

BERSERK.anim_add(
    Animation(
        "idle_anim",
        split_image(
            pygame.image.load("Helix/sprites/berserk_idle_anim.png").convert_alpha(),
            16,
            16,
        ),
        fps=2,
    )
)
BERSERK.anim_set("idle_anim")
BERSERK.points_upon_death = 10
