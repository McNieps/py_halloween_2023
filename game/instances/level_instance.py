import pygame

from isec.app import Resource
from isec.instance import BaseInstance
from isec.environment.scene import ComposedScene
from isec.objects import cast_ray

from game.objects.player import Player, PlayerDebug  # NOQA
from game.objects.level import Level
from game.objects.pellet import Pellet
from game.objects.rope_range_indicator import RopeRangeIndicator


class LevelInstance(BaseInstance):
    def __init__(self):
        super().__init__(Resource.data["instances"]["game"]["fps"])

        # Constructing the scene
        self.scene = ComposedScene(self.fps)

        self.level = Level("level_1", self.scene, self)
        self.player = Player(pygame.Vector2(200, 200),
                             self.scene,
                             self)
        self.rope_range_indicator = RopeRangeIndicator(self.player)

        # self.player_debug = PlayerDebug(self.player.position,  # NOQA
        #                                 self.scene,
        #                                 self)

    async def setup(self):
        self.scene.space.gravity = (0, 750)   # px.s-2
        self.scene.space.damping = 0.3
        self.scene.space.iterations = 5
        self.scene.camera.position.position = pygame.Vector2(200, 150)

        Pellet.create_body_arbiters(self.scene)

        print(Resource.data["colors"][1])

    async def loop(self):
        # LoopHandler.fps_caption()

        self.window.fill((24, 25, 35))
        self.scene.update(self.delta)
        self.scene.camera.position.position = self.player.position.position - pygame.Vector2(200, 150)
        self.scene.render()

        cursor_pos = pygame.Vector2(pygame.mouse.get_pos()) + self.scene.camera.position.position

if __name__ == '__main__':
    import asyncio

    from isec.app import App


    async def main():
        App.init("../assets/")

        await LevelInstance().execute()

    asyncio.run(main())
