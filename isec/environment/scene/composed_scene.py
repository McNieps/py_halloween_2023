from isec.environment.base.scene import Scene
from isec.environment.base.camera import Camera
from isec.environment.scene import EntityScene, TilemapScene
from isec.environment.base import Entity, Tilemap


class ComposedScene(Scene):
    def __init__(self,
                 fps: int) -> None:
        """
        A scene that contains multiple tilemap scenes and an entity scene.
        The tilemap scenes are rendered first, then the entity scene is rendered on top.
        If a tilemap scene have a parallax depth > 1, it will be rendered on top of the entity scene.

        :param fps: The fps of the scene.
        """

        super().__init__()
        self.entity_scene: EntityScene = EntityScene(fps, surface=self.surface, camera=self.camera)
        self.tilemap_scenes: list[TilemapScene] = []

    def add_entities(self,
                     *entities: Entity) -> None:
        """
        Add entities to the level scene.

        :param entities: The entities to add.
        """

        self.entity_scene.add_entities(*entities)

    def add_tilemap_scene(self,
                          tilemap: Tilemap) -> None:
        """
        Add a tilemap scene to the level scene.

        :param tilemap: The tilemap scene to add.
        """

        new_tilemap_scene = TilemapScene(tilemap, surface=self.surface, camera=self.camera)
        self.tilemap_scenes.append(new_tilemap_scene)

        self.tilemap_scenes.sort(key=lambda tilemap_scene: tilemap_scene.tilemap.parallax_depth)

    def update(self,
               delta: float) -> None:
        """
        Update all the entities and the tilemap scenes.

        :param delta: The time since the last update.
        """

        self.entity_scene.update(delta)
        for tilemap_scene in self.tilemap_scenes:
            tilemap_scene.update(delta)

    def render(self,
               camera: Camera = None) -> None:
        """
        Render the background tilemap scenes, then the entity scene, then the foreground tilemap scenes.

        :param camera: The camera to render the scene with. If None, the scene's camera will be used.
        """

        if camera is None:
            camera = self.camera

        for tilemap_scene in self.tilemap_scenes:
            if tilemap_scene.tilemap.parallax_depth > 1:
                break
            tilemap_scene.render(camera=camera)

        self.entity_scene.render(camera=camera)

        for tilemap_scene in self.tilemap_scenes:
            if tilemap_scene.tilemap.parallax_depth > 1:
                tilemap_scene.render(camera=camera)

    @property
    def space(self):
        return self.entity_scene.space
