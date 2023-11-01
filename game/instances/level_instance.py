import pygame

from isec.app import Resource
from isec.instance import BaseInstance
from isec.environment.scene import ComposedScene

from game.objects.game.player import Player, PlayerDebug  # NOQA
from game.objects.game.level import Level
from game.objects.game.pellet import Pellet
from game.objects.game.rope_range_indicator import RopeRangeIndicator
from game.objects.game.ammo_indicator import AmmoIndicator


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
        self.ammo_indicator = AmmoIndicator(self.player)

    async def setup(self):
        self.scene.space.gravity = (0, 750)   # px.s-2
        self.scene.space.damping = 0.3
        self.scene.space.iterations = 5
        self.scene.camera.position.position = pygame.Vector2(200, 150)

        Pellet.create_body_arbiters(self.scene)

    async def loop(self):
        # LoopHandler.fps_caption()

        # Smart and very efficient way to always have the player on top of the entity list
        player_index = self.scene.entities.index(self.player)
        self.scene.entities.append(self.scene.entities.pop(player_index))
        # /jk

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
