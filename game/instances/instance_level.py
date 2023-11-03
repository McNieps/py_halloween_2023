import pygame

from isec.app import Resource
from isec.instance import BaseInstance
from isec.environment.scene import ComposedScene

from game.instances.instance_pause import InstancePause
from game.instances.instance_tutorial import InstanceTutorial
from game.objects.game.player import Player, PlayerDebug  # NOQA
from game.objects.game.level import Level
from game.objects.game.rope_range_indicator import RopeRangeIndicator
from game.objects.game.ammo_indicator import AmmoIndicator
from game.objects.game.transition import Transition
from game.objects.game.trigger import Trigger


class InstanceLevel(BaseInstance):
    def __init__(self) -> None:
        super().__init__(Resource.data["instances"]["game"]["fps"])

        self.level = Level("level_6", self)
        self.triggers: list[Trigger] = []
        self.create_triggers()
        self.scene: ComposedScene = self.level.scene

        self.transition: Transition | None = None

        self.rope_range_indicator = RopeRangeIndicator(self.level.player)
        self.ammo_indicator = AmmoIndicator(self.level.player)

        self.event_handler.register_keydown_callback(pygame.K_ESCAPE, self.pause)
        self.event_handler.register_buttondown_callback(7, self.print_loc)
        self.event_handler.register_buttondown_callback(6, self.remove_loc)

        self.list_pos = []

    async def loop(self) -> None:
        self.scene.update(self.delta)
        self.block_player()

        await self.check_triggers()
        self.check_level_change()

        self.window.fill(self.level.background_color)
        self.put_player_on_top()
        self.center_camera()
        self.scene.render()

    def center_camera(self) -> None:
        self.scene.camera.position.position = self.level.player.position.position - pygame.Vector2(200, 150)

        if self.scene.camera.position.x < self.level.visible_rect.left:
            self.scene.camera.position.x = self.level.visible_rect.left
        elif self.scene.camera.position.x > self.level.visible_rect.right - 400:
            self.scene.camera.position.x = self.level.visible_rect.right - 400

        if self.scene.camera.position.y < self.level.visible_rect.top:
            self.scene.camera.position.y = self.level.visible_rect.top
        elif self.scene.camera.position.y > self.level.visible_rect.bottom - 300:
            self.scene.camera.position.y = self.level.visible_rect.bottom - 300

    def block_player(self) -> None:
        if self.level.player.position.x < self.level.visible_rect.left+4:
            self.level.player.position.x = self.level.visible_rect.left+4
            
        elif self.level.player.position.x > self.level.visible_rect.right-4:
            self.level.player.position.x = self.level.visible_rect.right-4

        if self.level.player.position.y > self.level.visible_rect.bottom:
            self.level.player.kill()

    def change_level(self,
                     level_name: str) -> None:
        self.level.level_name = level_name
        self.transition = Transition(self.level.player.position,
                                     self.scene,
                                     self)
        return

    def check_level_change(self) -> None:
        if self.level.player.is_dead() or self.transition is not None:
            if self.transition is None:
                self.transition = Transition(self.level.player.position,
                                             self.scene,
                                             self)
                return

            elif self.transition.can_switch:
                self.level = Level(self.level.level_name, self)
                self.scene = self.level.scene
                self.rope_range_indicator = RopeRangeIndicator(self.level.player)
                self.ammo_indicator = AmmoIndicator(self.level.player)
                self.scene.add_entities(self.transition)
                self.transition.position = self.level.player.position
                self.create_triggers()
                return

            if self.transition.can_kill:
                self.transition.destroy()
                self.transition = None
                return

    async def check_triggers(self) -> None:
        for trigger in self.triggers:
            if await trigger.check(self.level.player.position.position):
                self.triggers.remove(trigger)
                break

    def create_triggers(self) -> None:
        self.triggers = []
        for trigger_dict in self.level.data["info"]["triggers"]:
            trigger_zone = pygame.Rect(trigger_dict["zone"])

            if trigger_dict["type"] == "level_change":
                trigger_cb = self.change_level
                trigger_args = trigger_dict["level_name"]
                self.triggers.append(Trigger(trigger_zone,
                                             trigger_cb,
                                             False,
                                             False,
                                             trigger_args))

            elif trigger_dict["type"] == "tutorial":
                trigger_args = trigger_dict["tutorial_name"]
                self.triggers.append(Trigger(trigger_zone,
                                             self.tutorial_trigger,
                                             True,
                                             False,
                                             self, trigger_args))

            else:
                raise ValueError(f"Unknown trigger type: {trigger_dict['type']}")

    @staticmethod
    async def tutorial_trigger(self,
                               tutorial_name: str) -> None:

        if tutorial_name not in InstanceTutorial.TUTORIALS_DONE:
            await InstanceTutorial(tutorial_name).execute()



    def put_player_on_top(self) -> None:
        if self.transition is None:
            self.scene.entities.remove(self.level.player)
            self.scene.entities.append(self.level.player)

    @staticmethod
    async def pause():
        await InstancePause().execute()

    async def remove_loc(self) -> None:
        if self.list_pos:
            self.list_pos.pop(-1)
        print(self.list_pos)

    async def print_loc(self) -> None:
        cursor_pos = pygame.mouse.get_pos()
        relative_pos = self.scene.camera.position.position+cursor_pos
        relative_pos = [int(relative_pos[0]), int(relative_pos[1])]
        self.list_pos.append(relative_pos)
        print(self.list_pos)


if __name__ == '__main__':
    import asyncio

    from isec.app import App


    async def main():
        App.init("../assets/")

        await InstanceLevel().execute()

    asyncio.run(main())
