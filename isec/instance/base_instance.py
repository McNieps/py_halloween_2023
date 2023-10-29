import pygame
import asyncio

import isec.app
from isec.app.resource import Resource
from isec.instance.handlers import LoopHandler, EventHandler


class BaseInstance:
    def __init__(self,
                 fps: int = None):

        self.window = isec.app.App.window

        if fps is None:
            fps = Resource.data["instances"]["default"]["fps"]

        self.event_handler = EventHandler()
        self.event_handler.register_quit_callback(LoopHandler.stop_game)
        self.fps = fps

    async def _preloop(self):
        pygame.display.flip()
        LoopHandler.limit_and_get_delta(self.fps)
        await self.event_handler.handle_events()

    async def setup(self):
        return

    async def loop(self):
        return

    async def finish(self):
        return

    async def execute(self):
        await self.setup()
        LoopHandler.stack.append(self)

        while LoopHandler.is_running(self):
            await self._preloop()
            await self.loop()
            await asyncio.sleep(0)

        await self.finish()

    @property
    def delta(self):
        return LoopHandler.delta
