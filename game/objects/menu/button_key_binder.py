import pygame

from isec.app import Resource
from isec.gui import Button
from isec.instance import BaseInstance, LoopHandler
from isec.environment import EntityScene
from isec.environment.position import SimplePos
from isec.environment.sprite import AnimatedSprite

from game.objects.controls import Controls


class KeyBinderButton(Button):
    last_key = pygame.K_a
    font = None

    def __init__(self,
                 position: tuple[int, int],
                 action_name: str,
                 linked_instance: BaseInstance,
                 linked_scene: EntityScene) -> None:

        self.action = action_name
        self.position = SimplePos(position)

        surfaces = self.create_surfaces()
        self.sprite = AnimatedSprite(surfaces, [1, 0])

        self.hovered = False

        async def down_callback() -> None:
            self.hovered = True
            self.sprite.frames_duration = [0, 1]
            self.sprite.current_frame = 1
            Resource.sound["effects"]["button_preclick"].play()

        async def pressed_callback() -> None:
            self.hovered = True
            self.sprite.frames_duration = [0, 1]
            self.sprite.current_frame = 1

        async def up_callback() -> None:
            Resource.sound["effects"]["button_click"].play()
            x = KeyBindingInstance()
            await x.execute()
            if self.last_key != pygame.K_ESCAPE:
                Controls.change_bind(self.action, self.last_key)
                self.sprite.surfaces = self.create_surfaces()

        super().__init__(linked_instance,
                         linked_scene,
                         self.position,
                         self.sprite,
                         up_callback,
                         down_callback,
                         pressed_callback)

    def create_surfaces(self) -> list[pygame.Surface]:
        if self.font is None:
            self.font = pygame.font.Font(Resource.project_assets_directory+"/font/Ernst-Regular.ttf", 15)

        surfaces = []
        for i in range(2):
            surf = pygame.Surface(Resource.image["menu"]["button_"].get_size(), pygame.SRCALPHA)
            surf.blit(Resource.image["menu"]["button_"], (0, i))
            font_surf = self.font.render(Controls.get_key_name_from_action(self.action),
                                         False,
                                         Resource.data["colors"][0])
            blit_rect = font_surf.get_rect()
            blit_rect.center = (surf.get_width() // 2, i+surf.get_height() // 2-2)
            surf.blit(font_surf, blit_rect)
            surfaces.append(surf)

        return surfaces

    def update(self, delta) -> None:
        super().update(delta)

        if not self.hovered:
            self.sprite.frames_duration = [1, 0]
            self.sprite.current_frame = 0

        self.hovered = False


class KeyBindingInstance(BaseInstance):
    def __init__(self) -> None:
        self.bg_surf = pygame.display.get_surface().copy()

        self.blit_rect = Resource.image["menu"]["board_key_confirmation"].get_rect()
        self.blit_rect.center = (Resource.data["engine"]["window"]["size"][0] // 2,
                                 Resource.data["engine"]["window"]["size"][1] // 2)
        super().__init__(60)

    async def loop(self):
        self.bg_surf = pygame.transform.gaussian_blur(self.bg_surf, 1)
        self.window.blit(self.bg_surf, (0, 0))
        self.window.blit(Resource.image["menu"]["board_key_confirmation"], self.blit_rect)
        found_key = False
        for event in self.event_handler.events:
            if event.type == pygame.KEYDOWN:
                KeyBinderButton.last_key = event.key
                found_key = True
                break

        if found_key:
            LoopHandler.stop_instance(self)
