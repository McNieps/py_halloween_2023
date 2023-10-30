import pygame

from typing import TYPE_CHECKING, Union
from collections.abc import Iterable

from isec.instance import BaseInstance
from isec.environment.base.pos import Pos
from isec.environment.base.sprite import Sprite


if TYPE_CHECKING:
    from isec.environment.scene import ComposedScene, EntityScene


class Entity:
    def __init__(self,
                 position: Pos,
                 sprite: Sprite,
                 linked_scene: Union["EntityScene", "ComposedScene"],
                 linked_instance: BaseInstance) -> None:

        # Metadata
        self.linked_scene = linked_scene
        self.linked_instance = linked_instance

        self.to_delete: bool = False
        self.position: Pos = position
        self.sprite: Sprite = sprite

        self.linked_scene.add_entities(self)

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

        self.sprite.render(surface, rect, camera_offset, self.position.angle)

    def destroy(self) -> None:
        """Destroy the entity."""

        self.to_delete = True
