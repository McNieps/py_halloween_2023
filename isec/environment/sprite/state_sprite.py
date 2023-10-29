import pygame

from typing import Self

from isec.app import Resource
from isec.environment.base import RenderingTechniques
from isec.environment.sprite.animated_sprite import AnimatedSprite


class StateSprite(AnimatedSprite):
    def __init__(self,
                 surfaces: list[pygame.Surface],
                 state_dictionary: dict[str: dict],
                 rendering_technique: RenderingTechniques.TYPING = "static",
                 blit_flag: int = 0) -> None:

        self.current_state = "default"
        self.states = {"default": {"frames_durations": [int(i == 0) for i in range(len(surfaces))],
                                   "loop": True},
                       }

        self.states.update(state_dictionary)

        super().__init__(surfaces,
                         self.states[self.current_state]["frames_durations"],
                         self.states[self.current_state]["loop"],
                         rendering_technique,
                         blit_flag)

    def switch_state(self,
                     state_name: str) -> None:

        if state_name not in self.states:
            err_msg = (f"{state_name} is not a valid state name. "
                       f"Only these states are available for this sprite: {list(self.states.keys())}.")
            raise IndexError(err_msg)

        self.current_state = state_name
        self.frames_duration = self.states[state_name]["frames_duration"]
        self.loop = self.states[state_name]["loop"]

    def flip(self,
             flip_x: bool = True,
             flip_y: bool = False) -> None:

        for i, surface in enumerate(self.surfaces):
            self.surfaces[i] = pygame.transform.flip(surface, flip_x, flip_y)

    @classmethod
    def create_from_directory(cls,
                              directory_path: str,
                              rendering_technique: RenderingTechniques.TYPING = "static") -> Self:

        keys = directory_path.replace("\\", "/").rstrip("/").split("/")

        surfaces_dict = Resource.image
        states_dict = Resource.data["image"]

        for key in keys:
            surfaces_dict = surfaces_dict[key]
            states_dict = states_dict[key]

        states_dict = states_dict["state"]

        surfaces = []
        states = {}

        for state in states_dict:
            for frame in states_dict[state]["frames"]:
                surfaces.append(surfaces_dict[frame["image"]])

        i = 0
        for state in states_dict:
            states[state] = {}
            states[state]["frames_duration"] = [0 for _ in range(len(surfaces))]
            states[state]["loop"] = states_dict[state]["loop"]

            for frame in states_dict[state]["frames"]:
                states[state]["frames_duration"][i] = frame["duration"]
                i += 1

        return cls(surfaces, states, rendering_technique=rendering_technique)
