import pygame

from isec.app import Resource
from isec.instance import BaseInstance
from isec.environment.scene import ComposedScene
from isec.environment.base import Tilemap
from isec.environment.terrain.terrain_collision import TerrainCollision

from game.objects.player import Player
from game.objects.collision_types import CollisionTypes
from game.objects.pellet import Pellet
from game.objects.level import Level


class LevelInstance(BaseInstance):
    def __init__(self):
        super().__init__(Resource.data["instances"]["game"]["fps"])

        self.scene = ComposedScene(self.fps)

        # Entities definition
        self.player = Player(pygame.Vector2(200, 200),
                             self.scene,
                             self)

        self.level = None   # TODO

        print(Resource.data["levels"]["level_1"]["data"])

        self.terrain_tilemap = Tilemap(Resource.data["game"]["levels"]["test_3"],
                                       {-1: None, 0: Resource.image["game"]["tileset"]["block"]})

        self.collision_map = self.terrain_tilemap.create_collision_map([-1])
        self.terrain_collision_entities = TerrainCollision.from_collision_map(self.collision_map,
                                                                              self.terrain_tilemap.tile_size,
                                                                              self.scene,
                                                                              self,
                                                                              collision_type=CollisionTypes.TERRAIN,
                                                                              wall_friction=1,
                                                                              wall_elasticity=0,
                                                                              show_collision=True)

        # Constructing the scene
        self.scene.add_entities(*self.terrain_collision_entities, self.player)
        self.scene.add_tilemap_scene(self.terrain_tilemap)

    async def setup(self):
        self.scene.space.gravity = (0, 500)   # px.s-2
        self.scene.space.damping = 0.3

        Pellet._create_body_arbiters(self.scene)

    async def loop(self):
        # LoopHandler.fps_caption()
        self.window.fill((120, 120, 120))
        self.scene.update(self.delta)
        self.scene.camera.position.position = self.player.position.position - pygame.Vector2(200, 150)
        self.scene.render()


if __name__ == '__main__':
    import asyncio

    from isec.app import App


    async def main():
        App.init("../assets/")

        await LevelInstance().execute()

    asyncio.run(main())
