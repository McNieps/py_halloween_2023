import pygame

from isec.app import Resource
from isec.instance import BaseInstance, LoopHandler
from isec.environment import EntityScene

from game.objects.menu.button_understood import ButtonUnderstood


class InstanceTutorial(BaseInstance):
    TUTORIALS_DONE = []

    def __init__(self, tutorial_name: str) -> None:
        self.bg_surf = None
        self.tutorial_name = tutorial_name
        super().__init__(Resource.data["instances"]["menu"]["fps"])
        self.scene = EntityScene(Resource.data["instances"]["menu"]["fps"])
        self.sound_played = False
        blur_window = pygame.transform.box_blur(self.window, 1)
        self.window.blit(blur_window, (0, 0))

        self.scene.add_entities(ButtonUnderstood(self, self.scene))

        self.event_handler.register_keydown_callback(pygame.K_ESCAPE, self.quit_instance)

    async def setup(self):
        if self.tutorial_name not in self.TUTORIALS_DONE:
            self.TUTORIALS_DONE.append(self.tutorial_name)

        Resource.sound["effects"]["tutorial_open"].play()

    async def loop(self):
        if self.bg_surf is None:
            self.bg_surf = pygame.transform.gaussian_blur(self.window, 1)

        self.window.blit(self.bg_surf, (0, 0))

        self.window.blit(Resource.image["menu"][f"board_tutorial_{self.tutorial_name}"], (50, 37))
        self.scene.update(self.delta)
        self.scene.render()

    async def quit_instance(self) -> None:
        LoopHandler.stop_instance(self)
