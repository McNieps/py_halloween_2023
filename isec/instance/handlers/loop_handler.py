import pygame
import sys

from isec._ise_error import InvalidInstanceError


class LoopHandler:
    stack: list = []
    delta: float = 0

    _clock: pygame.time.Clock = pygame.time.Clock()

    @classmethod
    def is_running(cls,
                   instance) -> bool:

        return cls.stack[-1] == instance

    @classmethod
    def fps_caption(cls) -> None:

        pygame.display.set_caption(str(cls._clock.get_fps()))

    @classmethod
    def limit_and_get_delta(cls,
                            fps: int):

        cls.delta = cls._clock.tick(fps) / 1000
        return cls.delta

    @classmethod
    def stop_instance(cls, instance) -> None:
        cls.stack.remove(instance)
        if len(cls.stack) == 0:
            cls.stop_game()

    @classmethod
    def stop_game(cls):
        sys.exit()

    @classmethod
    def return_to_instance_id(cls, instance):
        if instance not in cls.stack:
            raise InvalidInstanceError(f"{instance} is not in the stack.")

        cls.stack = cls.stack[:cls.stack.index(instance)+1]

    @classmethod
    def return_to_instance_name(cls, instance_name: str):
        for instance in reversed(cls.stack):
            if instance.__class__.__name__ == instance_name:
                cls.return_to_instance_id(instance)
                return

        raise InvalidInstanceError(f"There is no instance in stack with name: {instance_name}")

    @classmethod
    def get_stack(cls,
                  raw: bool = False) -> list[str]:
        if raw:
            return cls.stack
        return [inst.__class__.__name__ for inst in cls.stack]
