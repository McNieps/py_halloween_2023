import pygame

from isec.app import Resource
from isec.instance import BaseInstance
from isec.environment import Entity, Sprite, Pos
from isec.environment.scene import ComposedScene


class Transition(Entity):
    CLOSING_TIME = 0.5
    OPENING_TIME = 0.5
    CLOSING_POWER = 2
    OPENING_POWER = 0.8

    def __init__(self,
                 player_pos: Pos,
                 scene: ComposedScene,
                 instance: BaseInstance) -> None:

        self.color = Resource.data["colors"][0]

        self.current_time = 0
        self.can_switch = False
        self.switched = False
        self.can_kill = False

        sprite = Sprite(pygame.Surface((800, 600), pygame.SRCALPHA), "static")
        super().__init__(player_pos, sprite, scene, instance)

    def update(self, delta: float) -> None:
        max_circle_radius = 500

        self.current_time += delta

        if self.can_switch and not self.switched:
            self.switched = True
            self.can_switch = False

        if self.current_time > self.CLOSING_TIME and not self.switched:
            self.can_switch = True

        if self.current_time > self.CLOSING_TIME + self.OPENING_TIME and not self.can_kill:
            self.can_kill = True

        # Change surface
        if self.current_time < self.CLOSING_TIME:
            factor = 1 - (self.current_time / self.CLOSING_TIME)
            radius = max_circle_radius * factor ** self.CLOSING_POWER
            self.sprite.surface.fill(self.color)
            pygame.draw.circle(self.sprite.surface, (0, 0, 0, 0), (400, 300), int(radius))
            self.sprite.surface = pygame.transform.box_blur(self.sprite.surface, 5)

        elif self.current_time < self.CLOSING_TIME + self.OPENING_TIME:
            factor = ((self.current_time - self.OPENING_TIME) / self.OPENING_TIME)
            radius = max_circle_radius * factor ** self.OPENING_POWER
            self.sprite.surface.fill(self.color)
            pygame.draw.circle(self.sprite.surface, (0, 0, 0, 0), (400, 300), int(radius))
            self.sprite.surface = pygame.transform.box_blur(self.sprite.surface, 5)

        else:
            self.sprite.surface.fill((0, 0, 0, 0))
