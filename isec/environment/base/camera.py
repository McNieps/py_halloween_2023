import pygame

from isec.environment.position import SimplePos


class Camera:
    def __init__(self,
                 position: pygame.Vector2 = None) -> None:

        self.position = SimplePos()
        self.position.position = position if position is not None else pygame.math.Vector2(0, 0)

    def get_offset_pos(self,
                       position: SimplePos) -> pygame.math.Vector2:

        return position.position - self.position.position

    def get_coordinates_from_screen(self,
                                    screen_coordinates: pygame.math.Vector2) -> pygame.math.Vector2:

        return screen_coordinates + self.position.position
