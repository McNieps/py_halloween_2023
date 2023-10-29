import pygame
import pymunk

from isec.environment.base import Entity
from isec.environment.sprite import PymunkSprite
from isec.environment.position import PymunkPos


class Platform(Entity):
    def __init__(self, rect: pygame.Rect):
        position = PymunkPos(body_type=PymunkPos.TYPE_STATIC, position=rect.center)

        collision_shape = pymunk.Segment(position.body,
                                         (-rect.width/2, 0),
                                         (rect.width/2, 0),
                                         rect.height/2)

        position.add_shape(collision_shape)

        sprite = PymunkSprite(position)

        super().__init__(position=position, sprite=sprite)
