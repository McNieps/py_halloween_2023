import asyncio
import numpy
import pymunk
import pygame
import math
import time

from isec.app import App, Resource
from game.instances.menu import Menu

__all__ = [asyncio, numpy, pymunk, pygame, math, time, App, Resource, Menu]


async def main() -> None:
    App.init("game/assets/")
    await Menu().execute()


asyncio.run(main())
