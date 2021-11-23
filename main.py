import ctypes

from ProjectRespawn.Sakuya.client import Client
from ProjectRespawn.Sakuya.math import Vector
from ProjectRespawn.scenes.start import Start
from ProjectRespawn.Sakuya.scene import SceneManager

# get user's MONITOR RESOLUTION
user32 = ctypes.windll.user32
monitor_resolution = Vector(user32.GetSystemMetrics(0), user32.GetSystemMetrics(1))

RespawnClient = Client(
    "Project Respawn",
    Vector(monitor_resolution.x*0.6, monitor_resolution.y*0.6)
)
RespawnSceneManager = SceneManager(RespawnClient)
RespawnSceneManager.register_scene(Start)

RespawnClient.add_scene("Start")
RespawnClient.main()