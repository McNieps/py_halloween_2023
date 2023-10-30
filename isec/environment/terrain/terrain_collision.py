import pygame
import pymunk
import pymunk.autogeometry

from typing import Self, Type

from isec.instance import BaseInstance
from isec.environment.base import Entity, Sprite, Scene
from isec.environment.position.pymunk_pos import PymunkPos, PymunkShapeInfo
from isec.environment.sprite import PymunkSprite


class TerrainCollision(Entity):
    SHAPES_RADIUS = 4

    def __init__(self,
                 polygon: list[tuple],
                 shape_info: Type[PymunkShapeInfo],
                 linked_scene: Scene,
                 linked_instance: BaseInstance,
                 show_collisions: bool = False) -> None:

        position = PymunkPos(space=linked_scene.space,
                             body_type="STATIC",
                             default_shape_info=shape_info)

        position.add_shape(pymunk.Poly(body=position.body,
                                       vertices=polygon,
                                       radius=self.SHAPES_RADIUS))

        sprite = PymunkSprite(position) if show_collisions else Sprite(pygame.Surface((1, 1),
                                                                                      pygame.SRCALPHA))
        super().__init__(position=position,
                         sprite=sprite,
                         linked_scene=linked_scene,
                         linked_instance=linked_instance)

    @classmethod
    def from_collision_map(cls,
                           collision_map: list[list[bool]],
                           tile_size: int,
                           linked_scene: Scene,
                           linked_instance: BaseInstance,
                           shape_info: Type[PymunkShapeInfo] = None,
                           show_collisions: bool = False) -> list[Self]:

        entities = []

        for polygon in cls._decompose_collision_map_into_polygons(collision_map, tile_size):
            new_body = cls(polygon=polygon,
                           shape_info=shape_info,
                           linked_scene=linked_scene,
                           linked_instance=linked_instance,
                           show_collisions=show_collisions)

            entities.append(new_body)

        return entities

    """
    def _build_collision_shape(self,
                               position: PymunkPos) -> None:
        Not possible to have holes...

        for polygon in self._decompose_terrain_into_polygons():
            collision_shape = pymunk.Poly(position.body,
                                          vertices=polygon,
                                          radius=self.SHAPES_RADIUS)

            position.set_shape_characteristics(collision_shape)
            position.shapes.append(collision_shape)
    """

    @staticmethod
    def _decompose_collision_map_into_polygons(collision_map: list[list[bool]],
                                               tile_size: int) -> list[list[tuple]]:
        """Edges must be not collidable! It's cause by pymunk.autogeometry.march_hard and march_soft functions."""

        def sample_function(point):
            return collision_map[round(point[1])][round(point[0])]

        bounding_box = pymunk.BB(len(collision_map[0])-1, len(collision_map)-1)

        raw_polyset = pymunk.autogeometry.march_hard(bounding_box,
                                                     len(collision_map[0]),
                                                     len(collision_map),
                                                     0,
                                                     sample_function)

        sized_polyset = []

        for raw_polygon in raw_polyset:
            sized_polygon = []
            for raw_vertices in raw_polygon:
                sized_polygon.append((raw_vertices.x * tile_size + tile_size/2,
                                      raw_vertices.y * tile_size + tile_size/2))

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