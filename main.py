import asyncio
import numpy
import pymunk
import pygame
import math
import time

from isec.app import App, Resource
from game.instances.instance_main_menu import InstanceMainMenu

__all__ = [asyncio, numpy, pymunk, pygame, math, time, App, Resource]


async def main() -> None:
    App.init("game/assets/")
    await InstanceMainMenu().execute()


asyncio.run(main())
