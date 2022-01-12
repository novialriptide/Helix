from SakuyaEngine.entity import Entity
from SakuyaEngine.bullets import Bullet, BulletSpawner
from SakuyaEngine.animation import Animation
from SakuyaEngine.effect_particles import Particles
from SakuyaEngine.tile import split_image

from Helix.data.entity.helix import HELIX
from Helix.data.const_bullets import *

import pygame

ADO = Entity(
    name="Ado",
    tags=["enemy"],
    max_health=24,
    custom_hitbox_size=pygame.Vector2(11, 11),
    speed=1,
    bullet_spawners=[
        BulletSpawner(
            small_bullet1,
            iterations=3,
            bullets_per_array=3,
            total_bullet_arrays=6,
            fire_rate=500,
            spread_between_bullet_arrays=60,
            spread_within_bullet_arrays=40,
            bullet_lifetime=10000,
            bullet_speed=1,
            aim=True,
            target=HELIX,
            is_active=True,
            starting_angle=90,
            wait_until_reset=1000,
            repeat=True,
        ),
        BulletSpawner(
            big_bullet1,
            iterations=5,
            bullets_per_array=1,
            total_bullet_arrays=1,
            fire_rate=200,
            spread_between_bullet_arrays=0,
            spread_within_bullet_arrays=0,
            bullet_lifetime=2000,
            aim=True,
            target=HELIX,
            is_active=True,
            wait_until_reset=1000,
            repeat=True,
        ),
    ],
    particle_systems=[
        Particles(
            velocity=pygame.Vector2(0, -2),
            colors=[[249, 199, 63], [255, 244, 70], [255, 78, 65]],
            offset=pygame.Vector2(16, 16),
            particles_num=0,
            spread=1,
            lifetime=500,
        )
    ],
)

ADO.anim_add(
    Animation(
        "idle_anim",
        split_image(
            pygame.image.load("Helix/sprites/ado_idle_anim.png").convert_alpha(), 32, 32
        ),
        fps=1.5,
    )
)
ADO.anim_set("idle_anim")
ADO.points_upon_death = 20

ADO.shake_screen_on_death = True
