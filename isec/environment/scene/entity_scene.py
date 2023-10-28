import pygame
import pymunk

from isec.environment.base.scene import Scene
from isec.environment.base.entity import Entity
from isec.environment.base.camera import Camera
from isec.environment.position.pymunk_pos import PymunkPos


class EntityScene(Scene):
    def __init__(self,
                 fps: int,
                 surface: pygame.Surface = None,
                 entities: list[Entity] = None,
                 camera: Camera = None) -> None:

        super().__init__(surface, camera)

        if entities is None:
            entities = []
        self.entities = entities

        self.avg_delta = 1 / fps
        self.space = pymunk.Space()

    def add_entities(self,
                     *entities) -> None:

        self.entities.extend([entity for entity in entities
                              if entity not in self.entities])

        for entity in entities:
            if isinstance(entity.position, PymunkPos):
                if entity.position.body not in self.space.bodies:
                    self.space.add(entity.position.body)
                self.space.add(*[shape for shape in entity.position.shapes if shape not in self.space.shapes])

    def remove_entities(self,
                        *entities) -> None:

        for entity in entities:
            if entity not in self.entities:
                continue

            self.entities.remove(entity)

    def remove_entities_by_name(self,
                                name) -> None:

        for entity in self.entities:
            if entity.__class__.__name__ == name:
                self.remove_entities(entity)

    def update(self,
               delta: float) -> None:

        for entity in self.entities:
            entity.update(self.avg_delta)

        for entity in reversed(self.entities):
            if entity.to_delete:
                self.entities.remove(entity)

        self.space.step(self.avg_delta)

    def render(self,
               camera: Camera = None) -> None:

        if camera is None:
            camera = self.camera

        for entity in self.entities:
            entity.render(camera.get_offset_pos(entity.position), self.surface, self.rect)
