"""
Helix: Flight Test (c) 2021 Andrew Hong
This code is licensed under MIT license (see LICENSE for details)
"""
import ctypes
import argparse

from Helix.SakuyaEngine.client import Client
from Helix.SakuyaEngine.math import Vector
from Helix.SakuyaEngine.scene import SceneManager

from Helix.scenes.start import Start
from Helix.scenes.death import Death
from Helix.scenes.splash import Splash

from Helix.scenes.tests.bullet_test import BulletTest

from Helix.const import player_sprites

# get user's MONITOR RESOLUTION
user32 = ctypes.windll.user32
monitor_resolution = Vector(
    user32.GetSystemMetrics(0),
    user32.GetSystemMetrics(1)
)

HelixClient = Client(
    "Helix",
    Vector(256, 224),
    scale_upon_startup = 2,
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

if args.fps:
    HelixClient.max_fps = args.fps

if args.scene:
    HelixClient.add_scene(args.scene)
else:
    HelixClient.add_scene("Splash")

HelixClient.main()