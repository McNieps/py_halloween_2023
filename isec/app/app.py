import pygame

from isec.app.resource import Resource
from isec._ise_typing import PathLike


class App:
    window: pygame.Surface = None
    window_rect: pygame.Rect = None

    @classmethod
    def init(cls,
             assets_dir: PathLike,
             default_safeguard: bool = True,
             default_only: bool = False) -> None:

        Resource.set_directory(assets_dir)
        Resource.pre_init(default_safeguard, default_only)
        App._init_pygame()
        App._create_window()
        Resource.init(default_safeguard, default_only)
        App._set_window_icon()

    @classmethod
    def _init_pygame(cls) -> None:
        pygame.mixer.pre_init(frequency=Resource.data["engine"]["resource"]["sound"]["frequency"],
                              size=Resource.data["engine"]["resource"]["sound"]["size"],
                              channels=Resource.data["engine"]["resource"]["sound"]["channels"],
                              buffer=Resource.data["engine"]["resource"]["sound"]["buffer"],
                              devicename=Resource.data["engine"]["resource"]["sound"]["devicename"])
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.set_num_channels(Resource.data["engine"]["resource"]["sound"]["max_simultaneous_sounds"])

    @classmethod
    def _create_window(cls) -> None:
        window_size = Resource.data["engine"]["window"]["size"]
        window_flag = Resource.data["engine"]["window"]["scaled"] * pygame.SCALED
        window_flag |= Resource.data["engine"]["window"]["fullscreen"] * pygame.FULLSCREEN
        cls.window = pygame.display.set_mode(window_size, window_flag)
        cls.window_rect = cls.window.get_rect()
        pygame.display.set_caption(Resource.data["engine"]["window"]["name"])

    @classmethod
    def _set_window_icon(cls) -> None:
        icon_loc = Resource.data["engine"]["window"]["icon"]
        icon = Resource.image
        for key in icon_loc:
            icon = icon[key]
        pygame.display.set_icon(icon)
