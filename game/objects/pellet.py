import math
import random

from typing import Self

import pygame
import pymunk

from isec.app import Resource
from isec.environment.position import PymunkPos
from isec.environment.base import Sprite, Entity
from isec.environment.scene import EntityScene, ComposedScene
from isec.instance import BaseInstance

from game.objects.shape_info import PelletSI, TerrainSI


class Pellet(Entity):
    QUANTITY_PER_SHOT = 20
    ANGULAR_SPRAY = 20  # degrees
    VELOCITY_MEAN = 1500  # pixels per second
    VELOCITY_STD = 200  # pixels per second
    DENSITY = 0.01  # kg per pixel ** 2

    def __init__(self,
                 initial_position: tuple[float, float],
                 direction: float,
                 linked_scene: ComposedScene | EntityScene,
                 linked_instance: BaseInstance) -> None:
        """Pellet object used by the shotgun. The shotgun shoots a spray of pellets and propel the player backwards."""

        # Position related
        pellet_position = PymunkPos(body_type="DYNAMIC",
                                    space=linked_scene.space,
                                    default_shape_info=PelletSI,
                                    position=pygame.Vector2(*initial_position))

        pellet_position.add_shape(pymunk.Circle(body=pellet_position.body,
                                                radius=1))

        direction = direction + random.uniform(-self.ANGULAR_SPRAY, self.ANGULAR_SPRAY)
        speed_norm = random.gauss(self.VELOCITY_MEAN, self.VELOCITY_STD)

        pellet_position.speed = pygame.Vector2(speed_norm * math.cos(math.radians(direction)),
                                               speed_norm * math.sin(math.radians(direction)))

        pellet_position.add_to_space()

        # Sprite related
        pellet_sprite = Sprite(Resource.image["game"]["objects"]["pellet"], rendering_technique="cached")

        super().__init__(position=pellet_position,
                         sprite=pellet_sprite,
                         linked_scene=linked_scene,
                         linked_instance=linked_instance)

    def update(self,
               delta: float) -> None:
        """Update the pellet."""

        if not self.position.body.mass:
            self.destroy()
            return

        super().update(delta)

        # The pellet will always be angled in the direction of the shot
        pellet_angle = math.degrees(math.atan2(self.position.body.velocity.y, self.position.body.velocity.x))
        self.position.angle = pellet_angle

    @classmethod
    def shot_pellets(cls,
                     initial_position: tuple[float, float],
                     direction: float,
                     linked_scene: ComposedScene | EntityScene,
                     linked_instance: BaseInstance) -> list[Self]:

        pellets = []

        for _ in range(cls.QUANTITY_PER_SHOT):
            pellets.append(cls(initial_position,
                               direction,
                               linked_scene,
                               linked_instance))

        return pellets

    @classmethod
    def create_body_arbiters(cls,
                             scene: ComposedScene | EntityScene) -> None:
        """Create the arbiters for the player's body."""

        scene_space: pymunk.Space = scene.space

        t = scene_space.add_collision_handler(PelletSI.collision_type,
                                              TerrainSI.collision_type)

        def begin(arbiter: pymunk.Arbiter,
                  _space: pymunk.Space,
                  _data: dict):

            for shape in arbiter.shapes:
                if shape.collision_type == PelletSI.collision_type:
                    _space.remove(shape.body, *shape.body.shapes)
                    # shape.entity.on_contact()
            return False

        t.begin = begin
