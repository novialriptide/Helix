from ProjectRespawn.Sakuya.client import Client
from ProjectRespawn.Sakuya.math import Vector
from ProjectRespawn.start import Start

RespawnClient = Client(
    "Project Respawn",
    Vector(1280, 720)
)

RespawnClient.add_scene(Start)
RespawnClient.main()