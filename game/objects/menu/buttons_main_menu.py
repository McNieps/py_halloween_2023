import pygame

from isec.app import Resource
from isec.gui import Button
from isec.instance import BaseInstance, LoopHandler
from isec.environment import EntityScene
from isec.environment.position import SimplePos
from isec.environment.sprite import AnimatedSprite

from game.instances.instance_level import InstanceLevel
from game.instances.instance_settings import InstanceSettings


_height_offset = -30
_width_offset = 10


class PlayButton(Button):
    def __init__(self,
                 linked_instance: BaseInstance,
                 linked_scene: EntityScene) -> None:

        self.position = SimplePos((62+_width_offset, 216+_height_offset))

        base_surface = Resource.image["menu"][f"button_play"]
        surfaces = [base_surface,
                    pygame.surface.Surface(base_surface.get_size(), pygame.SRCALPHA)]
        surfaces[1].blit(surfaces[0], (0, 1))

        self.sprite = AnimatedSprite(surfaces, [0, 1])
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

            # pygame.mixer.music.load(Resource.project_assets_directory+"sound/music/menu.ogg")
            # music_volume = (Resource.data["engine"]["resource"]["sound"]["master_volume"] *
            #                 Resource.data["engine"]["resource"]["sound"]["music_volume"])
            # pygame.mixer.music.set_volume(music_volume)
            # pygame.mixer.music.play(-1)

            await InstanceLevel().execute()

        super().__init__(linked_instance,
                         linked_scene,
                         self.position,
                         self.sprite,
                         up_callback,
                         down_callback,
                         pressed_callback)

    def update(self, delta) -> None:
        super().update(delta)

        if not self.hovered:
            self.sprite.frames_duration = [1, 0]
            self.sprite.current_frame = 0

        self.hovered = False


class OptionButton(Button):
    def __init__(self,
                 linked_instance: BaseInstance,
                 linked_scene: EntityScene) -> None:

        self.position = SimplePos((62+_width_offset, 250+_height_offset))
        base_surface = Resource.image["menu"][f"button_settings"]
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
            x = InstanceSettings()
            await x.execute()

        super().__init__(linked_instance,
                         linked_scene,
                         self.position,
                         self.sprite,
                         up_callback,
                         down_callback,
                         pressed_callback)

    def update(self, delta) -> None:
        super().update(delta)

        if not self.hovered:
            self.sprite.frames_duration = [1, 0]
            self.sprite.current_frame = 0

        self.hovered = False


class QuitButton(Button):
    def __init__(self,
                 linked_instance: BaseInstance,
                 linked_scene: EntityScene) -> None:

        self.position = SimplePos((62+_width_offset, 284+_height_offset))

        base_surface = Resource.image["menu"][f"button_quit"]
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
            LoopHandler.stop_game()

        super().__init__(linked_instance,
                         linked_scene,
                         self.position,
                         self.sprite,
                         up_callback,
                         down_callback,
                         pressed_callback)

    def update(self, delta) -> None:
        super().update(delta)

        if not self.hovered:
            self.sprite.frames_duration = [1, 0]
            self.sprite.current_frame = 0

        self.hovered = False
