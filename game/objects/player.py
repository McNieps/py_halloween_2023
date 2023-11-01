import math
import pygame
import pymunk

from isec.app import Resource
from isec.instance.base_instance import BaseInstance
from isec.environment.base import Entity
from isec.environment.scene import ComposedScene
from isec.environment.sprite import StateSprite, PymunkSprite  # NOQA Can be used for debugging
from isec.environment.position import PymunkPos

from game.objects.shape_info import PlayerSkeletonSI, PlayerFeetSI, PlayerLeftSI, PlayerRightSI, TerrainSI
from game.objects.controls import Controls
from game.objects.pellet import Pellet
from game.objects.level import Level
from game.objects.rope import Rope


class PlayerDebug(Entity):
    def __init__(self,
                 player_position: PymunkPos,
                 linked_scene: ComposedScene,
                 linked_instance: BaseInstance) -> None:

        super().__init__(position=player_position,
                         sprite=PymunkSprite(player_position,
                                             color=(255, 255, 255)),
                         linked_scene=linked_scene,
                         linked_instance=linked_instance)


class Player(Entity):
    # Physics
    MASS: float | None = None

    # Movements
    FLOORED_WALK_FORCE: float | None = None
    FLOORED_WALK_MAX_SPEED: float | None = None
    FLOORED_SPEED_DAMPING: float | None = None

    AIRTIME_WALK_FORCE: float | None = None
    AIRTIME_WALK_MAX_SPEED: float | None = None
    AIRTIME_SPEED_DAMPING: float | None = None

    JUMP_BASE_FORCE: float | None = None
    JUMP_FORCE_DAMPING: float | None = None

    CLIMB_JUMP_ANGLE: float | None = None

    # Utils
    SHOTGUN_KNOCKBACK: float | None = None

    def __init__(self,
                 position: pygame.Vector2,
                 linked_scene: ComposedScene,
                 linked_instance: BaseInstance,
                 level: Level = None) -> None:
        """Create a player object."""

        # Metadata
        super().__init__(position=PymunkPos("DYNAMIC"),
                         sprite=StateSprite.create_from_directory("game/player_anim"),
                         linked_scene=linked_scene,
                         linked_instance=linked_instance)

        self._init_class_variables()

        if level is None:
            level = self.linked_instance.level  # NOQA
        self.level = level

        # Controls related
        self.user_events = None
        self._reset_user_inputs()

        self.collision_status = None
        self._reset_collision_status()

        self._add_control_callbacks()

        # Position related
        self._create_body(position)
        self._create_body_arbiters()
        self.direction = 1
        self.jump_force = 0
        self.jump_vec = pygame.Vector2(0, -1)

        # Gameplay related
        self.rope: Rope | None = None

    def update(self,
               delta: float) -> None:
        """Update the player."""

        self._handle_user_inputs()
        self.sprite.update(delta)

        print(self.collision_status)
        print(self.jump_vec)

        self._reset_user_inputs()
        self._reset_collision_status()

    def _set_direction(self, direction: int) -> None:
        if direction != self.direction:
            self.sprite.flip()
            self.direction = direction

    def _shoot(self) -> None:
        """Shoot a pellet."""

        cursor_vec = pygame.Vector2([pygame.mouse.get_pos()[i] - (200, 150)[i] for i in range(2)]).normalize()

        # Shoot
        pellet_direction = 90 - math.degrees(math.atan2(*cursor_vec))
        pellet_position = (self.position.position[0], self.position.position[1])
        Pellet.shot_pellets(initial_position=pellet_position,
                            direction=pellet_direction,
                            linked_scene=self.linked_scene,
                            linked_instance=self.linked_instance)

        # Propel player
        impulse_vec = -(cursor_vec * self.SHOTGUN_KNOCKBACK)
        self.position.body.apply_impulse_at_local_point(tuple(impulse_vec))

    def _create_rope(self) -> None:
        pass

    def _destroy_rope(self) -> None:
        pass

    def _jump(self) -> None:
        if self.collision_status["FLOORED"] == 0:
            self.jump_force = self.JUMP_BASE_FORCE
            self.jump_vec = pygame.Vector2(0, -1)
            self.collision_status["FLOORED"] = -5
            return

        if any((self.collision_status["CONTACT_LEFT"] == 0 and self.direction == -1,
                self.collision_status["CONTACT_RIGHT"] == 0 and self.direction == 1)):
            self.jump_force = self.JUMP_BASE_FORCE
            self.jump_vec = pygame.Vector2(0, -1).rotate(-self.CLIMB_JUMP_ANGLE*self.direction)
            self.collision_status["CONTACT_LEFT"] = -3
            self.collision_status["CONTACT_RIGHT"] = -3
            return

    def _maintain_jump(self) -> None:
        if self.collision_status["FLOORED"] == 0 or self.jump_force < 1:
            return

        self.jump_force *= self.JUMP_FORCE_DAMPING ** self.linked_instance.delta
        self.position.body.apply_force_at_local_point(tuple(self.jump_vec * self.jump_force))

    def _run(self) -> None:
        if self.direction == -1 and self.position.body.velocity[0] < -self.FLOORED_WALK_MAX_SPEED:
            return

        if self.direction == 1 and self.position.body.velocity[0] > self.FLOORED_WALK_MAX_SPEED:
            return

        self.position.body.apply_force_at_local_point((self.FLOORED_WALK_FORCE * self.direction, 0))

        self.sprite.switch_state("run")

    def _climb(self) -> None:
        self.position.body.velocity = (0, 0)
        self.sprite.switch_state("climb")

    def _air_control(self) -> None:
        self.position.body.apply_force_at_local_point((self.direction * self.AIRTIME_WALK_FORCE, 0))

    def _idle(self) -> None:
        self.sprite.switch_state("idle")

    def _speed_damping(self) -> None:
        if self.collision_status["FLOORED"] == 0:
            self.position.body.velocity *= self.FLOORED_SPEED_DAMPING ** self.linked_instance.delta

        else:
            self.position.body.velocity *= self.AIRTIME_SPEED_DAMPING ** self.linked_instance.delta

    def _handle_user_inputs(self):
        if self.user_events["BUTTONDOWN_SHOOT"]:
            self._shoot()

        if self.user_events["BUTTONDOWN_ROPE"]:
            self._create_rope()

        if self.user_events["BUTTONUP_ROPE"] and self.rope is not None:
            self._destroy_rope()

        if self.user_events["KEYDOWN_JUMP"]:
            self._jump()

        if self.user_events["KEYPRESSED_JUMP"]:
            self._maintain_jump()

        if self.user_events["KEYPRESSED_LEFT"] or self.user_events["KEYPRESSED_RIGHT"]:
            self._set_direction(-1 if self.user_events["KEYPRESSED_LEFT"] else 1)

            if self.collision_status["FLOORED"] == 0:
                self._run()
                return

            if (any((self.collision_status["CONTACT_LEFT"] == 0 and self.direction == -1,
                    self.collision_status["CONTACT_RIGHT"] == 0 and self.direction == 1))
                    and self.position.body.velocity[1] > 0):
                self._climb()
                return

            self._air_control()
            return

        else:
            self._speed_damping()

        self._idle()

    def _reset_user_inputs(self) -> dict[str: bool]:
        """Reset user inputs to False."""

        self.user_events = {"KEYDOWN_UP": False,
                            "KEYDOWN_DOWN": False,
                            "KEYDOWN_LEFT": False,
                            "KEYPRESSED_LEFT": False,
                            "KEYDOWN_RIGHT": False,
                            "KEYPRESSED_RIGHT": False,
                            "KEYDOWN_JUMP": False,
                            "KEYPRESSED_JUMP": False,
                            "BUTTONDOWN_SHOOT": False,
                            "BUTTONDOWN_ROPE": False,
                            "BUTTONUP_ROPE": False}
        return self.user_events

    def _reset_collision_status(self) -> dict[str: bool]:
        """Reset collision events to False."""
        if self.collision_status is None:
            self.collision_status = {"CONTACT_LEFT": 999,
                                     "CONTACT_RIGHT": 999,
                                     "FLOORED": 999}

            return self.collision_status

        for collision in self.collision_status:
            self.collision_status[collision] += 1

        return self.collision_status

    def _add_control_callbacks(self) -> None:
        """Add all control callbacks to the instance's event_handler."""

        for cb_str in self.user_events:
            self._create_input_cb(self.linked_instance, cb_str)

    def _create_body(self,
                     position: pygame.Vector2) -> None:
        """Create the player's body."""

        self.position.shape_info = PlayerSkeletonSI
        self.position.position = position
        self.position.space = self.linked_scene.space

        self.skeleton = pymunk.Segment(self.position.body, (0, -6), (0, 3), 1)
        self.feet = pymunk.Circle(self.position.body, 1, offset=(0, 3))
        self.left_hand = pymunk.Segment(self.position.body, (-3, -4), (0, -4), 0)
        self.right_hand = pymunk.Segment(self.position.body, (0, -4), (3, -4), 0)

        self.position.add_shape(shape=self.skeleton, shape_info=PlayerSkeletonSI)
        self.position.add_shape(shape=self.feet, shape_info=PlayerFeetSI)
        self.position.add_shape(shape=self.left_hand, shape_info=PlayerLeftSI)
        self.position.add_shape(shape=self.right_hand, shape_info=PlayerRightSI)

        self.position.add_to_space()
        self.position.body.mass = self.MASS
        self.position.body.moment = float('inf')   # Block rotation

    def _create_body_arbiters(self):
        scene_space = self.linked_scene.space

        t = scene_space.add_collision_handler(PlayerFeetSI.collision_type,
                                              TerrainSI.collision_type)

        def pre_solve(_arbiter: pymunk.Arbiter,
                      _space: pymunk.Space,
                      _data: dict) -> bool:

            if self.collision_status["FLOORED"] > 0:
                self.collision_status["FLOORED"] = 0
            return True

        t.pre_solve = pre_solve

        t = scene_space.add_collision_handler(PlayerLeftSI.collision_type,
                                              TerrainSI.collision_type)

        def pre_solve(_arbiter: pymunk.Arbiter,
                      _space: pymunk.Space,
                      _data: dict) -> bool:

            if self.collision_status["CONTACT_LEFT"] > 0:
                self.collision_status["CONTACT_LEFT"] = 0
            return True

        t.pre_solve = pre_solve

        t = scene_space.add_collision_handler(PlayerRightSI.collision_type,
                                              TerrainSI.collision_type)

        def pre_solve(_arbiter: pymunk.Arbiter,
                      _space: pymunk.Space,
                      _data: dict) -> bool:

            if self.collision_status["CONTACT_RIGHT"] > 0:
                self.collision_status["CONTACT_RIGHT"] = 0
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

    @classmethod
    def _init_class_variables(cls) -> None:
        if cls.MASS is not None:
            return

        cls.MASS = Resource.data["objects"]["player"]["PHYSICS"]["MASS"]

        cls.FLOORED_WALK_FORCE = Resource.data["objects"]["player"]["MOVEMENTS"]["FLOORED_WALK_FORCE"]
        cls.FLOORED_WALK_MAX_SPEED = Resource.data["objects"]["player"]["MOVEMENTS"]["FLOORED_WALK_MAX_SPEED"]
        cls.FLOORED_SPEED_DAMPING = Resource.data["objects"]["player"]["MOVEMENTS"]["FLOORED_SPEED_DAMPING"]

        cls.AIRTIME_WALK_FORCE = Resource.data["objects"]["player"]["MOVEMENTS"]["AIRTIME_WALK_FORCE"]
        cls.AIRTIME_WALK_MAX_SPEED = Resource.data["objects"]["player"]["MOVEMENTS"]["AIRTIME_WALK_MAX_SPEED"]
        cls.AIRTIME_SPEED_DAMPING = Resource.data["objects"]["player"]["MOVEMENTS"]["AIRTIME_SPEED_DAMPING"]

        cls.JUMP_BASE_FORCE = Resource.data["objects"]["player"]["MOVEMENTS"]["JUMP_BASE_FORCE"]
        cls.JUMP_FORCE_DAMPING = Resource.data["objects"]["player"]["MOVEMENTS"]["JUMP_FORCE_DAMPING"]

        cls.CLIMB_JUMP_ANGLE = Resource.data["objects"]["player"]["MOVEMENTS"]["CLIMB_JUMP_ANGLE"]

        cls.SHOTGUN_KNOCKBACK = Resource.data["objects"]["player"]["UTILS"]["SHOTGUN_KNOCKBACK"]
