"""
Helix: Flight Test (c) 2021 Andrew Hong
This code is licensed under MIT license (see LICENSE for details)
"""
class WaterRipple:
    def __init__(self, max_radius: int) -> None:
        self.current_radius = 0
        self.max_radius = max_radius

    def update(self, delta_time: float) -> None:
        pass