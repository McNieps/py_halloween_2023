from isec.app import Resource
from isec.environment.scene import ComposedScene
from isec.environment.base import Tilemap


class Level:
    def __init__(self,
                 level_name: str,
                 scene: ComposedScene) -> None:

        self.name = level_name
        self.scene = scene
        self.data = Resource.data["levels"][level_name]["data"]

        self.terrain_tilemap = None
        self.terrain_collision_map = None

        self.decoration_tilemaps = []

        self.tileset = Tilemap.create_tileset_from_surface(Resource.image["game"]["tileset"]["block"],
                                                           16)

        self.terrain_tilemap = Tilemap(Resource.data["game"]["levels"][level_name],
                                       self.tileset)

        self.collision_map = self.terrain_tilemap.create_collision_map([0])

    def create_terrain(self):
        pass

    def create_collision_map(self):
        pass
