import pygame

from isec.objects.cached_surface import CachedSurface
from isec.environment.sprite.animated_sprite import AnimatedSprite


radius = 9
surface_1 = pygame.Surface((radius * 2 + 1, radius * 2 + 1))
surface_1.set_colorkey((0, 0, 0))

pygame.draw.line(surface_1, (255, 0, 0), (radius, radius), (radius * 2 + 1, radius), 1)
pygame.draw.line(surface_1, (0, 255, 0), (radius, radius), (radius, 0), 1)
pygame.draw.ellipse(surface_1, (0, 0, 255), pygame.Rect(radius - 1, radius - 1, 3, 3))

surface_2 = surface_1.copy()
pygame.draw.ellipse(surface_2, (0, 0, 255), pygame.Rect(radius - 2, radius - 2, 5, 5))
pygame.draw.ellipse(surface_2, (255, 255, 255), pygame.Rect(radius - 1, radius - 1, 3, 3))

surface_3 = surface_1.copy()
pygame.draw.ellipse(surface_3, (255, 255, 255), pygame.Rect(radius - 2, radius - 2, 5, 5))
pygame.draw.ellipse(surface_3, (0, 0, 255), pygame.Rect(radius - 1, radius - 1, 3, 3))

cache_size = 8
cached_surfaces = [CachedSurface(surface_1, cache_size),
                   CachedSurface(surface_2, cache_size),
                   CachedSurface(surface_3, cache_size)]


class DebugSprite(AnimatedSprite):
    def __init__(self) -> None:

        super().__init__(surfaces=cached_surfaces,
                         rendering_technique="cached",
                         frame_durations=[0.8, 0.1, 0.1],
                         loop=True)


if __name__ == '__main__':
    x = DebugSprite()
