import math
import typing
import pygame

from collections.abc import Iterable

from isec.objects.cached_surface import CachedSurface
from isec.environment.base.rendering_techniques import RenderingTechniques


class Sprite:
    __slots__ = ["surface",
                 "rect",
                 "max_rect",
                 "effective_surf",
                 "effective_rect",
                 "_rendering_technique",
                 "blit_flag"]

    def __init__(self,
                 surface: pygame.Surface,
                 rendering_technique: RenderingTechniques.TYPING = "static",
                 blit_flag: int = 0) -> None:

        self.surface = surface
        self.rect = self.surface.get_rect()
        self.max_rect = self.rect.copy()
        self.max_rect.width = math.ceil(self.max_rect.width * math.sqrt(2))
        self.max_rect.height = math.ceil(self.max_rect.height * math.sqrt(2))
        self.rect.center = self.max_rect.center = 0, 0

        self.effective_surf = self.surface
        self.effective_rect = self.rect

        self._rendering_technique = RenderingTechniques.static
        self.set_rendering_technique(rendering_technique)
        self.blit_flag = blit_flag

    def update(self,
               delta: float) -> None:

        pass

    def set_rendering_technique(self,
                                rendering_technique: typing.Literal["static", "rotated", "cached"]) -> None:

        if rendering_technique == "static":
            self._rendering_technique = RenderingTechniques.static

        elif rendering_technique == "rotated":
            self._rendering_technique = RenderingTechniques.rotated

        elif rendering_technique == "cached":
            if not isinstance(self.surface, CachedSurface):
                raise ValueError("Cached rendering technique requires cached surface.")
            self._rendering_technique = RenderingTechniques.cached

        elif rendering_technique == "optimized_static":
            self._rendering_technique= RenderingTechniques.optimized_static

        else:
            raise ValueError("Invalid rendering technique.")

    def render(self,
               destination: pygame.Surface,
               destination_rect: pygame.Rect,
               offset: Iterable,
               angle: float) -> None:

        self._rendering_technique(self,
                                  destination,
                                  destination_rect,
                                  offset,
                                  angle)
