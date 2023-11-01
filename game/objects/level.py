from isec.app import Resource
from isec.environment.scene import ComposedScene
from isec.environment.base import Tilemap
from isec.environment.terrain.terrain_collision import TerrainCollision
from isec.instance import BaseInstance

from game.objects.shape_info import TerrainSI


class Level:
    def __init__(self,
                 level_name: str,
                 scene: ComposedScene,
                 instance: BaseInstance) -> None:

        self.level_name = level_name
        self.scene = scene
        self.instance = instance

        self.data = Resource.data["levels"][self.level_name]

        self.collidable_tilemap: Tilemap | None = None
        self.collision_map: list[list[bool]] | None = None

        self.load_level()

    def load_level(self) -> None:
        self._create_tilemaps()
        self._create_collision_entities()
        # self._add_entities()

    def _create_tilemaps(self):
        for tilemap_name in self.data["info"]["tilemaps"]:
            tilemap_depth = 1
            if "parallax_depth" in self.data["info"]["tilemaps"][tilemap_name]:
                tilemap_depth = self.data["info"]["tilemaps"][tilemap_name]["parallax_depth"]

            tileset_surface = Resource.image
            for key in self.data["info"]["tilemaps"][tilemap_name]["tileset"]["path"]:
                tileset_surface = tileset_surface[key]

            tile_size = self.data["info"]["tilemaps"][tilemap_name]["tileset"]["tile_size"]
            tile_margin = self.data["info"]["tilemaps"][tilemap_name]["tileset"]["margin"]
            tile_spacing = self.data["info"]["tilemaps"][tilemap_name]["tileset"]["spacing"]

            tileset = Tilemap.create_tileset_from_surface(tileset_surface,
                                                          tile_size,
                                                          tile_margin,
                                                          tile_spacing)

            tilemap = Tilemap(tilemap_array=self.data[tilemap_name],
                              tileset=tileset,
                              parallax_depth=tilemap_depth)

            tilemap.name = tilemap_name

            if "collidable_tiles" in self.data["info"]["tilemaps"][tilemap_name]:
                self.collidable_tilemap = tilemap
                self.collision_map = tilemap.create_collision_map(self.data["info"]["tilemaps"][tilemap_name]["collidable_tiles"])

            self.scene.add_tilemap_scene(tilemap)

    def _create_collision_entities(self) -> None:
        if self.collidable_tilemap:
            terrain_entities = TerrainCollision.from_collision_map(self.collision_map,
                                                                   self.collidable_tilemap.tile_size,
                                                                   self.scene,
                                                                   self.instance,
                                                                   shape_info=TerrainSI,
                                                                   show_collisions=False)

            self.scene.add_entities(*terrain_entities)

    def _add_entities(self):
        pass
