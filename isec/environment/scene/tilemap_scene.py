import pygame
import numpy
import math

from isec.environment.base.scene import Scene, Camera


class TilemapScene(Scene):
    EMPTY_TILE = -1

    def __init__(self,
                 tilemap: list[list[int]],
                 tileset: dict[int, pygame.Surface],
                 surface: pygame.Surface = None,
                 camera: Camera = None) -> None:

        super().__init__(surface, camera)

        self.tilemap = tilemap
        self.tilemap_size = len(tilemap[0]), len(tilemap)
        self.tileset = tileset
        self.tile_size = self.tileset[0].get_size()[0]
        self._inter_tile_distance = 0
        self.map_size_pixels = self.tilemap_size[0]*self.tile_size, self.tilemap_size[1]*self.tile_size

        if not self._check_tileset_validity():
            raise ValueError("Invalid tileset")

    def _check_tileset_validity(self) -> bool:
        return all(tile in self.tileset for row in self.tilemap for tile in row)

    @property
    def inter_tile_distance(self):
        return self._inter_tile_distance

    @inter_tile_distance.setter
    def inter_tile_distance(self, value) -> None:
        self._inter_tile_distance = value
        self.tile_size = self.tileset[0].get_size()[0] + self.inter_tile_distance
        if self.tile_size <= 0:
            self.tile_size = 1

    def render(self,
               camera: Camera = None) -> None:

        if camera is None:
            camera = self.camera

        camera_pos = pygame.Vector2(math.floor(camera.position.position[0]), math.floor(camera.position.position[1]))
        start_x = max(0, math.floor(camera_pos[0]/self.tile_size))
        end_x = min(math.ceil((camera_pos[0]+self.rect.width)/self.tile_size), self.tilemap_size[0])
        start_y = max(0, math.floor(camera_pos[1]/self.tile_size))
        end_y = min(math.ceil((camera_pos[1]+self.rect.height)/self.tile_size), self.tilemap_size[1])

        pos_x = numpy.arange(end_x)*self.tile_size - camera_pos[0]
        pos_y = numpy.arange(end_y)*self.tile_size - camera_pos[1]

        self.surface.fblits([(self.tileset[self.tilemap[y][x]], (pos_x[x], pos_y[y]))
                             for x in range(start_x, end_x)
                             for y in range(start_y, end_y)
                             if self.tilemap[y][x] != -1])

        return

    @classmethod
    def create_tileset(cls,
                       tileset_surface: pygame.Surface,
                       tile_size: int,
                       tile_margin: int = 0,
                       tile_spacing: int = 0) -> dict[int, pygame.Surface | None]:

        tileset = {cls.EMPTY_TILE: None}
        tileset_width, tileset_height = tileset_surface.get_size()

        if (tileset_surface.get_width()-tile_margin+tile_spacing) % (tile_size + tile_spacing) != 0:
            raise ValueError("Invalid tileset width")

        if (tileset_surface.get_height()-tile_margin+tile_spacing) % (tile_size + tile_spacing) != 0:
            raise ValueError("Invalid tileset height")

        nb_columns = (tileset_width-tile_margin+tile_spacing) // (tile_size + tile_spacing)
        nb_rows = (tileset_height-tile_margin+tile_spacing) // (tile_size + tile_spacing)

        for i in range(nb_rows):
            for j in range(nb_columns):
                tileset[i*nb_columns+j] = tileset_surface.subsurface(
                    pygame.Rect(tile_margin + j*(tile_size + tile_spacing),
                                tile_margin + i*(tile_size + tile_spacing),
                                tile_size,
                                tile_size))

        return tileset

    def update(self, delta):
        pass

    @classmethod
    def create_collision_map(cls,
                             tilemap: list[list[int]],
                             collision_tile: list[int]) -> list[list[bool]]:
        """Function that return a collision map where every tile adjacent to void tiles is True and False otherwise."""

        collision_map = []

        for y, row in enumerate(tilemap):
            collision_map.append([False] * len(row))

            if y == 0 or y == len(tilemap) - 1:
                collision_map[y] = [True] * len(row)
                continue

            for x, tile in enumerate(row):
                if x == 0 or x == len(row) - 1:
                    collision_map[y][x] = True
                    continue

                if tile == cls.EMPTY_TILE or tile not in collision_tile:
                    collision_map[y][x] = False
                    continue

                if any((tilemap[y-1][x] not in collision_tile,
                        tilemap[y+1][x] not in collision_tile,
                        tilemap[y][x-1] not in collision_tile,
                        tilemap[y][x+1] not in collision_tile,
                        tilemap[y-1][x-1] not in collision_tile,
                        tilemap[y-1][x+1] not in collision_tile,
                        tilemap[y+1][x-1] not in collision_tile,
                        tilemap[y+1][x+1] not in collision_tile)):

                    collision_map[y][x] = True
                else:
                    collision_map[y][x] = False

        return collision_map


if __name__ == '__main__':
    def draw_circle(_tilemap: list[list[int]],
                    x: int,
                    y: int,
                    radius: int,
                    tile: int) -> None:

        for i in range(x - radius, x + radius + 1):
            for j in range(y - radius, y + radius + 1):
                if numpy.sqrt((x - i) ** 2 + (y - j) ** 2) <= radius:
                    _tilemap[j][i] = tile

    tile_map = [[TilemapScene.EMPTY_TILE for _ in range(100)] for _ in range(100)]
    draw_circle(tile_map, 50, 50, 16, 0)
    tile_set = {0: pygame.Surface((32, 32), pygame.SRCALPHA)}
    pygame.draw.circle(tile_set[0], (255, 255, 255), (16, 16), 16)
