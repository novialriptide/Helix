from SakuyaEngine.scene import Scene

class Ability:
    def __init__(self, cooldown: int, scene: Scene) -> None:
        self.cooldown = cooldown
        self.scene = scene
        
        self.active = False
        self.enabled = True
        
    def draw(self) -> None:
        pass

    def update(self, delta_time: float) -> None:
        pass