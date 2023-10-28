import pygame

from collections.abc import Iterable

from isec.environment.base.pos import Pos
from isec.environment.base.sprite import Sprite


class Entity:
    def __init__(self,
                 position: Pos,
                 sprite: Sprite) -> None:

        self.to_delete: bool = False
        self.position: Pos = position
        self.sprite: Sprite = sprite

    def update(self,
               delta: float) -> None:
        """Update elements of this container."""

        self.position.update(delta)
        self.sprite.update(delta)

    def render(self,
               camera_offset: Iterable,
               surface: pygame.Surface,
               rect: pygame.Rect) -> None:
        """Render elements of this container."""

        self.sprite.render(surface, rect, camera_offset, self.position.a)
