import pygame

from collections.abc import Iterable
from isec.environment.position.static_pos import StaticPos


class SimplePos(StaticPos):
    """
    A basic class used to position a sprite inside a space.

    Feature:
        - x  y   position.
        - vx vy  speed.
    """

    def __init__(self,
                 position: Iterable = None,
                 speed: Iterable = None,
                 **kwargs):

        super().__init__(position, **kwargs)

        if speed is not None:
            self.speed = pygame.math.Vector2(*speed)
        else:
            self.speed = pygame.math.Vector2(0, 0)

    def update(self,
               delta: float) -> None:
        """
        Update position.

        The position will change because of speed.
        """

        self.position += self.speed * delta

    @property
    def vx(self):
        return self.speed[0]

    @property
    def vy(self):
        return self.speed[1]


if __name__ == '__main__':
    x = StaticPos(position=(0, 5))
    print(x.x)
    print(x.y)
