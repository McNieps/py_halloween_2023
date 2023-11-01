import pymunk

from isec.environment.position.pymunk_pos import PymunkShapeInfo

__all__ = ["PlayerSkeletonSI",
           "PlayerFeetSI",
           "PlayerLeftSI",
           "PlayerRightSI",
           "TerrainSI",
           "PelletSI",
           "MonsterSI",
           "MiscSI"]


_collision_masks_input = {"PLAYER": ["TERRAIN"],
                          "TERRAIN": ["*"],
                          "PELLET": ["TERRAIN"],
                          "MONSTER": ["PLAYER", "TERRAIN", "PELLET", "MONSTER"],
                          "MISC": ["MISC"]}


_collision_types = {key: i for i, key in enumerate(_collision_masks_input)}
_collision_categories = {collision_type: 2**i for i, collision_type in enumerate(_collision_types)}
_collision_masks = {}
for mask_input in _collision_masks_input:
    mask = 0
    for collision_type in _collision_masks_input[mask_input]:
        if collision_type == "*":
            mask = 0xFFFFFFFF
            break

        mask |= _collision_categories[collision_type]
    _collision_masks[mask_input] = mask


class PlayerSkeletonSI(PymunkShapeInfo):
    collision_type: int = 0
    collision_category: int = _collision_categories["PLAYER"]  # 0b_0000001
    collision_mask: int = _collision_masks["PLAYER"]  # 0b_0010000
    shape_filter: pymunk.ShapeFilter = pymunk.ShapeFilter(group=collision_type,
                                                          categories=collision_category,
                                                          mask=collision_mask)

    elasticity: float = 0
    friction: float = 0
    density: float = 0
    sensor: bool = False


class PlayerFeetSI(PymunkShapeInfo):
    collision_type: int = 1
    collision_category: int = _collision_categories["PLAYER"]  # 0b_0000001
    collision_mask: int = _collision_masks["PLAYER"]  # 0b_0010000
    shape_filter: pymunk.ShapeFilter = pymunk.ShapeFilter(group=collision_type,
                                                          categories=collision_category,
                                                          mask=collision_mask)

    elasticity: float = 0
    friction: float = 0
    density: float = 0
    sensor: bool = False


class PlayerLeftSI(PymunkShapeInfo):
    collision_type: int = 2
    collision_category: int = _collision_categories["PLAYER"]  # 0b_0000001
    collision_mask: int = _collision_masks["PLAYER"]  # 0b_0010000
    shape_filter: pymunk.ShapeFilter = pymunk.ShapeFilter(group=collision_type,
                                                          categories=collision_category,
                                                          mask=collision_mask)

    elasticity: float = 0
    friction: float = 0
    density: float = 0
    sensor: bool = False


class PlayerRightSI(PymunkShapeInfo):
    collision_type: int = 3
    collision_category: int = _collision_categories["PLAYER"]  # 0b_0000001
    collision_mask: int = _collision_masks["PLAYER"]  # 0b_0010000
    shape_filter: pymunk.ShapeFilter = pymunk.ShapeFilter(group=collision_type,
                                                          categories=collision_category,
                                                          mask=collision_mask)

    elasticity: float = 0
    friction: float = 0
    density: float = 0
    sensor: bool = False


class TerrainSI(PymunkShapeInfo):
    collision_type: int = 4
    collision_category: int = _collision_categories["TERRAIN"]
    collision_mask: int = _collision_masks["TERRAIN"]
    shape_filter: pymunk.ShapeFilter = pymunk.ShapeFilter(group=collision_type,
                                                          categories=collision_category,
                                                          mask=collision_mask)

    elasticity: float = 0
    friction: float = 0
    density: float = 0
    sensor: bool = False


class PelletSI(PymunkShapeInfo):
    collision_type: int = 5
    collision_category: int = _collision_categories["PELLET"]
    collision_mask: int = _collision_masks["PELLET"]
    shape_filter: pymunk.ShapeFilter = pymunk.ShapeFilter(group=collision_type,
                                                          categories=collision_category,
                                                          mask=collision_mask)

    elasticity: float = 0
    friction: float = 0
    density: float = 10
    sensor: bool = False


class MonsterSI(PymunkShapeInfo):
    collision_type: int = 6
    collision_category: int = _collision_categories["MONSTER"]
    collision_mask: int = _collision_masks["MONSTER"]
    shape_filter: pymunk.ShapeFilter = pymunk.ShapeFilter(group=collision_type,
                                                          categories=collision_category,
                                                          mask=collision_mask)

    elasticity: float = 0
    friction: float = 0
    density: float = 0
    sensor: bool = False


class MiscSI(PymunkShapeInfo):
    collision_type: int = 7
    collision_category: int = _collision_categories["MISC"]
    collision_mask: int = _collision_masks["MISC"]
    shape_filter: pymunk.ShapeFilter = pymunk.ShapeFilter(group=collision_type,
                                                          categories=collision_category,
                                                          mask=collision_mask)

    elasticity: float = 0
    friction: float = 0
    density: float = 0.01
    sensor: bool = False
