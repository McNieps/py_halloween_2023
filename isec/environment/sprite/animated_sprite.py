import pygame

from isec.environment.base import Sprite, RenderingTechniques


class AnimatedSprite(Sprite):
    def __init__(self,
                 surfaces: list[pygame.Surface],
                 frames_duration: list[float],
                 loop: bool = True,
                 rendering_technique: RenderingTechniques.TYPING = "static",
                 blit_flag: int = 0) -> None:

        if len(surfaces) == 0:
            raise ValueError("Length of surfaces must be greater than 0.")

        if len(surfaces) != len(frames_duration):
            raise ValueError("Length of surfaces and frames_duration must be equal.")

        if not all(isinstance(duration, (int | float)) for duration in frames_duration):
            raise ValueError("All frames_duration must be int or float.")

        super().__init__(surface=surfaces[0],
                         rendering_technique=rendering_technique,
                         blit_flag=blit_flag)

        self.surfaces: list[pygame.Surface] = surfaces
        self.frames_duration: list[float] = frames_duration
        self.loop: bool = loop

        self._current_frame: int = 0
        self._current_duration: float = 0.0

    def update(self,
               delta: float) -> None:

        self._current_duration += delta
        if self._current_duration >= self.frames_duration[self._current_frame]:
            self._current_duration -= self.frames_duration[self._current_frame]
            self._current_frame += 1

            if self._current_frame >= len(self.surfaces):
                if self.loop:
                    self._current_frame = 0
                else:
                    self._current_frame = len(self.surfaces) - 1

            while self.frames_duration[self._current_frame] == 0:
                self._current_frame += 1
                if self._current_frame >= len(self.surfaces):
                    if self.loop:
                        self._current_frame = 0
                    else:
                        self._current_frame = len(self.surfaces) - 1

    def render(self,
               destination: pygame.Surface,
               destination_rect: pygame.Rect,
               offset: tuple[int, int],
               angle: float) -> None:

        self.surface = self.surfaces[self._current_frame]
        super().render(destination, destination_rect, offset, angle)
