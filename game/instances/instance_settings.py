import pygame

from isec.app import Resource
from isec.instance import BaseInstance, LoopHandler
from isec.environment import EntityScene

from game.objects.menu.settings_buttons import ControlsButton, SoundsButton
from game.objects.menu.button_return import ReturnButton


class InstanceSettings(BaseInstance):
    def __init__(self) -> None:
        self.bg_surf = pygame.display.get_surface().copy()
        super().__init__(Resource.data["instances"]["menu"]["fps"])
        self.scene = EntityScene(Resource.data["instances"]["menu"]["fps"])
        self.scene.add_entities(ControlsButton(self, self.scene),
                                SoundsButton(self, self.scene),
                                ReturnButton(self, self.scene))

        blur_window = pygame.transform.box_blur(self.window, 1)
        self.window.blit(blur_window, (0, 0))

        self.event_handler.register_keydown_callback(pygame.K_ESCAPE, self.quit_instance)

    async def loop(self):
        self.bg_surf = pygame.transform.gaussian_blur(self.window, 1)
        self.window.blit(self.bg_surf, (0, 0))

        self.window.blit(Resource.image["menu"]["board_settings"], (50, 37))
        self.scene.update(self.delta)
        self.scene.render()

    async def quit_instance(self) -> None:
        LoopHandler.stop_instance(self)
