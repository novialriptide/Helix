from ProjectRespawn.Sakuya.client import Client
from ProjectRespawn.Sakuya.math import Vector
from ProjectRespawn.scenes.start import Start
from ProjectRespawn.Sakuya.scene import SceneManager

RespawnClient = Client(
    "Project Respawn",
    Vector(1280, 720)
)
RespawnSceneManager = SceneManager(RespawnClient)
RespawnSceneManager.register_scene(Start)

RespawnClient.add_scene("Start")
RespawnClient.main()