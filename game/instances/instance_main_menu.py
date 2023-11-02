import pygame

from isec.app import Resource
from isec.instance import BaseInstance, LoopHandler
from isec.environment import EntityScene

from game.objects.menu.buttons_main_menu import PlayButton, OptionButton, QuitButton
from game.objects.menu.entities_main_menu import EntityBackground, EntityPillars, EntityArtifact


class InstanceMainMenu(BaseInstance):
    def __init__(self):
        super().__init__(Resource.data["instances"]["menu"]["fps"])
        pygame.mixer.music.load(Resource.project_assets_directory + "sound/music/main_menu.ogg")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.25)

        self.scene = EntityScene(self.fps)

        self.scene.add_entities(EntityBackground(self.scene, self),
                                EntityPillars(self.scene, self),
                                EntityArtifact(self.scene, self))

        self.scene.add_entities(PlayButton(self, self.scene),
                                OptionButton(self, self.scene),
                                QuitButton(self, self.scene))

        self.event_handler.register_keydown_callback(pygame.K_ESCAPE, LoopHandler.stop_game)

    async def loop(self):
        self.window.fill(Resource.data["colors"][6])
        pygame.draw.rect(self.window, Resource.data["colors"][7], pygame.Rect(0, 0, 400, 148))
        self.scene.update(self.delta)
        self.scene.render()


if __name__ == '__main__':
    import asyncio

    from isec.app import App


    async def main():
        App.init("../assets/")

        await InstanceMainMenu().execute()

    asyncio.run(main())
