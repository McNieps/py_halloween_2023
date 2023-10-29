import pymunk
import pygame

from isec.instance.base_instance import BaseInstance
from isec.environment.scene import EntityScene, ComposedScene
from isec.environment.base import Entity
from isec.environment.sprite import StateSprite, PymunkSprite
from isec.environment.position import PymunkPos

from game.objects.collision_types import CollisionTypes
from game.objects.controls import Controls


class Player(Entity):
    HORIZONTAL_FORCE = 50000
    JUMP_IMPULSE = 30000
    MASS = 100

    def __init__(self,
                 position: tuple[float, float],
                 linked_instance: BaseInstance) -> None:
        """
        Create a player object.

        :param position: The player's position.
        """

        # Metadata
        self.linked_instance = linked_instance

        # Controls related
        self.user_events = self.reset_user_inputs()
        self.collision_events = self.reset_collision_events()

        # Position related
        player_position = self._create_body(position)

        # Sprite related
        # player_sprite = StateSprite.create_from_directory("game/player_anim")
        player_sprite = PymunkSprite(player_position, "rotated")
        self.add_control_callbacks()

        super().__init__(position=player_position,
                         sprite=player_sprite)

    def update(self,
               delta: float) -> None:
        """Update the player."""

        self.handle_user_inputs()
        self.reset_user_inputs()
        self.reset_collision_events()

    def handle_user_inputs(self) -> None:
        """Handle user inputs. Must be called in the update method."""

        if self.user_events["KEYPRESSED_LEFT"]:
            self.position.body.apply_force_at_local_point((-self.HORIZONTAL_FORCE, 0))
        if self.user_events["KEYPRESSED_RIGHT"]:
            self.position.body.apply_force_at_local_point((self.HORIZONTAL_FORCE, 0))
        if self.user_events["KEYDOWN_JUMP"]:
            self.position.body.apply_impulse_at_local_point((0, -self.JUMP_IMPULSE))

    def reset_user_inputs(self) -> dict[str: bool]:
        """Reset user inputs to False."""

        self.user_events = {"KEYDOWN_UP": False,
                            "KEYDOWN_DOWN": False,
                            "KEYDOWN_LEFT": False,
                            "KEYDOWN_RIGHT": False,
                            "KEYDOWN_JUMP": False,
                            "KEYPRESSED_LEFT": False,
                            "KEYPRESSED_RIGHT": False,
                            "KEYPRESSED_JUMP": False,
                            "BUTTONPRESSED_SHOOT": False,
                            "BUTTONPRESSED_ROPE": False}
        return self.user_events

    def reset_collision_events(self) -> dict[str: bool]:
        """Reset collision events to False."""

        self.collision_events = {"left_wall_touch": False,
                                 "right_wall_touch": False,
                                 "feet_touch_floor": False}

        return self.collision_events

    def add_control_callbacks(self) -> None:
        """Add all control callbacks to the instance's event_handler."""

        for cb_str in self.user_events:
            self._create_cb(self.linked_instance, cb_str)

    def _create_body(self, position: tuple[float, float]) -> PymunkPos:
        """Create the player's body."""

        player_position = PymunkPos(position=position,
                                    shape_collision_type=CollisionTypes.PLAYER,
                                    base_shape_density=None,
                                    base_shape_elasticity=0,
                                    base_shape_friction=0)

        feet_bb = pymunk.BB(top=6, bottom=8, left=-4, right=4)
        left_hand_bb = pymunk.BB(top=-4, bottom=4, left=-5, right=-3)
        right_hand_bb = pymunk.BB(top=-4, bottom=4, left=3, right=5)

        self.skeleton = player_position.create_rect_shape(pygame.Rect(-4, -8, 8, 16))
        self.feet = pymunk.Poly.create_box_bb(player_position.body, feet_bb)
        self.left_hand = pymunk.Poly.create_box_bb(player_position.body, left_hand_bb)
        self.right_hand = pymunk.Poly.create_box_bb(player_position.body, right_hand_bb)

        player_position.add_shape(self.feet, None, 0, 0)
        player_position.add_shape(self.left_hand, None, 0, 0)
        player_position.add_shape(self.right_hand, None, 0, 0)

        self.skeleton.sensor = False
        self.feet.sensor = False   # !!!! Set to False
        self.left_hand.sensor = True
        self.right_hand.sensor = True

        self.skeleton.id = "skeleton"
        self.feet.id = "feet"
        self.left_hand.id = "left_hand"
        self.right_hand.id = "right_hand"

        player_position.body.mass = self.MASS
        player_position.body.moment = float('inf')   # Block rotation

        return player_position

    def _create_body_arbiters(self):
        pass

    def _create_cb(self,
                   linked_instance: BaseInstance,
                   cb_str: str) -> None:
        """Create a callback and add it to the instance's event_handler. Must not be called directly."""

        cb_dict = {"KEYDOWN": linked_instance.event_handler.register_keydown_callback,
                   "KEYUP": linked_instance.event_handler.register_keyup_callback,
                   "KEYPRESSED": linked_instance.event_handler.register_keypressed_callback,
                   "BUTTONDOWN": linked_instance.event_handler.register_buttondown_callback,
                   "BUTTONUP": linked_instance.event_handler.register_buttonup_callback,
                   "BUTTONPRESSED": linked_instance.event_handler.register_buttonpressed_callback}

        cb_type, control_name = cb_str.split("_")

        async def cb() -> None:
            self.user_events["".join(cb_str)] = True

        cb_dict[cb_type](vars(Controls)[control_name], cb)
