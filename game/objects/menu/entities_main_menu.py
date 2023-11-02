import pygame

from isec.app import Resource
from isec.environment import Entity, Sprite, EntityScene
from isec.environment.position import SimplePos
from isec.instance import BaseInstance


class EntityBackground(Entity):
    def __init__(self,
                 linked_scene: EntityScene,
                 linked_instance: BaseInstance) -> None:

        super().__init__(position=SimplePos((200, 150)),
                         sprite=Sprite(Resource.image["menu"]["background"]),
                         linked_scene=linked_scene,
                         linked_instance=linked_instance)


class EntityPillars(Entity):
    def __init__(self,
                 linked_scene: EntityScene,
                 linked_instance: BaseInstance) -> None:

        super().__init__(position=SimplePos((200, 150)),
                         sprite=Sprite(Resource.image["menu"]["pillars"]),
                         linked_scene=linked_scene,
                         linked_instance=linked_instance)

    def update(self,
               _delta: float) -> None:
        cursor_x = pygame.mouse.get_pos()[0]
        self.position.position.x = 200+cursor_x/20


class EntityArtifact(Entity):
    def __init__(self,
                 linked_scene: EntityScene,
                 linked_instance: BaseInstance) -> None:

        self.center_x = 325

        super().__init__(position=SimplePos((self.center_x, 220)),
                         sprite=Sprite(Resource.image["menu"]["artifact"]),
                         linked_scene=linked_scene,
                         linked_instance=linked_instance)

    def update(self,
               _delta: float) -> None:
        cursor_x = pygame.mouse.get_pos()[0]
        self.position.position.x = self.center_x-cursor_x/20
