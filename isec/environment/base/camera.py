import pygame

from collections.abc import Iterable

from isec.environment.base.pos import Pos


class Camera:
    def __init__(self,
                 position: pygame.Vector2 = None) -> None:

        self.position = Pos()
        if self.position is not None:
            self.position.position = position

    def get_offset_pos(self,
                       position: Pos) -> pygame.math.Vector2:

        return position.position - self.position.position

    def get_coordinates_from_screen(self,
                                    screen_coordinates: pygame.math.Vector2) -> pygame.math.Vector2:

        return screen_coordinates + self.position.position
