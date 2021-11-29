import ctypes

from Helix.SakuyaEngine.client import Client
from Helix.SakuyaEngine.math import Vector
from Helix.SakuyaEngine.scene import SceneManager

from Helix.scenes.start import Start
from Helix.scenes.death import Death
from Helix.images import player_sprites

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
HelixSceneManager.register_scene(Start)
HelixSceneManager.register_scene(Death)
HelixClient.max_fps = 60

HelixClient.add_scene("Start")
HelixClient.main()