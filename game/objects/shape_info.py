import pymunk

from isec.environment.position.pymunk_pos import PymunkShapeInfo


class PlayerSkeletonSI(PymunkShapeInfo):
    collision_type: int = 0
    collision_category: int = 0b_0000001
    collision_mask: int = 0b_0010000
    shape_filter: pymunk.ShapeFilter = pymunk.ShapeFilter(group=collision_type,
                                                          categories=collision_category,
                                                          mask=collision_mask)

    elasticity: float = 0
    friction: float = 0
    density: float = 0
    sensor: bool = False


class PlayerFeetSI(PymunkShapeInfo):
    collision_type: int = 1
    collision_category: int = 0b_0000010
    collision_mask: int = 0b_0000000
    shape_filter: pymunk.ShapeFilter = pymunk.ShapeFilter(group=collision_type,
                                                          categories=collision_category,
                                                          mask=collision_mask)

    elasticity: float = 0
    friction: float = 0
    density: float = 0
    sensor: bool = False


class PlayerLeftSI(PymunkShapeInfo):
    collision_type: int = 2
    collision_category: int = 0b_0000100
    collision_mask: int = 0b_0000000
    shape_filter: pymunk.ShapeFilter = pymunk.ShapeFilter(group=collision_type,
                                                          categories=collision_category,
                                                          mask=collision_mask)

    elasticity: float = 0
    friction: float = 0
    density: float = 0
    sensor: bool = False


class PlayerRightSI(PymunkShapeInfo):
    collision_type: int = 3
    collision_category: int = 0b_0001000
    collision_mask: int = 0b_0000000
    shape_filter: pymunk.ShapeFilter = pymunk.ShapeFilter(group=collision_type,
                                                          categories=collision_category,
                                                          mask=collision_mask)

    elasticity: float = 0
    friction: float = 0
    density: float = 0
    sensor: bool = False


class TerrainSI(PymunkShapeInfo):
    collision_type: int = 4
    collision_category: int = 0b_0010000
    collision_mask: int = 0b_0000001
    shape_filter: pymunk.ShapeFilter = pymunk.ShapeFilter(group=collision_type,
                                                          categories=collision_category,
                                                          mask=collision_mask)

    elasticity: float = 0
    friction: float = 0.5
    density: float = 0
    sensor: bool = False


class PelletSI(PymunkShapeInfo):
    collision_type: int = 5
    collision_category: int = 0b_0100000
    collision_mask: int = 0b_0000000
    shape_filter: pymunk.ShapeFilter = pymunk.ShapeFilter(group=collision_type,
                                                          categories=collision_category,
                                                          mask=collision_mask)

    elasticity: float = 0
    friction: float = 0
    density: float = 0
    sensor: bool = False


class ScarfSI(PymunkShapeInfo):
    collision_type: int = 6
    collision_category: int = 0b_1000000
    collision_mask: int = 0b_0000000
    shape_filter: pymunk.ShapeFilter = pymunk.ShapeFilter(group=collision_type,
                                                          categories=collision_category,
                                                          mask=collision_mask)

    elasticity: float = 0
    friction: float = 0
    density: float = 0
    sensor: bool = False
