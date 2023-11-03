import pygame
import random

from isec.app import Resource
from isec.instance import BaseInstance
from isec.environment.scene import ComposedScene
from isec.environment.base import Tilemap, Entity
from isec.environment.terrain.terrain_collision import TerrainCollision

from game.objects.game.player import Player
from game.objects.game.arrow import Arrow
from game.objects.game.spike import Spike
from game.objects.game.pellet import Pellet
from game.objects.game.ghost import Ghost
from game.objects.game.shape_info import TerrainSI


class Level:
    def __init__(self,
                 level_name: str,
                 instance: BaseInstance) -> None:

        self.level_name = level_name
        self._scene: ComposedScene | None = None
        self.instance = instance

        self.player: Player | None = None

        self.data = Resource.data["levels"][self.level_name]

        self.terrain_tilemap: Tilemap | None = None
        self.collision_maps: dict[str, list[list[bool]]] = {}

        self.background_color: tuple[int, int, int] = (0, 0, 0)
        self.visible_rect: pygame.Rect = pygame.Rect(0, 0, 0, 0)

        self.load_level()

    def load_level(self) -> None:
        self._scene = ComposedScene(self.instance.fps)

        self._create_world()
        self._create_entities()

        self._create_collision_handlers()

        self.visible_rect = pygame.Rect((self.terrain_tilemap.tile_size, self.terrain_tilemap.tile_size),
                                        ((self.terrain_tilemap.width-2) * self.terrain_tilemap.tile_size,
                                         (self.terrain_tilemap.height-2) * self.terrain_tilemap.tile_size))

        """
        self.player = Player(pygame.Vector2(*self.data["info"]["player_position"]),
                             self._scene,
                             self.instance)
        """

    def _create_world(self):
        self.background_color = Resource.data["colors"][self.data["info"]["world"]["color"]]

        # customizing pymunk space
        if "physics" in self.data["info"]:
            physics_dict = self.data["info"]["physics"]
            self.scene.space.gravity = physics_dict["gravity"] if "gravity" in physics_dict else (0, 750)  # px/s²
            self.scene.space.damping = physics_dict["damping"] if "damping" in physics_dict else 0.3

        else:
            self.scene.space.gravity = (0, 750)
            self.scene.space.damping = 0.3

        for layer_name in self.data["info"]["world"]:
            if layer_name == "color":
                continue

            layer_dict = self.data["info"]["world"][layer_name]
            layer_depth = layer_dict["depth"] if "depth" in layer_dict else 1

            tileset_surface = Resource.image["game"]["tileset"][layer_dict["tileset"]["name"]]
            tileset = Tilemap.create_tileset_from_surface(tileset_surface,
                                                          layer_dict["tileset"]["tile_size"],
                                                          0,
                                                          0)

            layer_tilemap = Tilemap(tilemap_array=self.data[layer_name],
                                    tileset=tileset,
                                    parallax_depth=layer_depth)
            layer_tilemap.name = layer_name

            if "solid_tiles" in layer_dict:
                self.terrain_tilemap = layer_tilemap
                self.collidable_tilemaps = layer_tilemap
                for collision_layer in layer_dict["solid_tiles"]:
                    collidable_tiles = layer_dict["solid_tiles"][collision_layer]
                    self.collision_maps[collision_layer] = layer_tilemap.create_collision_map(collidable_tiles)

            self._scene.add_tilemap_scene(layer_tilemap)

        self._add_terrain_collision_entities()

    def _create_entities(self) -> None:
        for entity_dict in self.data["info"]["entities"]:
            entity_type = entity_dict["type"]
            entity_position = entity_dict["position"] if "position" in entity_dict else pygame.Vector2(0, 0)
            entity_angle = entity_dict["angle"] if "angle" in entity_dict else 0

            if entity_type == "player":
                if self.player is not None:
                    raise ValueError(f"Level {self.level_name} already have one player entity.")

                self.player = Player(entity_position,
                                     self._scene,
                                     self.instance,
                                     self)
                self.scene.add_entities(self.player)

            elif entity_type == "arrow":
                self.scene.add_entities(Arrow(entity_position,
                                        entity_angle,
                                        self._scene,
                                        self.instance))

            elif entity_type == "spike":
                self.scene.add_entities(Spike(entity_position,
                                        entity_angle,
                                        self._scene,
                                        self.instance))

            elif entity_type == "spike_range":
                spacing = entity_dict["spacing"] if "spacing" in entity_dict else 7
                start_position = entity_dict["start_position"]
                end_position = entity_dict["end_position"]
                spike_vector = pygame.Vector2(end_position) - pygame.Vector2(start_position)
                angle = entity_dict["angle"] if "angle" in entity_dict else spike_vector.as_polar()[1]
                unit_vector = pygame.Vector2(spacing, 0).rotate(angle)
                number_of_spikes = int(spike_vector.length() / spacing)
                for i in range(number_of_spikes):
                    self.scene.add_entities(Spike(start_position + unit_vector * i,
                                            angle+random.randint(-200, 200)/10,
                                            self._scene,
                                            self.instance))

            elif entity_type == "ghost":
                entity_position = entity_dict["position"]
                self.scene.add_entities(Ghost(entity_position,
                                        self.player,
                                        self._scene,
                                        self.instance))

            else:
                raise ValueError(f"Unknown entity {entity_type} in level {self.level_name}.")

    def _create_collision_handlers(self) -> None:
        self.player.create_collision_handler(self._scene.space)
        Spike.create_collision_handler(self._scene.space)
        Ghost.create_collision_handler(self._scene.space)
        Pellet.create_body_arbiters(self._scene)

    def _add_terrain_collision_entities(self) -> None:
        if "terrain" not in self.collision_maps:
            err_msg = f"Level {self.level_name} has no terrain collision map."
            raise ValueError(err_msg)

        terrain_entities = TerrainCollision.from_collision_map(self.collision_maps["terrain"],
                                                               self.terrain_tilemap.tile_size,
                                                               self._scene,
                                                               self.instance,
                                                               shape_info=TerrainSI,
                                                               show_collisions=False)

        self._scene.add_entities(*terrain_entities)

    def _add_entities(self, *args: Entity):
        self._scene.add_entities(*args)

    @property
    def scene(self) -> ComposedScene:
        return self._scene
