"""
Helix: Flight Test (c) 2021 Andrew Hong
This code is licensed under MIT license (see LICENSE for details)
"""
import argparse
import pygame

from Helix.SakuyaEngine.client import Client
from Helix.SakuyaEngine.scene import SceneManager

HelixClient = Client(
    "Helix",
    pygame.Vector2(256, 336)
)

from Helix.scenes.start import Start
from Helix.scenes.death import Death
from Helix.scenes.splash import Splash
from Helix.scenes.dialogue import Dialogue
from Helix.scenes.pause import Pause
from Helix.scenes.tests.bullet_test import BulletTest

scenes = [Splash, Start, Death, Pause, Dialogue, BulletTest]
HelixSceneManager = SceneManager(HelixClient)
for s in scenes:
    HelixSceneManager.register_scene(s)

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