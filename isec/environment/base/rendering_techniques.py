import pygame
import typing

from collections.abc import Iterable


class RenderingTechniques:
    TYPING = typing.Literal["static", "rotated", "cached", "optimized_static"]

    @staticmethod
    def optimized_static(self,
                         destination: pygame.Surface,
                         destination_rect: pygame.Rect,
                         offset: Iterable,
                         _angle: float) -> None:

        self.effective_surf = self.surface
        self.effective_rect = self.rect.move(*offset)

        if not self.effective_rect.colliderect(destination_rect):
            return

        relative_destination_rect = self.effective_rect.move((-self.effective_rect[0],
                                                              -self.effective_rect[1]))
        area = self.effective_surf.get_rect().clip(relative_destination_rect)

        destination.blit(self.surface, self.effective_rect, area, special_flags=self.blit_flag)

    @staticmethod
    def static(self,
               destination: pygame.Surface,
               destination_rect: pygame.Rect,
               offset: Iterable,
               _angle: float) -> None:

        self.effective_surf = self.surface
        self.effective_rect = self.rect.move(*offset)

        if not self.effective_rect.colliderect(destination_rect):
            return

        destination.blit(self.surface, self.effective_rect, special_flags=self.blit_flag)

    @staticmethod
    def rotated(self,
                destination: pygame.Surface,
                destination_rect: pygame.Rect,
                offset: Iterable,
                angle: float) -> None:

        self.effective_surf = pygame.transform.rotate(self.surface, angle)
        self.effective_rect = self.effective_surf.get_rect()
        self.effective_rect.center = self.rect.move(*offset).center

        if not self.effective_rect.colliderect(destination_rect):
            return

        destination.blit(self.effective_surf, self.effective_rect, special_flags=self.blit_flag)

    @staticmethod
    def cached(self,
               destination: pygame.Surface,
               destination_rect: pygame.Rect,
               offset: Iterable,
               angle: float) -> None:

        self.effective_surf = self.surface[angle]
        self.effective_rect = self.effective_surf.get_rect()
        self.effective_rect.center = self.rect.move(*offset).center

        if not self.effective_rect.colliderect(destination_rect):
            return

        destination.blit(self.effective_surf, self.effective_rect, special_flags=self.blit_flag)
