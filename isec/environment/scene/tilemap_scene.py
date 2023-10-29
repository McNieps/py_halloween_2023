import pygame
import numpy
import math

from isec.environment.base import Tilemap
from isec.environment.base.scene import Scene
from isec.environment.base.camera import Camera


class TilemapScene(Scene):
    def __init__(self,
                 tilemap: Tilemap,
                 surface: pygame.Surface = None,
                 camera: Camera = None) -> None:

        super().__init__(surface, camera)
        self.tilemap = tilemap

    def render(self,
               camera: Camera = None) -> None:

        if camera is None:
            camera = self.camera

        tile_size = self.tilemap.tile_size   # Trying to make the code more readable. Trying because it's not working.

        camera_pos = pygame.Vector2(math.floor(camera.position.position[0]) * self.tilemap.parallax_depth,
                                    math.floor(camera.position.position[1]) * self.tilemap.parallax_depth)

        start_x = max(0, math.floor(camera_pos[0]/tile_size))
        end_x = min(math.ceil((camera_pos[0]+self.rect.width)/tile_size), self.tilemap.width)
        start_y = max(0, math.floor(camera_pos[1]/tile_size))
        end_y = min(math.ceil((camera_pos[1]+self.rect.height)/tile_size), self.tilemap.height)

        pos_x = numpy.arange(end_x) * self.tilemap.tile_size - camera_pos[0]
        pos_y = numpy.arange(end_y) * self.tilemap.tile_size - camera_pos[1]

        self.surface.fblits([(self.tilemap.tileset[self.tilemap[y][x]], (pos_x[x], pos_y[y]))
                             for x in range(start_x, end_x)
                             for y in range(start_y, end_y)
                             if self.tilemap[y][x] != -1])

        return

    def update(self,
               delta: float) -> None:
        pass
