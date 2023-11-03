import pygame

from isec.app import Resource
from isec.environment.scene import ComposedScene
from isec.instance import BaseInstance
from isec.environment import Entity
from isec.environment.sprite import AnimatedSprite
from isec.environment.position import SimplePos


class Arrow(Entity):
    def __init__(self,
                 position: pygame.Vector2,
                 angle: float,
                 scene: ComposedScene,
                 instance: BaseInstance) -> None:

        arrow_pos = SimplePos(position)
        arrow_pos.angle = angle

        arrow_sprite = AnimatedSprite([Resource.image["game"]["objects"][f"arrow_{i}"] for i in range(1, 5)],
                                      [0.2, 0.1, 0.2, 0.1], rendering_technique="rotated")

        super().__init__(arrow_pos, arrow_sprite, scene, instance)
