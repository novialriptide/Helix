import ctypes

from Helix.Sakuya.client import Client
from Helix.Sakuya.math import Vector
from Helix.scenes.start import Start
from Helix.Sakuya.scene import SceneManager

# get user's MONITOR RESOLUTION
user32 = ctypes.windll.user32
monitor_resolution = Vector(
    user32.GetSystemMetrics(0),
    user32.GetSystemMetrics(1)
)

HelixClient = Client(
    "Helix",
    monitor_resolution * 0.6
)
HelixSceneManager = SceneManager(HelixClient)
HelixSceneManager.register_scene(Start)
HelixClient.fps = 60

HelixClient.add_scene("Start")
HelixClient.main()