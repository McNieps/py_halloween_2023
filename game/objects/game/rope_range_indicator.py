import math
import pygame

from isec.app import Resource
from isec.environment import Entity, Sprite

from game.objects.game.player import Player


class RopeRangeIndicator(Entity):
    MAX_ARC_WIDTH = 25  # degrees
    MIN_ARC_CUTOFF = 0.1  # degrees
    MAX_VISIBILITY_THRESHOLD = 15  # pixels
    VISIBILITY_RANGE_CUTOFF = 15  # pixels
    BELOW_ARC_REDUCTION = 0.5  # ratio

    def __init__(self,
                 player: Player):

        self.range = Resource.data["objects"]["player"]["UTILS"]["ROPE_MAX_LENGTH"]
        surface = pygame.Surface((self.range * 2, self.range * 2), pygame.SRCALPHA)
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
        cursor_pos = pygame.Vector2(pygame.mouse.get_pos())
        center_pos = pygame.Vector2(Resource.data["engine"]["window"]["size"]) / 2
        cursor_vec = (cursor_pos-center_pos)

        angle = cursor_vec.angle_to(pygame.Vector2(1, 0))

        distance_from_center = cursor_vec.length()
        delta_radius = abs(distance_from_center - self.range)

        self.sprite.surface.fill((0, 0, 0, 0))

        if delta_radius > self.MAX_VISIBILITY_THRESHOLD + self.VISIBILITY_RANGE_CUTOFF:
            return

        if delta_radius > self.MAX_VISIBILITY_THRESHOLD:
            multiplier = 1-((delta_radius - self.MAX_VISIBILITY_THRESHOLD)/self.VISIBILITY_RANGE_CUTOFF)
            arc_width = self.MAX_ARC_WIDTH * multiplier

        else:
            arc_width = self.MAX_ARC_WIDTH

        i = 0
        while arc_width > self.MIN_ARC_CUTOFF:
            half_arc_width = arc_width / 2
            pygame.draw.arc(self.sprite.surface,
                            Resource.data["colors"][7],
                            pygame.Rect(i, i, (self.range-i) * 2, (self.range-i) * 2),
                            math.radians(angle-half_arc_width),
                            math.radians(angle+half_arc_width),
                            1)

            i += 1
            arc_width *= self.BELOW_ARC_REDUCTION
