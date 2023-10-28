import pygame
import pymunk

from isec.environment.base import Entity, Sprite
from isec.environment.position import PymunkPos
from isec.environment.sprite import PymunkSprite


class TileCollision(Entity):
    def __init__(self,
                 collision_map: list[list[bool]],
                 tile_size: int,
                 wall_friction: float = None,
                 wall_elasticity: float = None,
                 show_collision: bool = False,
                 collision_type: int = None) -> None:

        self.collision_map = collision_map
        self.tile_size = tile_size

        position = PymunkPos(body_type=PymunkPos.TYPE_STATIC,
                             base_shape_friction=wall_friction,
                             base_shape_elasticity=wall_elasticity,
                             shape_collision_type=collision_type)

        self._build_collision_shape(position)

        sprite = PymunkSprite(position) if show_collision else Sprite(pygame.Surface((1, 1),
                                                                                     pygame.SRCALPHA))

        super().__init__(position=position, sprite=sprite)

    def _build_collision_shape(self,
                               position: PymunkPos) -> None:

        for y, row in enumerate(self.collision_map):
            for x, collision_tile in enumerate(row):
                if collision_tile:
                    vertices = [(x*self.tile_size, y*self.tile_size),
                                (x*self.tile_size+self.tile_size, y*self.tile_size),
                                (x*self.tile_size+self.tile_size, y*self.tile_size+self.tile_size),
                                (x*self.tile_size, y*self.tile_size+self.tile_size)]

                    tile_shape = pymunk.Poly(position.body,
                                             vertices,
                                             radius=0)
                    position.set_shape_characteristics(tile_shape)
                    position.shapes.append(tile_shape)
