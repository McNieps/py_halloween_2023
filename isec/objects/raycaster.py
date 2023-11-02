import math
import pygame


def cast_ray(collision_map: list[list[bool]],
             tile_size: int,
             start_position: pygame.Vector2,
             direction_vector: pygame.Vector2,
             max_distance: float = 20) -> tuple[pygame.Vector2, bool]:

    vec_ray_start = start_position / tile_size
    if direction_vector.length() == 0:
        return start_position, False

    vec_ray_dir = direction_vector.normalize()

    vec_start_cell = pygame.Vector2(math.floor(vec_ray_start[0]),
                                    math.floor(vec_ray_start[1]))

    dir_y_over_x = float('+inf') if vec_ray_dir[0] == 0 else vec_ray_dir[1] / vec_ray_dir[0]
    dir_x_over_y = float('+inf') if vec_ray_dir[1] == 0 else vec_ray_dir[0] / vec_ray_dir[1]

    vec_ray_unit_step_size = pygame.Vector2(math.sqrt(1 + dir_y_over_x ** 2), math.sqrt(1 + dir_x_over_y ** 2))
    vec_map_check = vec_start_cell.copy()

    vec_ray_length_1d = pygame.Vector2(0, 0)
    vec_step = pygame.Vector2(0, 0)

    if vec_ray_dir[0] < 0:
        vec_step[0] = -1
        vec_ray_length_1d[0] = (vec_ray_start[0] - vec_start_cell[0]) * vec_ray_unit_step_size[0]

    else:
        vec_step[0] = 1
        vec_ray_length_1d[0] = (vec_start_cell[0] + 1 - vec_ray_start[0]) * vec_ray_unit_step_size[0]

    if vec_ray_dir[1] < 0:
        vec_step[1] = -1
        vec_ray_length_1d[1] = (vec_ray_start[1] - vec_start_cell[1]) * vec_ray_unit_step_size[1]

    else:
        vec_step[1] = 1
        vec_ray_length_1d[1] = (vec_start_cell[1] + 1 - vec_ray_start[1]) * vec_ray_unit_step_size[1]

    tile_found = False
    current_distance = 0

    while not tile_found and current_distance < max_distance:
        if vec_ray_length_1d[0] < vec_ray_length_1d[1]:
            vec_map_check[0] += vec_step[0]
            current_distance = vec_ray_length_1d[0]
            vec_ray_length_1d[0] += vec_ray_unit_step_size[0]

        else:
            vec_map_check[1] += vec_step[1]
            current_distance = vec_ray_length_1d[1]
            vec_ray_length_1d[1] += vec_ray_unit_step_size[1]

        y_floor = math.floor(vec_map_check[1])
        x_floor = math.floor(vec_map_check[0])

        if any((x_floor < 1,
                y_floor < 1,
                x_floor >= len(collision_map[0]) - 1,
                y_floor >= len(collision_map) - 1)):

            tile_found = False
            current_distance = max_distance

        elif collision_map[y_floor][x_floor]:
            tile_found = True

    if current_distance > max_distance:
        current_distance = max_distance
        tile_found = False

    if not tile_found:
        current_distance = max_distance

    return (vec_ray_dir * current_distance + vec_ray_start) * tile_size, tile_found
