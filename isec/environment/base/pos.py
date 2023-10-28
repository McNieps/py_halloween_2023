from collections.abc import Iterable

import pygame
import pymunk


class Pos:
    """
    An abstract position class
    """

    __slots__ = ["position", "speed", "accel", "damping", "a", "va", "aa", "a_damping", "body", "shapes"]

    def __init__(self,
                 position: Iterable = None,
                 speed: Iterable = None,
                 accel: Iterable = None,
                 damping: float = 1,
                 a: float = 0,
                 va: float = 0,
                 aa: float = 0,
                 a_damping: float = 1,
                 body: pymunk.Body = None,
                 shapes: list[pymunk.Shape] = None) -> None:

        if position is None:
            position = (0, 0)

        if speed is None:
            speed = (0, 0)

        if accel is None:
            accel = (0, 0)

        if shapes is None:
            shapes = []

        self.body: pymunk.Body = body
        self.shapes: list[pymunk.Shape] = shapes

        self.position: pygame.Vector2 = pygame.Vector2(*position)
        self.speed: pygame.Vector2 = pygame.Vector2(*speed)
        self.accel: pygame.Vector2 = pygame.Vector2(*accel)
        self.damping: float = damping

        self.a: float = a
        self.va: float = va
        self.aa: float = aa
        self.a_damping: float = a_damping


    def update(self,
               delta: float) -> None:
        pass
