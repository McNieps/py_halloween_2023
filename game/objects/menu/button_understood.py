import pygame

from isec.app import Resource
from isec.environment import EntityScene
from isec.environment.position import SimplePos
from isec.gui import Button
from isec.environment.sprite import AnimatedSprite
from isec.instance import BaseInstance, LoopHandler


class ButtonUnderstood(Button):
    def __init__(self,
                 linked_instance: BaseInstance,
                 linked_scene: EntityScene) -> None:

        self.position = SimplePos((200, 275))
        self.linked_instance = linked_instance
        base_surface = Resource.image["menu"][f"button_understood"]
        surfaces = [base_surface,
                    pygame.surface.Surface(base_surface.get_size(), pygame.SRCALPHA)]
        surfaces[1].blit(surfaces[0], (0, 1))
        self.sprite = AnimatedSprite(surfaces, [1, 0])

        self.hovered = False

        async def down_callback() -> None:
            self.hovered = True
            self.sprite.frames_duration = [0, 1]
            self.sprite.current_frame = 1
            Resource.sound["effects"]["button_preclick"].play()

        async def pressed_callback() -> None:
            self.hovered = True
            self.sprite.frames_duration = [0, 1]
            self.sprite.current_frame = 1

        async def up_callback() -> None:
            Resource.sound["effects"]["button_click"].play()
            LoopHandler.stop_instance(self.linked_instance)

        super().__init__(linked_instance,
                         linked_scene,
                         self.position,
                         self.sprite,
                         up_callback,
                         down_callback,
                         pressed_callback)

    def update(self, delta) -> None:
        super().update(delta)

        if not self.hovered:
            self.sprite.frames_duration = [1, 0]
            self.sprite.current_frame = 0

        self.hovered = False
