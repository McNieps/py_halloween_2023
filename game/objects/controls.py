import pygame
import warnings


class Controls:
    UP = pygame.K_w  # pygame.K_z
    DOWN = pygame.K_s
    LEFT = pygame.K_a  # pygame.K_q
    RIGHT = pygame.K_d
    GRAB = pygame.K_LSHIFT
    JUMP = pygame.K_SPACE
    PAUSE = pygame.K_ESCAPE

    SHOOT = pygame.BUTTON_LEFT
    ROPE = pygame.BUTTON_RIGHT

    KEY_NAMES = {vars(pygame)[key]: key for key in vars(pygame) if key.startswith("K_")}

    @classmethod
    def change_bind(cls, action, key):
        if key not in cls.KEY_NAMES:
            warnings.warn("Key not found")
            return

        if action not in vars(cls):
            raise ValueError("Action not found")

        setattr(cls, action, key)

    @classmethod
    def check_if_bound(cls, key):
        if key not in cls.KEY_NAMES:
            raise ValueError("Key not found")

        for action_name, action_key in vars(cls).items():
            if action_key == key:
                return action_name

        return None

    @classmethod
    def get_key_name(cls, key):
        if key not in cls.KEY_NAMES:
            raise ValueError("Key not found")

        return cls.KEY_NAMES[key]

    @classmethod
    def get_key(cls, action):
        action = action.upper()
        if action not in vars(cls):
            raise ValueError("Action not found")

        return getattr(cls, action)

    @classmethod
    def get_key_name_from_action(cls, action: str) -> str:
        return cls.get_key_name(cls.get_key(action))
