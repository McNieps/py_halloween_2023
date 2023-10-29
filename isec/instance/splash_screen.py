import pygame
import time
import math
import random

from isec.instance.handlers import LoopHandler
from isec.instance.base_instance import BaseInstance


class Splash(BaseInstance):
    def __init__(self):
        super().__init__()
        self.window = pygame.display.get_surface()
        self.rect_color = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

    async def setup(self):
        return

    async def loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                LoopHandler.stop_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    LoopHandler.stop_instance(self)

                else:
                    x = Splash()
                    await x.execute()

        rect = pygame.Rect(0, 0, 40, 40)
        rect.center = (200+180*math.cos(time.time()), 150+130*math.sin(time.time()))
        self.window.fill((0, 0, 0))
        pygame.draw.rect(self.window, self.rect_color, rect)

        pygame.display.flip()
