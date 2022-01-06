"""
Helix: Flight Test (c) 2021 Andrew Hong
This code is licensed under GNU LESSER GENERAL PUBLIC LICENSE (see LICENSE for details)
"""
import argparse
import pygame

from Helix.SakuyaEngine.client import Client
from Helix.SakuyaEngine.scene import SceneManager
from Helix.__version__ import GAME_VERSION

HelixClient = Client(
    f"Helix (ver: {GAME_VERSION})",
    pygame.Vector2(256, 336)
)

pygame.mixer.init()
pygame.mixer.set_num_channels(64)

from Helix.scenes.ocean import Ocean
from Helix.scenes.death import Death
from Helix.scenes.splash import Splash
from Helix.scenes.dialogue import Dialogue
from Helix.scenes.pause import Pause
from Helix.scenes.tests.bullet_test import BulletTest
from Helix.scenes.tests.editor import Editor
from Helix.scenes.mainmenu import MainMenu
from Helix.scenes.components import Components

scenes = [Splash, MainMenu, Ocean, Death, Pause, Dialogue, BulletTest, Editor, Components]
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