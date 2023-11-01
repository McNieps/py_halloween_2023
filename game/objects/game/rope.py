import math
import pygame
import pymunk

from isec.app import Resource
from isec.environment import Entity, Sprite
from isec.environment.position import PymunkPos
from isec.environment.scene import ComposedScene
from isec.instance import BaseInstance

from game.objects.game.shape_info import MiscSI


class Rope:
    ADDITIONNAL_LENGTH = 20

    def __init__(self,
                 start_position: pygame.Vector2,
                 linked_entity: Entity,
                 linked_scene: ComposedScene,
                 linked_instance: BaseInstance) -> None:
        """Rope object used by the grappling hook. The grappling hook is used to swing the player."""

        self.linked_entity = linked_entity
        self.linked_scene = linked_scene
        self.linked_instance = linked_instance
        self.links: list[RopeLink] = []
        self.constraints: list[pymunk.Constraint] = []

        self.start_position = start_position

        self.create_decorative_links()
        self.create_true_link()

    def create_true_link(self) -> None:
        link_vec = self.linked_entity.position.position - self.start_position
        link_length = link_vec.length()
        angle = -link_vec.angle_to(pygame.Vector2(-1, 0))

        true_link = RopeLink(self.linked_scene,
                             self.linked_instance,
                             (self.start_position + self.linked_entity.position.position)/2,
                             angle,
                             link_length,
                             show_sprite=False)

        self.links.append(true_link)

        root_constraint = pymunk.PinJoint(true_link.position.body,
                                          self.linked_scene.space.static_body,
                                          (link_length/2, 0),
                                          tuple(self.start_position))

        root_constraint.collide_bodies = False

        self.constraints.append(root_constraint)
        self.linked_scene.space.add(root_constraint)

        base_constraint = pymunk.GrooveJoint(true_link.position.body,
                                             self.linked_entity.position.body,
                                             (-link_length/2, 0),
                                             (link_length/2, 0),
                                             (0, 0))

        self.constraints.append(base_constraint)
        self.linked_scene.space.add(base_constraint)

    def create_decorative_links(self) -> None:

        end_position = self.linked_entity.position.position

        rope_length = (end_position - self.start_position).length()
        rope_link_count = math.ceil(rope_length / RopeLink.LINK_SPACING)
        link_vector = (end_position - self.start_position).normalize() * RopeLink.LINK_SPACING
        link_angle = -link_vector.angle_to(pygame.Vector2(1, 0))

        # Create objects
        for i in range(rope_link_count):
            link_center_pos = self.start_position + link_vector * (i + 0.5)
            self.links.append(RopeLink(self.linked_scene,
                                       self.linked_instance,
                                       link_center_pos,
                                       link_angle))

        # Create constraints
        base_constraint = pymunk.PinJoint(self.links[0].position.body,
                                          self.linked_scene.space.static_body,
                                          RopeLink.LINK_BASE_OFFSET,
                                          tuple(self.start_position))
        base_constraint.collide_bodies = False

        self.constraints.append(base_constraint)
        self.linked_scene.space.add(base_constraint)

        for i in range(rope_link_count - 1):
            constraint = pymunk.PinJoint(self.links[i].position.body,
                                         self.links[i + 1].position.body,
                                         RopeLink.LINK_END_OFFSET,
                                         RopeLink.LINK_BASE_OFFSET)
            constraint.collide_bodies = False
            self.constraints.append(constraint)
            self.linked_scene.space.add(constraint)

        end_constraint = pymunk.PinJoint(self.links[-1].position.body,
                                         self.linked_entity.position.body,
                                         (0, 0),
                                         (0, 0))

        self.constraints.append(end_constraint)
        self.linked_scene.space.add(end_constraint)

    def delete(self) -> None:
        """Delete the rope."""
        self.linked_scene.space.remove(*self.constraints)

        for link in self.links:
            link.destroy()


class RopeLink(Entity):
    LINK_LENGTH = 10
    LINK_SPACING = LINK_LENGTH + 0

    LINK_BASE_OFFSET = (-LINK_LENGTH/2, 0)
    LINK_END_OFFSET = (LINK_LENGTH/2, 0)

    def __init__(self,
                 linked_scene: ComposedScene,
                 linked_instance: BaseInstance,
                 link_center: pygame.Vector2,
                 angle: float,
                 link_length: float = None,
                 show_sprite: bool = True) -> None:

        sprite = Sprite(Resource.image["game"]["objects"]["rope_link"],
                        rendering_technique="cached")
        if not show_sprite:
            sprite = Sprite(pygame.Surface((0, 0), pygame.SRCALPHA),
                            rendering_technique="static")

        super().__init__(position=PymunkPos(body_type="DYNAMIC",
                                            space=linked_scene.space,
                                            default_shape_info=MiscSI),
                         sprite=sprite,
                         linked_scene=linked_scene,
                         linked_instance=linked_instance)

        base_offset = self.LINK_BASE_OFFSET
        end_offset = self.LINK_END_OFFSET
        if link_length is not None:
            base_offset = (-link_length/2, 0)
            end_offset = (link_length/2, 0)

        self.position.position = link_center
        self.position.angle = angle
        rope_link_shape = pymunk.Segment(self.position.body,
                                         base_offset,
                                         end_offset,
                                         1)

        self.position.add_shape(rope_link_shape)
        self.position.add_to_space()
        # self.sprite = PymunkSprite(self.position,"rotated")
