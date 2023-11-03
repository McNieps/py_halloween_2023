import pygame


class Trigger:
    def __init__(self,
                 zone_rect: pygame.Rect,
                 callback: callable,
                 trigger_async: bool = False,
                 reusable: bool = False,
                 *call_args) -> None:

        self.active = True
        self.reusable = reusable
        self.trigger_async = trigger_async

        self.rect = zone_rect
        self.callback = callback
        self.call_args = call_args

    async def check(self,
                    coords: pygame.Vector2) -> bool:
        if not self.active:
            return False

        if self.rect.collidepoint(coords):
            if self.reusable:
                self.active = False

            if self.trigger_async:
                await self.callback(*self.call_args)

            else:
                self.callback(*self.call_args)
            return True

        return False

