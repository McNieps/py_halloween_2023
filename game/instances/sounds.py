import pygame

from isec.app import Resource
from isec.instance import BaseInstance, LoopHandler
from isec.environment import EntityScene

from game.objects.menu.sounds_button import SoundsButton
from game.objects.menu.return_button import ReturnButton


class Sounds(BaseInstance):
    font = None

    def __init__(self) -> None:
        super().__init__(60)
        self.scene = EntityScene(60)
        self.scene.add_entities(ReturnButton(self,
                                             self.scene))

        for general in [True, False]:
            for increment in [True, False]:
                self.scene.add_entities(SoundsButton(increment,
                                                     general,
                                                     self,
                                                     self.scene))

        blur_window = pygame.transform.box_blur(self.window, 1)
        self.window.blit(blur_window, (0, 0))

        self.event_handler.register_keydown_callback(pygame.K_ESCAPE, self.quit_instance)

    async def loop(self):
        self.window.blit(Resource.image["menu"]["sounds_board"], (50, 37))
        self.scene.update(self.delta)
        self.scene.render()
        self.display_volume()

    def display_volume(self):
        if self.font is None:
            self.font = pygame.font.Font(Resource.project_assets_directory+"/font/Ernst-Regular.ttf", 15)

        master_volume_str = f"{round(Resource.data['engine']['resource']['sound']['master_volume']*100)}%"
        master_volume = self.font.render(master_volume_str, False, Resource.data["color"]["list"][-3])
        master_rect = master_volume.get_rect()
        master_rect.center = (204, 135)
        self.window.blit(master_volume, master_rect)

        music_volume_str = f"{round(Resource.data['engine']['resource']['sound']['music_volume']*100)}%"
        music_volume = self.font.render(music_volume_str, False, Resource.data["color"]["list"][-3])
        music_rect = music_volume.get_rect()
        music_rect.center = (204, 165)
        self.window.blit(music_volume, music_rect)

    async def quit_instance(self) -> None:
        LoopHandler.stop_instance(self)
