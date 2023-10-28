import pygame

from isec.environment.base.camera import Camera


class Scene:
    def __init__(self,
                 surface: pygame.Surface = None,
                 camera: Camera = None) -> None:

        if surface is None:
            surface = pygame.display.get_surface()

        if camera is None:
            camera = Camera()

        self.camera = camera
        self.surface = surface
        self.rect = self.surface.get_rect()

    def update(self,
               delta: float) -> None:
        pass

    def render(self,
               camera: Camera = None) -> None:

        pass
