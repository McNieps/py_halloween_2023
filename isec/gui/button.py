import typing

import pygame.mouse

from isec.app import Resource
from isec.environment import Entity, EntityScene
from isec.environment.base import Sprite, Pos
from isec.environment.position import SimplePos
from isec.instance import BaseInstance


class Button(Entity):
    def __init__(self,
                 linked_instance: BaseInstance,
                 linked_scene: EntityScene,
                 button_position: Pos = None,
                 button_sprite: Sprite = None,
                 up_callback: typing.Callable[[], typing.Coroutine] = None,
                 down_callback: typing.Callable[[], typing.Coroutine] = None,
                 pressed_callback: typing.Callable[[], typing.Coroutine] = None) -> None:

        self.linked_instance = linked_instance
        self.linked_scene = linked_scene

        if button_position is None:
            button_position = SimplePos()
        if button_sprite is None:
            button_sprite = Sprite(surface=Resource.image["stock"]["button"],
                                   rendering_technique="static")

        super().__init__(button_position, button_sprite)

        if up_callback is None:
            up_callback = self._empty_callback
        if down_callback is None:
            down_callback = self._empty_callback
        if pressed_callback is None:
            pressed_callback = self._empty_callback

        self.up_callback = up_callback
        self.down_callback = down_callback
        self.pressed_callback = pressed_callback
        self.pressed = False

        self.linked_instance.event_handler.register_buttonup_callback(1, self.mouse_up)
        self.linked_instance.event_handler.register_buttondown_callback(1, self.mouse_down)
        self.linked_instance.event_handler.register_buttonpressed_callback(1, self.mouse_pressed)

    def _check_if_mouse_over(self) -> bool:
        sprite_effective_rect = pygame.Rect(0, 0, *self.sprite.rect.size)
        sprite_effective_rect.center = self.position.position
        mouse_pos_in_scene = self.linked_scene.camera.get_coordinates_from_screen(pygame.mouse.get_pos())

        return sprite_effective_rect.collidepoint(mouse_pos_in_scene)

    async def mouse_down(self) -> None:
        if not self._check_if_mouse_over():
            return

        self.pressed = True
        await self.down_callback()

    async def mouse_up(self) -> None:
        if not self.pressed or not self._check_if_mouse_over():
            self.pressed = False
            return

        await self.up_callback()
        self.pressed = False

    async def mouse_pressed(self) -> None:
        if not self.pressed or not self._check_if_mouse_over():
            return

        await self.pressed_callback()
        return

    async def _empty_callback(self):
        return
