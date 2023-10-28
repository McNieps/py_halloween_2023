import pygame
from enum import Enum


class MouseEvent(Enum):
    CLICK_LEFT = 1
    CLICK_RIGHT = 2
    CLICK_MIDDLE = 3
    WHEEL_UP = 4
    WHEEL_DOWN = 5
    CLICK_LATERAL_1 = 6
    CLICK_LATERAL_2 = 7

    @staticmethod
    def get_label(id_button: int) -> str:
        if id_button == 1:
            return "LEFT"
        if id_button == 2:
            return "MIDDLE"
        if id_button == 3:
            return "RIGHT"
        if id_button == 4:
            return "WHEEL_UP"
        if id_button == 5:
            return "WHEEL_DOWN"
        if id_button == 6:
            return "LATERAL_1"
        if id_button == 7:
            return "LATERAL_2"
        return "UNKNOWN"


class MouseState(Enum):
    PRESSED_LEFT = 1
    PRESSED_RIGHT = 2
    PRESSED_MIDDLE = 3
    PRESSED_LATERAL_1 = 4
    PRESSED_LATERAL_2 = 5

    @staticmethod
    def get_label(id_button: int) -> str:
        if id_button == 1:
            return "LEFT"
        if id_button == 2:
            return "MIDDLE"
        if id_button == 3:
            return "RIGHT"
        if id_button == 4:
            return "LATERAL_1"
        if id_button == 5:
            return "LATERAL_2"
        return "UNKNOWN"


if __name__ == '__main__':
    run = True
    window = pygame.display.set_mode((1000, 1000))

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print(MouseEvent.get_label(event.button))

        mouse_pressed = pygame.mouse.get_pressed(5)
        for i in range(5):
            if mouse_pressed[i]:
                print(MouseState.get_label(i + 1))

        window.fill((255, 0, 0))
        pygame.display.update()
