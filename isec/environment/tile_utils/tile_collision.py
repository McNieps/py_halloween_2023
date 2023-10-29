import pygame
import pymunk
import pymunk.autogeometry

from isec.environment.base import Entity, Sprite
from isec.environment.position import PymunkPos
from isec.environment.sprite import PymunkSprite


class TileCollision(Entity):
    SHAPES_RADIUS = -0.5

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

        self._build_optimized_collision_shape(position)

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
                                             radius=self.SHAPES_RADIUS)
                    position.set_shape_characteristics(tile_shape)
                    position.shapes.append(tile_shape)

    def _build_optimized_collision_shape(self,
                                         position: PymunkPos) -> None:
        """Not possible to have holes..."""

        for polygon in self.build_enhanced_collision_shape():
            collision_shape = pymunk.Poly(position.body,
                                          vertices=polygon,
                                          radius=self.SHAPES_RADIUS)

            position.set_shape_characteristics(collision_shape)
            position.shapes.append(collision_shape)

    def build_enhanced_collision_shape(self) -> list:
        def sample_function(point):
            return self.collision_map[int(point[1])][int(point[0])]

        bounding_box = pymunk.BB(len(self.collision_map[0])-1, len(self.collision_map)-1)

        raw_polyset = pymunk.autogeometry.march_hard(bounding_box,
                                                     len(self.collision_map[0]),
                                                     len(self.collision_map),
                                                     0,
                                                     sample_function)

        sized_polyset = []

        for raw_polygon in raw_polyset:
            sized_polygon = []
            for raw_vertices in raw_polygon:
                sized_polygon.append((raw_vertices.x * self.tile_size + self.tile_size/2,
                                      raw_vertices.y * self.tile_size + self.tile_size/2))
            sized_polyset.append(sized_polygon)

        concave_polyset = []
        for sized_polygon in sized_polyset:
            try:
                fixed_polyset = pymunk.autogeometry.convex_decomposition(sized_polygon, 0)
            except AssertionError:
                sized_polygon.reverse()
                fixed_polyset = pymunk.autogeometry.convex_decomposition(sized_polygon, 0)
            for fixed_polygon in fixed_polyset:
                concave_polyset.append(fixed_polygon)

        return concave_polyset
