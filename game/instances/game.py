import pygame

from isec.app import Resource
from isec.instance import BaseInstance, LoopHandler
from isec.environment import EntityScene


class Game(BaseInstance):
    def __init__(self):
        super().__init__(Resource.data["instances"]["game"]["fps"])

        # pygame.mixer.music.load(Resource.project_assets_directory + "sound/music/menu.ogg")
        # pygame.mixer.music.play(-1)
        # pygame.mixer.music.set_volume(0.25)

        self.entity_scene: EntityScene = EntityScene(self.fps)
        
