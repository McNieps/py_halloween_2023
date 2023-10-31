import pygame

from typing import Union


class Tilemap:
    EMPTY_TILE = -1

    def __init__(self,
                 tilemap_array: list[list[int]],
                 tileset: Union[dict[int, pygame.Surface | None], pygame.Surface],
                 tile_size: int = None,
                 parallax_depth: float = 1) -> None:
        """
        A class that represent a tilemap.

        :param tilemap_array: A 2D array of integers that represent the tiles of the map.
        :param tileset: A dictionary of integers that represent the tiles of the map with pygame surfaces.
            The tileset can also be a pygame surface, in which case the tile_size must be specified.
        :param tile_size: The size of the tiles in pixels.
        :param parallax_depth: A float that represent the parallax depth of the tilemap.
            0 is static, 1 is normal, 2 is twice the speed of the camera, etc.
            A parallax depth > 1 will be rendered on top of the entities.
        """

        if tile_size is None:
            tile_size = self._tile_size_from_tileset(tileset)

        if isinstance(tileset, pygame.Surface):
            tileset = self.create_tileset_from_surface(tileset, tile_size)

        self.tilemap_array = tilemap_array
        self.tileset = tileset
        self.tile_size = tile_size
        self.parallax_depth = parallax_depth

        self._check_tileset_validity(self.tilemap_array, self.tileset)

    @staticmethod
    def _check_tileset_validity(tilemap_array: list[list[int]],
                                tileset: dict[int: pygame.Surface | None]) -> bool:
        """A function that check if the tileset is valid."""

        return all(tile in tileset
                   for row in tilemap_array
                   for tile in row)

    @staticmethod
    def _tile_size_from_tileset(tileset) -> int:
        """A function that return the tile size from a constructed tileset."""
        return tileset[0].get_width()

    @staticmethod
    def create_tileset_from_surface(tileset_surface: pygame.Surface,
                                    tile_size: int,
                                    tile_margin: int = 0,
                                    tile_spacing: int = 0) -> dict[int, pygame.Surface | None]:
        """
        Create a tileset from a surface.

        :param tileset_surface: A pygame surface that contain the tiles.
        :param tile_size: The size of the tiles in pixels.
        :param tile_margin: The margin between the tiles and the left edge and the top edge of the tileset surface.
        :param tile_spacing: The spacing between the tiles.
        :return:
        """

        tileset = {Tilemap.EMPTY_TILE: None}
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

    def create_collision_map(self,
                             collision_tiles: list[int]) -> list[list[bool]]:
        """
        Function that return a collision map where every tile adjacent to void tiles is True and False otherwise.

        :param collision_tiles: A list of integers that represent the tiles that are collidable.
        """

        if len(collision_tiles) == 0:
            raise ValueError("The list of collision tiles must not be empty.")

        collision_map = []

        for y, row in enumerate(self.tilemap_array):
            collision_map.append([False] * len(row))

            for x, tile in enumerate(row):
                if tile in collision_tiles:
                    collision_map[y][x] = True

        return collision_map

    @property
    def size(self):
        return len(self.tilemap_array[0]), len(self.tilemap_array)

    @property
    def width(self):
        return len(self.tilemap_array[0])

    @property
    def height(self):
        return len(self.tilemap_array)

    def __getitem__(self, item):
        return self.tilemap_array[item]
