from Helix.SakuyaEngine.controllers import BaseController

class PlayerController(BaseController):
    def __init__(self) -> None:
        super().__init__(1.5)
        self.is_shooting = False