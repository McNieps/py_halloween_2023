import pygame

from collections.abc import Iterable
from isec.environment.position.simple_pos import SimplePos


class AdvancedPos(SimplePos):
    """
    An advanced class used to position a sprite inside a space.

    Feature:
        - x  y   position.
        - vx vy  speed.
        - ax ay  acceleration.
        - a      angle.
        - va     angular speed.
        - aa     angular acceleration.
        - damp   vx, vy damping.
        - a damp angular damping.
    """

    def __init__(self,
                 position: Iterable = None,
                 speed: Iterable = None,
                 accel: Iterable = None,
                 a: float = 0,
                 va: float = 0,
                 aa: float = 0,
                 damping: float = 1,
                 a_damping: float = 1) -> None:

        super().__init__(position=position,
                         speed=speed)

        if accel is not None:
            self.acceleration = pygame.math.Vector2(*speed)
        else:
            self.acceleration = pygame.math.Vector2(0, 0)

        self.a = a
        self.va = va
        self.aa = aa

        self.damping = damping
        self.a_damping = a_damping

    def update(self,
               delta: float) -> None:
        """
        Update position.

        The position will change because of speed.
        The speed will change because of acceleration and damping.

        The angle will change because of angular speed.
        The angular speed will change because of angular acceleration and angular damping.
        """

        self.speed += self.acceleration * delta

        if self.speed.magnitude():
            self.speed.scale_to_length(self.speed.magnitude()*self.damping**delta)

        self.va += self.aa * delta
        self.va *= self.a_damping ** delta
        self.a += self.va * delta

        super().update(delta)  # Change position -> function of speed

    @property
    def ax(self):
        return self.acceleration[0]

    @property
    def ay(self):
        return self.acceleration[1]
