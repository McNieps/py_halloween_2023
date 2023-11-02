import pygame

from collections.abc import Iterable

from isec.environment.base import Pos


class StaticPos(Pos):
    """
    A very simple class used to position a sprite inside a space.

    Feature:
        - x y  position.
    """

    def __init__(self,
                 position: Iterable = None) -> None:

        super().__init__()
        self.position = pygame.math.Vector2(*position) if position is not None else pygame.math.Vector2(0, 0)

    def update(self,
               _delta: float) -> None:
        """
        Update position.

        Nothing will happen because this position is static.
        """
        return

    @property
    def x(self) -> float:
        return self.position[0]

    @x.setter
    def x(self,
          value: float) -> None:
        self.position.x = value

    @property
    def y(self) -> float:
        return self.position[1]

    @y.setter
    def y(self,
          value: float) -> None:
        self.position.y = value


if __name__ == '__main__':
    x = StaticPos(position=(0, 5))
    print(x.x)
    print(x.y)
