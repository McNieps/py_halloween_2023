import pygame
import pymunk

from isec.app import Resource
from isec.instance import BaseInstance
from isec.environment.scene import ComposedScene
from isec.environment.base import Tilemap
from isec.environment.tile_utils.tile_collision import TileCollision

from game.objects.player import Player
from game.objects.collision_types import CollisionTypes


class LevelInstance(BaseInstance):
    def __init__(self):
        super().__init__(Resource.data["instances"]["game"]["fps"])

        self.scene = ComposedScene(self.fps)

        # Entities definition
        self.player = Player((200, 200), self)
        self.terrain_tilemap = Tilemap(Resource.data["game"]["levels"]["test_2"],
                                       {-1: None, 0: Resource.image["game"]["tileset"]["block"]})

        self.collision_map = self.terrain_tilemap.create_collision_map([-1])

        self.terrain_collision_entity = TileCollision(self.collision_map,
                                                      self.terrain_tilemap.tile_size,
                                                      collision_type=CollisionTypes.TERRAIN)

        # Constructing the scene
        self.scene.add_entities(self.player, self.terrain_collision_entity)
        self.scene.add_tilemap_scene(self.terrain_tilemap)

        self.scene.space.gravity = (0, 500)   # px.s-2
        self.scene.space.damping = 0.2

        # self.player.position.body.moment = float("inf")

        self.player.add_control_callbacks()
        self._pymunk_create_collision_cb()
        self.polygon_visible = 0
        self.polyline = self.terrain_collision_entity.build_enhanced_collision_shape()
        self.event_handler.register_buttondown_callback(pygame.BUTTON_WHEELDOWN, self._change_polygon_visible_cb)

    async def setup(self):
        # TODO CHANGE SPRITE METHOD TO FIT ALL (and raise error if not right instance)
        # self.player.sprite.switch_state("idle")  # NOQA
        pass

    async def loop(self):
        self.window.fill((120, 120, 120))
        self.scene.update(self.delta)

        self.scene.camera.position.position = self.player.position.position - pygame.Vector2(200, 150)
        self.scene.render()

        for polygon in self.polyline:
            pygame.draw.polygon(pygame.display.get_surface(),
                                (255, 0, 0),
                                polygon, 1)
        pygame.draw.polygon(pygame.display.get_surface(),
                            (255, 0, 255),
                            self.polyline[self.polygon_visible], 1)

    def _pymunk_create_collision_cb(self):
        t = self.scene.space.add_collision_handler(CollisionTypes.PLAYER, CollisionTypes.TERRAIN)

        def pre_solve(_arbiter: pymunk.Arbiter,
                      _space: pymunk.Space,
                      data: dict) -> bool:

            # _arbiter.surface_velocity = self.player.position.body.velocity + (100, 0)
            _arbiter.friction = 0.5
            for shape in _arbiter.shapes:
                if shape.collision_type == CollisionTypes.PLAYER:
                    data["player_shape"] = shape.body.position
                    pygame.draw.circle(pygame.display.get_surface(), (255, 0, 0), shape.body.position, 5)
                else:
                    data["terrain_shape"] = shape.center_of_gravity
                    pygame.draw.circle(pygame.display.get_surface(), (0, 255, 0), shape.body.position, 5)
                    pygame.draw.circle(pygame.display.get_surface(), (0, 0, 255), shape.center_of_gravity, 5)

            return True

        t.pre_solve = pre_solve

        def post_step(_arbiter, _space, _data) -> bool:
            # print(data)
            return True

        t.post_solve = post_step

    async def _change_polygon_visible_cb(self):
        self.polygon_visible = (self.polygon_visible + 1) % len(self.polyline)
        print(self.polygon_visible)


if __name__ == '__main__':
    import asyncio

    from isec.app import App


    async def main():
        App.init("../assets/")

        await LevelInstance().execute()

    asyncio.run(main())
