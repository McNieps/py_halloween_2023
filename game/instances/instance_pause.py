# ET PAS INSTANT PAUSE !!!!!!!! lol

import pygame

from isec.app import Resource
from isec.instance import BaseInstance, LoopHandler
from isec.environment import EntityScene

from game.objects.menu.buttons_pause import ResumeButton, SettingsButton, LeaveButton


class InstancePause(BaseInstance):
    def __init__(self) -> None:
        self.bg_surf = None
        super().__init__(Resource.data["instances"]["menu"]["fps"])
        self.scene = EntityScene(Resource.data["instances"]["menu"]["fps"])

        blur_window = pygame.transform.box_blur(self.window, 1)
        self.window.blit(blur_window, (0, 0))

        self.scene.add_entities(ResumeButton(self, self.scene),
                                SettingsButton(self, self.scene),
                                LeaveButton(self, self.scene))

        self.event_handler.register_keydown_callback(pygame.K_ESCAPE, self.quit_instance)

    async def loop(self):
        if self.bg_surf is None:
            self.bg_surf = pygame.transform.gaussian_blur(self.window, 1)

        self.window.blit(self.bg_surf, (0, 0))

        self.window.blit(Resource.image["menu"]["board_pause"], (25, 25))
        self.scene.update(self.delta)
        self.scene.render()

    async def quit_instance(self) -> None:
        LoopHandler.stop_instance(self)
