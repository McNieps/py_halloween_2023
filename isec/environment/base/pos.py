import pygame
import pymunk

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from isec.environment.position.pymunk_pos import PymunkShapeInfo


class Pos:
    """
    An abstract position class
    """

    __slots__ = ["position",
                 "speed",
                 "damping",
                 "angle",
                 "angular_speed",
                 "angular_damping",
                 "space",
                 "body",
                 "shape_info"]

    def update(self,
               delta: float) -> None:
        pass
