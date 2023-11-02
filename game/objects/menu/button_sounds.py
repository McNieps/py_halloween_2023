import pygame

from isec.app import Resource
from isec.environment import EntityScene
from isec.environment.position import SimplePos
from isec.gui import Button
from isec.environment.sprite import AnimatedSprite
from isec.instance import BaseInstance


class SoundsButton(Button):
    font = None

    def __init__(self,
                 increment: bool,
                 general: bool,
                 linked_instance: BaseInstance,
                 linked_scene: EntityScene) -> None:

        self.increment = increment
        self.step = 0.1
        self.general = general
        self.position = SimplePos((125 + 150*increment, 135 + 30 * (1-general)))
        self.linked_instance = linked_instance

        base_surface = Resource.image["menu"][f"button_"].copy()
        surfaces = [base_surface,
                    pygame.surface.Surface(base_surface.get_size(), pygame.SRCALPHA)]
        surfaces[1].blit(surfaces[0], (0, 1))

        self.sprite = AnimatedSprite(surfaces, [1, 0])

        self.hovered = False

        async def down_callback() -> None:
            self.hovered = True
            self.sprite.frames_duration = [0, 1]
            self.sprite.current_frame = 1
            Resource.sound["effects"]["button_preclick"].play()

        async def pressed_callback() -> None:
            self.hovered = True
            self.sprite.frames_duration = [0, 1]
            self.sprite.current_frame = 1

        async def up_callback() -> None:
            Resource.sound["effects"]["button_click"].play()

            if self.general:
                if self.increment:
                    Resource.data["engine"]["resource"]["sound"]["master_volume"] += self.step
                    if Resource.data["engine"]["resource"]["sound"]["master_volume"] > 1:
                        Resource.data["engine"]["resource"]["sound"]["master_volume"] = 1
                else:
                    Resource.data["engine"]["resource"]["sound"]["master_volume"] -= self.step
                    if Resource.data["engine"]["resource"]["sound"]["master_volume"] < 0:
                        Resource.data["engine"]["resource"]["sound"]["master_volume"] = 0
                Resource.set_volume()

            else:
                if self.increment:
                    Resource.data["engine"]["resource"]["sound"]["music_volume"] += self.step
                    if Resource.data["engine"]["resource"]["sound"]["music_volume"] > 1:
                        Resource.data["engine"]["resource"]["sound"]["music_volume"] = 1
                else:
                    Resource.data["engine"]["resource"]["sound"]["music_volume"] -= self.step
                    if Resource.data["engine"]["resource"]["sound"]["music_volume"] < 0:
                        Resource.data["engine"]["resource"]["sound"]["music_volume"] = 0

            pygame.mixer.music.set_volume(Resource.data["engine"]["resource"]["sound"]["music_volume"] *
                                          Resource.data["engine"]["resource"]["sound"]["master_volume"])

        super().__init__(linked_instance,
                         linked_scene,
                         self.position,
                         self.sprite,
                         up_callback,
                         down_callback,
                         pressed_callback)
        self.create_surfaces()

    def update(self, delta) -> None:
        super().update(delta)

        if not self.hovered:
            self.sprite.frames_duration = [1, 0]
            self.sprite.current_frame = 0

        self.hovered = False

    def create_surfaces(self) -> None:
        if self.font is None:
            self.font = pygame.font.Font(Resource.project_assets_directory+"/font/Ernst-Regular.ttf", 15)

        for i in range(2):
            surf = self.sprite.surfaces[i]

            button_label = "general" if self.general else "music"
            button_label += " +" if self.increment else " -"
            font_surf = self.font.render(button_label,
                                         False,
                                         Resource.data["colors"][0])
            blit_rect = font_surf.get_rect()
            blit_rect.center = (surf.get_width() // 2, i+surf.get_height() // 2-2)
            surf.blit(font_surf, blit_rect)
