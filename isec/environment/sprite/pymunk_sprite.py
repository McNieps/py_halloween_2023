import pygame
import pymunk

from isec.environment.base import Sprite, Pos, RenderingTechniques


class PymunkSprite(Sprite):
    def __init__(self,
                 pymunk_pos: Pos,
                 rendering_technique: RenderingTechniques.TYPING = "static",
                 blit_flag: int = 0) -> None:

        if pymunk_pos.body is None:
            raise ValueError("Position must be of type PymunkPos")

        if len(pymunk_pos.shapes) == 0:
            raise ValueError("PymunkPos must have at least one shape")

        pymunk_angle = pymunk_pos.body.angle
        pymunk_pos.body.angle = 0

        for shape in pymunk_pos.shapes:
            shape.cache_bb()

        bb_min_x = min([shape.bb.left for shape in pymunk_pos.shapes])
        bb_min_y = min([shape.bb.bottom for shape in pymunk_pos.shapes])
        bb_max_x = max([shape.bb.right for shape in pymunk_pos.shapes])
        bb_max_y = max([shape.bb.top for shape in pymunk_pos.shapes])

        surface = pygame.Surface((bb_max_x - bb_min_x, bb_max_y - bb_min_y), pygame.SRCALPHA)

        for shape in pymunk_pos.shapes:
            if isinstance(shape, pymunk.Poly):
                vertices = [v+(surface.get_size()[0]/2, surface.get_size()[1]/2) for v in shape.get_vertices()]
                pygame.draw.polygon(surface,
                                    (255, 255, 255),
                                    vertices)

            else:
                raise TypeError(f"Unknown shape type: {type(shape)}. Maybe not supported yet...")

        pymunk_pos.body.angle = pymunk_angle

        #

        super().__init__(surface=surface,
                         rendering_technique=rendering_technique,
                         blit_flag=blit_flag)
