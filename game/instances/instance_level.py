import pygame

from isec.app import Resource
from isec.instance import BaseInstance, LoopHandler
from isec.environment.scene import ComposedScene

from game.instances.instance_pause import InstancePause
from game.objects.game.player import Player, PlayerDebug  # NOQA
from game.objects.game.level import Level
from game.objects.game.pellet import Pellet
from game.objects.game.rope_range_indicator import RopeRangeIndicator
from game.objects.game.ammo_indicator import AmmoIndicator


class InstanceLevel(BaseInstance):
    def __init__(self):
        super().__init__(Resource.data["instances"]["game"]["fps"])

        # Constructing the scene
        self.scene = ComposedScene(self.fps)

        self.level = Level("level_0", self.scene, self)
        self.player = Player(pygame.Vector2(200, 200),
                             self.scene,
                             self)

        self.rope_range_indicator = RopeRangeIndicator(self.player)
        self.ammo_indicator = AmmoIndicator(self.player)

        self.event_handler.register_keydown_callback(pygame.K_ESCAPE, self.pause)

    async def setup(self):
        self.scene.space.gravity = (0, 750)   # px.s-2
        self.scene.space.damping = 0.3
        self.scene.space.iterations = 5
        self.scene.camera.position.position = pygame.Vector2(200, 150)

        Pellet.create_body_arbiters(self.scene)

    async def loop(self):
        # Smart and very efficient way to always have the player on top of the entity list
        player_index = self.scene.entities.index(self.player)
        self.scene.entities.append(self.scene.entities.pop(player_index))
        # /jk

        self.window.fill(self.level.background_color)
        self.scene.update(self.delta)
        self.block_player()
        self.center_camera()
        self.scene.render()

    def center_camera(self):
        self.scene.camera.position.position = self.player.position.position - pygame.Vector2(200, 150)

        if self.scene.camera.position.x < self.level.visible_rect.left:
            self.scene.camera.position.x = self.level.visible_rect.left
        elif self.scene.camera.position.x > self.level.visible_rect.right - 400:
            self.scene.camera.position.x = self.level.visible_rect.right - 400

        if self.scene.camera.position.y < self.level.visible_rect.top:
            self.scene.camera.position.y = self.level.visible_rect.top
        elif self.scene.camera.position.y > self.level.visible_rect.bottom - 300:
            self.scene.camera.position.y = self.level.visible_rect.bottom - 300

    def block_player(self):
        if self.player.position.x < self.level.visible_rect.left+4:
            self.player.position.x = self.level.visible_rect.left+4
            print("i")
        elif self.player.position.x > self.level.visible_rect.right-4:
            self.player.position.x = self.level.visible_rect.right-4


    @staticmethod
    async def pause():
        await InstancePause().execute()


if __name__ == '__main__':
    import asyncio

    from isec.app import App


    async def main():
        App.init("../assets/")

        await InstanceLevel().execute()

    asyncio.run(main())
