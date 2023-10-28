import pygame


class CachedSurface(pygame.Surface):
    def __init__(self,
                 base_surface: pygame.Surface,
                 caching_size: int) -> None:

        super().__init__(base_surface.get_size())

        self.fill((255, 0, 0))
        self.set_colorkey((255, 0, 0))

        self._caching_size = caching_size
        self._caching_step = 360 / self._caching_size
        self.surfaces = []
        self.blit(base_surface, (0, 0))

        for i in range(caching_size):
            self.surfaces.append(pygame.transform.rotate(base_surface, i * self._caching_step))

    def _get_surface_index(self,
                           angle: float) -> int:

        return round(angle % 360 / self._caching_step) % self._caching_size

    def __getitem__(self, item):
        return self.surfaces[self._get_surface_index(item)]

    def __repr__(self):
        return f'CachedSurface with {len(self.surfaces)} surfaces.\n({self.surfaces})'
