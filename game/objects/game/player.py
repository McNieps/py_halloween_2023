import pymunk
import pygame

from isec.app import Resource
from isec.environment.base import Entity
from isec.environment.sprite import AnimatedSprite
from isec.environment.position import PymunkPos


class Player(Entity):
    def __init__(self,
                 position: tuple[float, float]) -> None:

        player_sprite = AnimatedSprite([Resource.image["game"][f"player_{i}"] for i in range(4)],
                                       [1, 1, 1, 1],
                                       rendering_technique="static")

        player_position = PymunkPos(position=position)
        player_position.create_rect_shape()
        player_position.body.moment = float('inf')
        super().__init__(position=player_position,
                         sprite=player_sprite)

        pass


if __name__ == '__main__':
    x = Player((0, 0))