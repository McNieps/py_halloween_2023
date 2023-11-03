import pygame
import pymunk

from isec.app import Resource
from isec.environment.scene import ComposedScene
from isec.environment import Entity, Sprite
from isec.environment.sprite import PymunkSprite  # NOQA
from isec.environment.position import PymunkPos
from isec.instance import BaseInstance

from game.objects.game.shape_info import SpikeSI, PlayerSkeletonSI


class Spike(Entity):
    def __init__(self,
                 position: pygame.Vector2,
                 angle: float,
                 scene: ComposedScene,
                 instance: BaseInstance) -> None:

        spike_pos = PymunkPos("STATIC", scene.space, SpikeSI)
        spike_pos.position = pygame.Vector2(position)
        spike_pos.angle = angle
        spike_pos.create_surface_shape(Resource.image["game"]["objects"]["spike"])
        spike_pos.add_to_space()

        # spike_sprite = PymunkSprite(spike_pos, "rotated")
        spike_sprite = Sprite(Resource.image["game"]["objects"]["spike"], "cached")

        super().__init__(spike_pos, spike_sprite, scene, instance)

    @classmethod
    def create_collision_handler(cls,
                                 space: pymunk.Space) -> None:

        t = space.add_collision_handler(PlayerSkeletonSI.collision_type,
                                        SpikeSI.collision_type)

        def pre_solve(_arbiter: pymunk.Arbiter,
                      _space: pymunk.Space,
                      _data: dict) -> bool:

            for shape in _arbiter.shapes:
                if shape.collision_type == PlayerSkeletonSI.collision_type:
                    _space.remove(*shape.body.shapes)
                    shape.dead = True

                    return False
            return True

        t.pre_solve = pre_solve
