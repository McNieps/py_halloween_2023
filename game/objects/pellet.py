import math
import random

from typing import Self

import pymunk

from isec.app import Resource
from isec.environment.position import PymunkPos
from isec.environment.base import Sprite, Entity, Scene
from isec.instance import BaseInstance

from game.objects.collision_types import CollisionTypes


class Pellet(Entity):
    QUANTITY_PER_SHOT = 1
    ANGULAR_SPRAY = 20  # degrees
    VELOCITY_MEAN = 2000  # pixels per second
    VELOCITY_STD = 100  # pixels per second
    DENSITY = 1  # kg per pixel ** 2

    def __init__(self,
                 initial_position: tuple[float, float],
                 direction: float,
                 linked_scene: Scene,
                 linked_instance: BaseInstance) -> None:
        """Pellet object used by the shotgun. The shotgun shoots a spray of pellets and propel the player backwards."""

        # Position related
        pellet_position = PymunkPos(position=initial_position,
                                    linked_entity=self,
                                    body_type=PymunkPos.TYPE_DYNAMIC,
                                    base_shape_density=self.DENSITY,
                                    base_shape_friction=0,
                                    base_shape_elasticity=0.5,
                                    base_shape_collision_type=CollisionTypes.PELLET)

        pellet_position.add_shape(pymunk.Circle(body=pellet_position.body,
                                                radius=1,
                                                offset=(0, 0)))

        direction = direction + random.uniform(-self.ANGULAR_SPRAY, self.ANGULAR_SPRAY)
        speed_norm = random.gauss(self.VELOCITY_MEAN, self.VELOCITY_STD)

        pellet_position.speed = (speed_norm * math.cos(math.radians(direction)),
                                 speed_norm * math.sin(math.radians(direction)))

        # Sprite related
        pellet_sprite = Sprite(Resource.image["game"]["pellet"], rendering_technique="cached")

        super().__init__(position=pellet_position,
                         sprite=pellet_sprite,
                         linked_scene=linked_scene,
                         linked_instance=linked_instance)

        for shape in self.position.body.shapes:
            print(shape.entity)

    def update(self,
               delta: float) -> None:
        """Update the pellet."""

        super().update(delta)

        # The pellet will always be angled in the direction of the shot
        pellet_angle = math.degrees(math.atan2(self.position.body.velocity.y, self.position.body.velocity.x))
        self.position.a = pellet_angle

    @classmethod
    def shot_pellets(cls,
                     initial_position: tuple[float, float],
                     direction: float,
                     linked_scene: Scene,
                     linked_instance: BaseInstance) -> list[Self]:

        pellets = []

        for _ in range(cls.QUANTITY_PER_SHOT):
            pellets.append(cls(initial_position,
                               direction,
                               linked_scene,
                               linked_instance))

        return pellets

    def on_contact(self):
        space: pymunk.Space = self.linked_scene.space  # NOQA
        space.remove(*self.position.shapes, self.position.body)
        self.destroy()

    @classmethod
    def _create_body_arbiters(cls,
                              scene: Scene) -> None:
        """Create the arbiters for the player's body."""

        scene_space: pymunk.Space = scene.space  # NOQA

        t = scene_space.add_collision_handler(CollisionTypes.PELLET,
                                              CollisionTypes.TERRAIN)

        def begin(arbiter, _space, _data):
            for shape in arbiter.shapes:
                if shape.collision_type == CollisionTypes.PELLET:
                    shape.entity.on_contact()
                    print("hello")
            return False

        t.begin = begin
