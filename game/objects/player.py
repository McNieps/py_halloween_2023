import math
import pygame
import pymunk

from isec.instance.base_instance import BaseInstance
from isec.environment.base import Entity, Scene
from isec.environment.sprite import StateSprite, PymunkSprite  # NOQA Can be used for debugging
from isec.environment.position import PymunkPos

from game.objects.collision_types import CollisionTypes
from game.objects.controls import Controls
from game.objects.pellet import Pellet


class Player(Entity):
    WALK_FORCE = 75000
    AIRCONTROL_FORCE = WALK_FORCE / 3
    JUMP_IMPULSE = 25000
    JUMP_MAINTAIN_FORCE = 25000
    MASS = 100

    def __init__(self,
                 position: tuple[float, float],
                 linked_scene: Scene,
                 linked_instance: BaseInstance) -> None:
        """
        Create a player object.

        :param position: The player's position.
        """

        # Metadata
        self.linked_instance = linked_instance
        self.linked_scene = linked_scene

        # Controls related
        self.user_events = self._reset_user_inputs()
        self.collision_status = self._reset_collision_status()
        self._add_control_callbacks()

        # Position related
        player_position = self._create_body(position)
        self._create_body_arbiters()

        # Sprite related
        player_sprite = StateSprite.create_from_directory("game/player_anim")
        player_sprite.switch_state("idle")
        self.last_direction = 1
        # player_sprite = PymunkSprite(player_position, "rotated")

        super().__init__(position=player_position,
                         sprite=player_sprite,
                         linked_scene=linked_scene,
                         linked_instance=linked_instance)

    def update(self,
               delta: float) -> None:
        """Update the player."""

        self.handle_user_inputs(delta)
        self.sprite.update(delta)

        self._reset_user_inputs()
        self._reset_collision_status()

    def handle_user_inputs(self,
                           _delta: float) -> None:
        """Handle user inputs. Must be called in the update method."""

        new_direction = self.last_direction

        if self.user_events["KEYPRESSED_LEFT"]:
            new_direction = -1
            if self.collision_status["FLOORED"]:
                self.position.body.apply_force_at_local_point((-self.WALK_FORCE, 0))

            else:
                self.position.body.apply_force_at_local_point((-self.AIRCONTROL_FORCE, 0))

        if self.user_events["KEYPRESSED_RIGHT"]:
            new_direction = 1
            if self.collision_status["FLOORED"]:
                self.position.body.apply_force_at_local_point((self.WALK_FORCE, 0))

            else:
                self.position.body.apply_force_at_local_point((self.AIRCONTROL_FORCE, 0))

        if all((self.user_events["KEYPRESSED_JUMP"],
                not self.collision_status["FLOORED"],
                self.position.body.velocity.y < 0)):
            self.position.body.apply_force_at_local_point((0, -self.JUMP_MAINTAIN_FORCE))

        if self.user_events["KEYDOWN_JUMP"]:
            self.position.body.apply_impulse_at_local_point((0, -self.JUMP_IMPULSE))

        if new_direction != self.last_direction:
            self.sprite.flip()  # NOQA
            self.last_direction = new_direction

        if self.user_events["BUTTONDOWN_SHOOT"]:
            self.shoot()

    def shoot(self) -> None:
        """Shoot a pellet."""

        direction = math.degrees(math.atan2(*[pygame.mouse.get_pos()[i] - (200, 150)[i] for i in range(2)]))
        position = (self.position.position[0], self.position.position[1])

        Pellet.shot_pellets(initial_position=position,
                            direction=direction,
                            linked_scene=self.linked_scene,
                            linked_instance=self.linked_instance)

    def _reset_user_inputs(self) -> dict[str: bool]:
        """Reset user inputs to False."""

        self.user_events = {"KEYDOWN_UP": False,
                            "KEYDOWN_DOWN": False,
                            "KEYDOWN_LEFT": False,
                            "KEYDOWN_RIGHT": False,
                            "KEYDOWN_JUMP": False,
                            "KEYPRESSED_LEFT": False,
                            "KEYPRESSED_RIGHT": False,
                            "KEYPRESSED_JUMP": False,
                            "BUTTONDOWN_SHOOT": False,
                            "BUTTONDOWN_ROPE": False,
                            "BUTTONUP_ROPE": False}
        return self.user_events

    def _reset_collision_status(self) -> dict[str: bool]:
        """Reset collision events to False."""

        self.collision_status = {"CONTACT_LEFT": False,
                                 "CONTACT_RIGHT": False,
                                 "FLOORED": False}

        return self.collision_status

    def _add_control_callbacks(self) -> None:
        """Add all control callbacks to the instance's event_handler."""

        for cb_str in self.user_events:
            self._create_input_cb(self.linked_instance, cb_str)

    def _create_body(self,
                     position: tuple[float, float]) -> PymunkPos:
        """Create the player's body."""

        player_position = PymunkPos(position=position,
                                    shape_collision_type=CollisionTypes.PLAYER,
                                    base_shape_density=None,
                                    base_shape_elasticity=0,
                                    base_shape_friction=0.5)

        self.skeleton = pymunk.Segment(player_position.body, (0, -6), (0, 3), 0)
        self.feet = pymunk.Circle(player_position.body, 2, offset=(0, 3))
        self.left_hand = pymunk.Segment(player_position.body, (-2, -4), (-2, -4), 0)
        self.right_hand = pymunk.Segment(player_position.body, (2, -4), (2, -4), 0)

        player_position.add_shape(self.skeleton,
                                  collision_type=CollisionTypes.PLAYER)

        player_position.add_shape(self.feet,
                                  collision_type=CollisionTypes.PLAYER_FEET)

        player_position.add_shape(self.left_hand,
                                  collision_type=CollisionTypes.PLAYER_LEFT)

        player_position.add_shape(self.right_hand,
                                  collision_type=CollisionTypes.PLAYER_RIGHT)

        self.skeleton.sensor = False
        self.feet.sensor = True
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
        scene_space = self.linked_scene.space  # NOQA

        t = scene_space.add_collision_handler(CollisionTypes.PLAYER_FEET,
                                              CollisionTypes.TERRAIN)

        def pre_solve(arbiter: pymunk.Arbiter,
                      _space: pymunk.Space,
                      _data: dict) -> bool:

            for shape in arbiter.shapes:
                if shape.body == self.position.body:
                    self.collision_status["FLOORED"] = True
            return True

        t.pre_solve = pre_solve

        t = scene_space.add_collision_handler(CollisionTypes.PLAYER_LEFT,
                                              CollisionTypes.TERRAIN)

        def pre_solve(arbiter: pymunk.Arbiter,
                      _space: pymunk.Space,
                      _data: dict) -> bool:

            for shape in arbiter.shapes:
                if shape.body == self.position.body:
                    self.collision_status["CONTACT_LEFT"] = True
            return True

        t.pre_solve = pre_solve

        t = scene_space.add_collision_handler(CollisionTypes.PLAYER_RIGHT,
                                              CollisionTypes.TERRAIN)

        def pre_solve(arbiter: pymunk.Arbiter,
                      _space: pymunk.Space,
                      _data: dict) -> bool:

            for shape in arbiter.shapes:
                if shape.body == self.position.body:
                    self.collision_status["CONTACT_RIGHT"] = True
            return True

        t.pre_solve = pre_solve

    def _create_input_cb(self,
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
