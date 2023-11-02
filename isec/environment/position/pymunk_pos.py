import math
import pygame
import pymunk

from typing import Literal, Type
from pymunk.autogeometry import march_soft, march_hard
from collections.abc import Sequence

from isec.environment.base import Pos


class PymunkShapeInfo:
    collision_type: int
    collision_category: int
    collision_mask: int
    shape_filter: pymunk.ShapeFilter

    elasticity: float
    friction: float
    density: float
    sensor: bool

    @classmethod
    def configure_shape(cls,
                        shape: pymunk.Shape) -> None:

        shape.collision_type = cls.collision_type
        shape.filter = cls.shape_filter
        shape.elasticity = cls.elasticity
        shape.friction = cls.friction
        shape.density = cls.density
        shape.sensor = cls.sensor


class BaseShapeInfo(PymunkShapeInfo):
    collision_type: int = 0
    collision_category: int = 0b_0
    collision_mask: int = 0b_0
    shape_filter: pymunk.ShapeFilter = pymunk.ShapeFilter(group=collision_type,
                                                          categories=collision_category,
                                                          mask=collision_mask)

    elasticity: float = 0.5
    friction: float = 0.5
    density: float = 0.5
    sensor: bool = False


class PymunkPos(Pos):
    _body_type_dict: dict = {"DYNAMIC": pymunk.Body.DYNAMIC,
                             "KINEMATIC": pymunk.Body.KINEMATIC,
                             "STATIC": pymunk.Body.STATIC}

    def __init__(self,
                 body_type: Literal["DYNAMIC", "KINEMATIC", "STATIC"] = "DYNAMIC",
                 space: pymunk.Space = None,
                 default_shape_info: Type[PymunkShapeInfo] = None,
                 position: pygame.Vector2 = None) -> None:

        super().__init__()

        self.space = space
        self.body = pymunk.Body(body_type=self._body_type_dict[body_type])

        self.shape_info = default_shape_info

        self.position = position if position is not None else pygame.Vector2(0, 0)

    def configure_shape(self,
                        shape: pymunk.Shape,
                        shape_info: Type[PymunkShapeInfo] = None) -> pymunk.Shape:

        if shape_info is None:
            shape_info = self.shape_info

        shape_info.configure_shape(shape)
        return shape

    def add_shape(self,
                  shape: pymunk.Shape,
                  shape_info: Type[PymunkShapeInfo] = None) -> pymunk.Shape:

        self.configure_shape(shape, shape_info)
        shape.body = self.body
        self.shapes.append(shape)

        return shape

    def add_to_space(self) -> None:
        self.space.add(self.body, *self.shapes)

    def remove_from_space(self) -> None:
        self.space.remove(self.body, *self.shapes)

    def create_rect_shape(self,
                          rect: pygame.Rect,
                          radius: float,
                          shape_info: Type[PymunkShapeInfo] = None) -> pymunk.Shape:

        shape = pymunk.Poly.create_box(self.body, rect.size, radius=radius)
        return self.add_shape(shape, shape_info)

    def create_circle_shape(self,
                            radius: float,
                            shape_info: Type[PymunkShapeInfo] = None) -> pymunk.Shape:

        if shape_info is None:
            shape_info = self.shape_info

        shape = pymunk.Circle(self.body, radius)
        return self.add_shape(shape, shape_info)

    def create_surface_shape(self,
                             surface: pygame.Surface,
                             scale: float = 1,
                             offset: Sequence[float, float] = (0, 0),
                             march_type: Literal["soft", "hard"] = "soft",
                             radius: float = -1,
                             shape_info: Type[PymunkShapeInfo] = None) -> list[pymunk.Shape]:

        if shape_info is None:
            shape_info = self.shape_info

        size = surface.get_size()
        offset = [offset[i]+size[i]/2 for i in range(2)]
        surface_bounding_box = pymunk.BB(0, 0, size[0]-1, size[1]-1)
        surface_array = pygame.surfarray.pixels3d(pygame.mask.from_surface(surface).to_surface())

        def sample_function(_point: tuple[float, float]) -> bool:
            return bool(surface_array[int(_point[0]), int(_point[1]), 0])

        # First decomposition
        if march_type == "soft":
            polygons = list(march_soft(surface_bounding_box,
                                       int(size[0]*scale),
                                       int(size[1]*scale),
                                       0,
                                       sample_function))

        elif march_type == "hard":
            polygons = list(march_hard(surface_bounding_box,
                                       int(size[0]*scale),
                                       int(size[1]*scale),
                                       0,
                                       sample_function))

        else:
            raise Exception("Invalid march type")

        for i in range(len(polygons)):
            polygon = polygons[i]
            polygons[i] = [(offset[0]+point[0], offset[1]+point[1]) for point in polygon]

        shapes = []
        for polygon in polygons:
            bad_poly = pymunk.Poly(body=None, vertices=polygon)
            bad_poly_cog = bad_poly.center_of_gravity
            t = pymunk.Transform(tx=-bad_poly_cog[0], ty=-bad_poly_cog[1])
            shapes.append(pymunk.Poly(self.body, polygon, transform=t, radius=radius))

        for shape in shapes:
            self.add_shape(shape, shape_info)

        return shapes

    @property
    def position(self) -> pygame.Vector2:
        return pygame.Vector2(math.floor(self.body.position[0]), math.floor(self.body.position[1]))

    @position.setter
    def position(self, position: pygame.Vector2) -> None:
        self.body.position = tuple(position)

    @property
    def x(self) -> float:
        return self.body.position[0]

    @x.setter
    def x(self, value: float) -> None:
        self.body.position = (value, self.body.position[1])

    @property
    def y(self) -> float:
        return self.body.position[1]

    @y.setter
    def y(self, value: float) -> None:
        self.body.position = (self.body.position[0], value)

    @property
    def speed(self) -> pygame.Vector2:
        return pygame.Vector2(self.body.velocity)

    @speed.setter
    def speed(self, speed: tuple[float, float]) -> None:
        self.body.velocity = tuple(speed)

    @property
    def angle(self) -> float:
        return -math.degrees(self.body.angle) % 360

    @angle.setter
    def angle(self, angle: float) -> None:
        self.body.angle = math.radians(angle)

    @property
    def angular_speed(self) -> float:
        return -math.radians(self.body.angular_velocity)

    @angular_speed.setter
    def angular_speed(self, angular_speed: float) -> None:
        self.body.angular_velocity = math.radians(angular_speed)

    @property
    def space(self) -> pymunk.Space | None:
        return self._space

    @space.setter
    def space(self,
              space: pymunk.Space) -> None:
        if self._space is not None:
            self._space.remove(self._body, *self._body.shapes)

        self._space = space

    @property
    def body(self) -> pymunk.Body | None:
        return self._body

    @body.setter
    def body(self,
             body: pymunk.Body) -> None:

        if self.space is not None and self.body is not None:
            self.space.remove(self.body, *self.shapes)

        self._body = body

    @property
    def shape_info(self) -> PymunkShapeInfo | None:
        return self._shape_info

    @shape_info.setter
    def shape_info(self,
                   shape_info: PymunkShapeInfo) -> None:
        self._shape_info = shape_info
