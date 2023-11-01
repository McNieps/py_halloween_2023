import math
import pygame

from isec.app import Resource
from isec.environment import Entity, Sprite

from game.objects.game.player import Player


class AmmoIndicator(Entity):
    MAX_ARC_WIDTH = 25  # degrees
    MIN_ARC_CUTOFF = 0.1  # degrees
    MAX_VISIBILITY_THRESHOLD = 15  # pixels
    VISIBILITY_RANGE_CUTOFF = 15  # pixels
    BELOW_ARC_REDUCTION = 0.5  # ratio

    def __init__(self,
                 player: Player):

        surface = pygame.Surface((32, 32), pygame.SRCALPHA)
        self.pixels = [(13, 5), (14, 5), (13, 4), (14, 4), (13, 3),
                       (14, 3), (13, 3), (14, 3), (13, 1), (14, 1),
                       (17, 5), (18, 5), (17, 4), (18, 4), (17, 3),
                       (18, 3), (17, 3), (18, 3), (17, 1), (18, 1)]
        self.player = player
        super().__init__(position=self.player.position,
                         sprite=Sprite(surface, "static"),
                         linked_scene=self.player.linked_scene,
                         linked_instance=self.player.linked_instance)

    def update(self,
               delta: float) -> None:
        super().update(delta)
        self.update_surface()

    def update_surface(self):
        self.sprite.surface.fill((0, 0, 0, 0))
        for i in range(math.floor(self.player.shells*10)):
            self.sprite.surface.set_at(self.pixels[i], Resource.data["colors"][7])
