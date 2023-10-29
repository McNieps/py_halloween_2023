import pygame
import pymunk
import random

from isec.environment.base import Sprite, Pos, RenderingTechniques


class PymunkSprite(Sprite):
    def __init__(self,
                 pymunk_pos: Pos,
                 rendering_technique: RenderingTechniques.TYPING = "optimized_static",
                 blit_flag: int = 0) -> None:

        if pymunk_pos.body is None:
            raise ValueError("Position must be of type PymunkPos")

        if len(pymunk_pos.shapes) == 0:
            raise ValueError("PymunkPos must have at least one shape")

        pymunk_angle = pymunk_pos.body.angle
        pymunk_pos.body.angle = 0

        for shape in pymunk_pos.shapes:
            shape.cache_bb()

        # bb_min_x = min([shape.bb.left for shape in pymunk_pos.shapes])
        # bb_min_y = min([shape.bb.bottom for shape in pymunk_pos.shapes])
        bb_max_x = max([shape.bb.right for shape in pymunk_pos.shapes])
        bb_max_y = max([shape.bb.top for shape in pymunk_pos.shapes])

        # surface = pygame.Surface((bb_max_x - bb_min_x, bb_max_y - bb_min_y), pygame.SRCALPHA)
        surface = pygame.Surface((bb_max_x*2, bb_max_y*2), pygame.SRCALPHA)

        for shape in pymunk_pos.shapes:
            if isinstance(shape, pymunk.Poly):
                shape: pymunk.Poly
                # vertices = [v+(surface.get_size()[0]/2, surface.get_size()[1]/2) for v in shape.get_vertices()]
                vertices = [v+(bb_max_x, bb_max_y) for v in shape.get_vertices()]
                pygame.draw.polygon(surface,
                                    [random.randint(0, 255) for _ in range(3)],
                                    vertices)

            elif isinstance(shape, pymunk.Segment):
                shape: pymunk.Segment
                point_a = shape.a + (bb_max_x, bb_max_y)
                point_b = shape.b + (bb_max_x, bb_max_y)
                width = int(shape.radius*2) if shape.radius > 0 else 1
                pygame.draw.line(surface,
                                 [random.randint(0, 255) for _ in range(3)],
                                 point_a,
                                 point_b,
                                 width=width)

            elif isinstance(shape, pymunk.Circle):
                shape: pymunk.Circle
                center = shape.center_of_gravity + (bb_max_x, bb_max_y)
                radius = int(shape.radius)
                pygame.draw.circle(surface,
                                   [random.randint(0, 255) for _ in range(3)],
                                   center,
                                   radius)

            else:
                raise TypeError(f"Unknown shape type: {type(shape)}. Maybe not supported yet...")

        pymunk_pos.body.angle = pymunk_angle

        super().__init__(surface=surface,
                         rendering_technique=rendering_technique,
                         blit_flag=blit_flag)
