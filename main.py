"""
Helix: Flight Test (c) 2021 Andrew Hong
This code is licensed under MIT license (see LICENSE for details)
"""
import argparse
import pygame

from Helix.SakuyaEngine.client import Client

from Helix.SakuyaEngine.scene import SceneManager

from Helix.scenes.start import Start
from Helix.scenes.death import Death
from Helix.scenes.splash import Splash

from Helix.scenes.tests.bullet_test import BulletTest

from Helix.const import player_sprites

HelixClient = Client(
    "Helix",
    pygame.math.Vector2(256, 336),
    window_icon = player_sprites[0]
)
HelixSceneManager = SceneManager(HelixClient)
HelixSceneManager.register_scene(Splash)
HelixSceneManager.register_scene(Start)
HelixSceneManager.register_scene(Death)

HelixSceneManager.register_scene(BulletTest)

parser = argparse.ArgumentParser()
parser.add_argument("--scene", type=str, help="Load a scene")
parser.add_argument("--fps", type=int, help="Set the game fps")
args = parser.parse_args()

HelixClient.max_fps = 60

if args.fps is not None:
    HelixClient.max_fps = args.fps

if args.scene is not None:
    HelixClient.add_scene(args.scene)
else:
    HelixClient.add_scene("Splash")

HelixClient.main()