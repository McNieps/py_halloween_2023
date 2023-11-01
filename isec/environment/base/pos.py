import pygame
import pymunk

from typing import TYPE_CHECKING, Union, Type

if TYPE_CHECKING:
    from isec.environment.position.pymunk_pos import PymunkShapeInfo


class Pos:
    """
    An abstract position class
    """

    __slots__ = ["_position",
                 "_speed",
                 "_damping",
                 "_angle",
                 "_angular_speed",
                 "_angular_damping",
                 "_space",
                 "_body",
                 "_shapes",
                 "_shape_info"]

    def __init__(self):
        self._position: pygame.Vector2 = pygame.Vector2(0, 0)
        self._speed: pygame.Vector2 = pygame.Vector2(0, 0)
        self._damping: float = 0
        self._angle: float = 0
        self._angular_speed: float = 0
        self._angular_damping: float = 0
        self._space: pymunk.Space | None = None
        self._body: pymunk.Body | None = None
        self._shapes: list[pymunk.Shape] = []
        self._shape_info: Union["PymunkShapeInfo", None] = None

    def update(self,
               delta: float) -> None:
        pass

    def add_to_space(self) -> None:
        err_msg = "Only PymunkPos support add_to_space method"
        raise TypeError(err_msg)

    def remove_from_space(self) -> None:
        err_msg = "Only PymunkPos support remove_from_space method"
        raise TypeError(err_msg)

    def add_shape(self,
                  shape: pymunk.Shape,
                  shape_info: Type["PymunkShapeInfo"] | None = None) -> None:
        err_msg = "Only PymunkPos support add_shape method"
        raise TypeError(err_msg)

    @property
    def position(self) -> pygame.Vector2:
        return self._position

    @position.setter
    def position(self,
                 position: pygame.Vector2) -> None:
        self._position = position

    @property
    def x(self) -> float:
        return self._position[0]

    @x.setter
    def x(self,
          x: float) -> None:
        self._position[0] = x

    @property
    def y(self) -> float:
        return self._position[1]

    @y.setter
    def y(self,
          y: float) -> None:
        self._position[1] = y

    @property
    def speed(self) -> pygame.Vector2:
        return self._speed

    @speed.setter
    def speed(self,
              speed: pygame.Vector2) -> None:
        self._speed = speed

    @property
    def vx(self) -> float:
        return self._speed[0]

    @vx.setter
    def vx(self,
           vx: float) -> None:
        self._speed[0] = vx

    @property
    def vy(self) -> float:
        return self._speed[1]

    @vy.setter
    def vy(self,
           vy: float) -> None:
        self._speed[1] = vy

    @property
    def damping(self) -> float:
        return self._damping

    @damping.setter
    def damping(self,
                damping: float) -> None:
        self._damping = damping

    @property
    def angle(self) -> float:
        return self._angle

    @angle.setter
    def angle(self,
              angle: float) -> None:
        self._angle = angle

    @property
    def angular_speed(self) -> float:
        return self._angular_speed

    @angular_speed.setter
    def angular_speed(self,
                      angular_speed: float) -> None:
        self._angular_speed = angular_speed

    @property
    def angular_damping(self) -> float:
        return self._angular_damping

    @angular_damping.setter
    def angular_damping(self,
                        angular_damping: float) -> None:
        self._angular_damping = angular_damping

    @property
    def space(self) -> pymunk.Space | None:
        return self._space

    @space.setter
    def space(self,
              _space: pymunk.Space) -> None:
        err_msg = "Only PymunkPos support space assignment"
        raise TypeError(err_msg)

    @property
    def body(self) -> pymunk.Body | None:
        return self._body

    @body.setter
    def body(self,
             _body: pymunk.Body) -> None:
        err_msg = "Only PymunkPos support body assignment"
        raise TypeError(err_msg)

    @property
    def shapes(self) -> list[pymunk.Shape]:
        return self._shapes

    @property
    def shape_info(self) -> Union["PymunkShapeInfo", None]:
        return self._shape_info

    @shape_info.setter
    def shape_info(self,
                   _shape_info: "PymunkShapeInfo") -> None:
        err_msg = "Only PymunkPos support shape_info assignment"
        raise TypeError(err_msg)
