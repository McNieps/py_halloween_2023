import math
import pygame
import pymunk

from isec.app import Resource
from isec.environment import Entity, Sprite
from isec.environment.position import PymunkPos
from isec.environment.scene import ComposedScene
from isec.instance import BaseInstance

from game.objects.shape_info import MiscSI


class Rope:
    ADDITIONNAL_LINKS = 4

    def __init__(self,
                 base_position: pygame.Vector2,
                 linked_entity: Entity,
                 linked_scene: ComposedScene,
                 linked_instance: BaseInstance) -> None:
        """Rope object used by the grappling hook. The grappling hook is used to swing the player."""

        self.linked_space = linked_scene.space
        self.links: list[RopeLink] = []
        self.constraints: list[pymunk.Constraint] = []
        end_position = linked_entity.position.position

        rope_length = (end_position - base_position).length()
        rope_link_count = math.ceil(rope_length / RopeLink.LINK_LENGTH)
        link_vector = (end_position - base_position).normalize()*RopeLink.LINK_LENGTH
        link_angle = -link_vector.angle_to(pygame.Vector2(1, 0))

        # Create objects
        for i in range(rope_link_count):
            link_center_pos = base_position + link_vector*(i+0.5)
            self.links.append(RopeLink(linked_scene,
                                       linked_instance,
                                       link_center_pos,
                                       link_angle))

        # Create constraints
        base_constraint = pymunk.PinJoint(self.links[0].position.body,
                                          linked_scene.space.static_body,
                                          RopeLink.LINK_BASE_OFFSET,
                                          tuple(base_position))
        base_constraint.collide_bodies = False

        self.constraints.append(base_constraint)
        linked_scene.space.add(base_constraint)

        for i in range(rope_link_count-1):
            constraint = pymunk.PinJoint(self.links[i].position.body,
                                         self.links[i+1].position.body,
                                         RopeLink.LINK_END_OFFSET,
                                         RopeLink.LINK_BASE_OFFSET)
            constraint.collide_bodies = False
            self.constraints.append(constraint)
            linked_scene.space.add(constraint)

        end_constraint = pymunk.PinJoint(self.links[-1].position.body,
                                         linked_entity.position.body,
                                         RopeLink.LINK_END_OFFSET,
                                         (0, 0))
        self.constraints.append(end_constraint)
        linked_scene.space.add(end_constraint)

    def delete(self) -> None:
        """Delete the rope."""
        self.linked_space.remove(*self.constraints)

        for link in self.links:
            link.destroy()



class RopeLink(Entity):
    LINK_LENGTH = 10
    LINK_BASE_OFFSET = (-LINK_LENGTH/2, 0)
    LINK_END_OFFSET = (LINK_LENGTH/2, 0)

    def __init__(self,
                 linked_scene: ComposedScene,
                 linked_instance: BaseInstance,
                 link_center: pygame.Vector2,
                 angle: float) -> None:

        super().__init__(position=PymunkPos(body_type="DYNAMIC",
                                            space=linked_scene.space,
                                            default_shape_info=MiscSI),
                         sprite=Sprite(Resource.image["game"]["objects"]["rope_link"],
                                       rendering_technique="cached"),
                         linked_scene=linked_scene,
                         linked_instance=linked_instance)

        self.position.position = link_center
        self.position.angle = angle
        rope_link_shape = pymunk.Segment(self.position.body,
                                         self.LINK_BASE_OFFSET,
                                         self.LINK_END_OFFSET,
                                         1)

        self.position.add_shape(rope_link_shape)
        self.position.add_to_space()
