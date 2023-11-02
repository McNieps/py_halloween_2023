import pygame

from isec.app import Resource
from isec.instance import BaseInstance, LoopHandler
from isec.environment import EntityScene

from game.objects.menu.button_key_binder import KeyBinderButton
from game.objects.menu.button_return import ReturnButton


class InstanceControls(BaseInstance):
    def __init__(self) -> None:
        super().__init__(60)
        self.bg_surf = pygame.display.get_surface().copy()
        self.scene = EntityScene(60)
        self.scene.add_entities(ReturnButton(self, self.scene))

        for i, action in enumerate(["LEFT", "RIGHT", "DOWN", "JUMP"]):
            self.scene.add_entities(KeyBinderButton((270, 96+i*24),
                                                    action,
                                                    self,
                                                    self.scene))

        blur_window = pygame.transform.box_blur(self.window, 1)
        self.window.blit(blur_window, (0, 0))

        self.event_handler.register_keydown_callback(pygame.K_ESCAPE, self.quit_instance)

    async def loop(self):
        self.bg_surf = pygame.transform.gaussian_blur(self.window, 1)
        self.window.blit(self.bg_surf, (0, 0))
        self.window.blit(Resource.image["menu"]["board_controls"], (50, 37))
        self.scene.update(self.delta)
        self.scene.render()

    async def quit_instance(self) -> None:
        LoopHandler.stop_instance(self)


if __name__ == '__main__':
    import asyncio

    from isec.app import App


    async def main():
        App.init("../assets/")

        await InstanceControls().execute()

    asyncio.run(main())
