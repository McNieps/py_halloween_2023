import pygame
import pymunk
import typing

from isec.app import Resource
from isec.instance import BaseInstance
from isec.environment import Entity, Sprite
from isec.environment.sprite import PymunkSprite
from isec.environment.position import PymunkPos
from isec.environment.scene import ComposedScene

from game.objects.game.shape_info import GhostSI, PlayerSkeletonSI

if typing.TYPE_CHECKING:
    from game.objects.game.player import Player


class Ghost(Entity):
    SPEED = 150

    def __init__(self,
                 position: pygame.Vector2,
                 player: Entity,
                 linked_scene: ComposedScene,
                 instance: BaseInstance) -> None:

        self.player = player

        self.float_pos = [position[0], position[1]]

        ghost_position = PymunkPos("KINEMATIC", linked_scene.space, GhostSI, position)

        ghost_shape = pymunk.Circle(ghost_position.body, 32)
        ghost_shape.mass = 50
        ghost_shape.density = 50
        ghost_position.add_shape(ghost_shape)
        ghost_position.add_to_space()

        ghost_sprite = Sprite(Resource.image["game"]["objects"]["ghost"], "static")

        super().__init__(ghost_position, ghost_sprite, linked_scene, instance)

    def update(self, delta: float) -> None:
        player_vec = self.player.position.position - self.float_pos

        if player_vec.length() > 0:
            speed_vec = player_vec.normalize() * self.SPEED * delta
            self.float_pos[0] += speed_vec.x
            self.float_pos[1] += speed_vec.y
            self.position.position = pygame.Vector2(self.float_pos)

    @classmethod
    def create_collision_handler(cls,
                                 space: pymunk.Space) -> None:

        t = space.add_collision_handler(PlayerSkeletonSI.collision_type,
                                        GhostSI.collision_type)

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
