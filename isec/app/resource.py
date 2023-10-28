import pygame
import json
import csv
import os

from isec._ise_typing import PathLike
from isec._ise_error import InvalidFileFormatError
from isec.objects import CachedSurface


class Resource:
    default_assets_directory: PathLike = None
    project_assets_directory: PathLike = None

    data: dict[str: dict[str: any]] = {}
    image: dict[str: dict[str: any]] = {}
    sound: dict[str: dict[str: any]] = {}

    @classmethod
    def set_directory(cls,
                      assets_dir: PathLike) -> None:

        cls.project_assets_directory = assets_dir

    @classmethod
    def pre_init(cls,
                 default_safeguard: bool = True,
                 default_only: bool = False) -> None:

        if default_safeguard or default_only:
            cls._get_default_assets_directory()
            cls._load_data(cls.default_assets_directory)

        if not default_only:
            cls._load_data(cls.project_assets_directory)

    @classmethod
    def init(cls,
             default_safeguard: bool = True,
             default_only: bool = False) -> None:

        if default_safeguard or default_only:
            cls._get_default_assets_directory()
            cls._load_image(cls.default_assets_directory)
            cls._load_sound(cls.default_assets_directory)

        if not default_only:
            cls._load_image(cls.project_assets_directory)
            cls._load_sound(cls.project_assets_directory)

        cls._cache()
        cls.set_volume()

    @classmethod
    def _get_default_assets_directory(cls):
        if cls.default_assets_directory is not None:
            return

        list_path = str(__file__).split("\\") if "\\" in __file__ else str(__file__).split("/")

        cls.default_assets_directory = "/".join(list_path[:list_path.index("isec") + 1]) + "/assets/"

    @classmethod
    def _load_data(cls,
                   assets_path: PathLike,
                   current_dict: dict = None) -> None:

        if current_dict is None:
            current_dict = cls.data
            assets_path += "data/"

        for elem in os.scandir(assets_path):
            if elem.is_dir():
                if elem.name not in current_dict:
                    current_dict[elem.name] = {}

                cls._load_data(assets_path+elem.name+"/", current_dict[elem.name])

            if elem.is_file():
                key_name = "".join(elem.name.split(".")[:-1])

                if elem.name.endswith(".json"):
                    if key_name not in current_dict:
                        current_dict[key_name] = {}

                    current_dict[key_name] |= cls._load_json(assets_path+elem.name)

                elif elem.name.endswith(".csv"):
                    current_dict[key_name] = cls._load_csv(assets_path+elem.name)

                else:
                    raise InvalidFileFormatError(f"{elem.name.split('.')[-1]} is not a supported data file format")

    @classmethod
    def _load_json(cls,
                   file_path: PathLike) -> dict[str, ...]:

        with open(file_path) as file:
            return json.load(file)

    @classmethod
    def _load_csv(cls,
                  file_path: PathLike) -> list[list[int]]:

        with open(file_path) as file:
            return [list(map(int, rec)) for rec in csv.reader(file, delimiter=',')]

    @classmethod
    def _load_image(cls,
                    assets_path: PathLike,
                    current_image_dict: dict = None,
                    current_data_dict: dict = None) -> None:

        if current_image_dict is None:
            current_image_dict = cls.image
            assets_path += "image/"

        if current_data_dict is None:
            if "image" not in cls.data:
                cls.data["image"] = {}
            current_data_dict = cls.data["image"]

        for elem in os.scandir(assets_path):
            if elem.is_dir():
                if elem.name not in current_image_dict:
                    current_image_dict[elem.name] = {}

                if elem.name not in current_data_dict:
                    current_data_dict[elem.name] = {}

                cls._load_image(assets_path + elem.name + "/",
                                current_image_dict[elem.name],
                                current_data_dict[elem.name])
                continue

            if elem.is_file():
                key_name = "".join(elem.name.split(".")[:-1])

                if elem.name == "index.json":
                    with open(assets_path + elem.name) as index_image:
                        image_dict = json.load(index_image)

                    current_data_dict |= image_dict

                elif any(elem.name.endswith(ext) for ext in [".png", ".jpg"]):
                    current_image_dict[key_name] = pygame.image.load(assets_path + elem.name).convert_alpha()

                else:
                    raise InvalidFileFormatError(f"{elem.name.split('.')[-1]} is not a supported image file format")

    @classmethod
    def _load_sound(cls,
                    assets_path: PathLike,
                    current_sound_dict: dict = None,
                    current_data_dict: dict = None) -> None:

        if current_sound_dict is None:
            current_sound_dict = cls.sound
            assets_path += "sound/"

        if current_data_dict is None:
            if "sound" not in cls.data:
                cls.data["sound"] = {}
            current_data_dict = cls.data["sound"]

        for elem in os.scandir(assets_path):
            if elem.is_dir():
                if elem.name not in current_sound_dict:
                    current_sound_dict[elem.name] = {}

                if elem.name not in current_data_dict:
                    current_data_dict[elem.name] = {}

                cls._load_sound(assets_path + elem.name + "/",
                                current_sound_dict[elem.name],
                                current_data_dict[elem.name])
                continue

            if elem.is_file():
                key_name = "".join(elem.name.split(".")[:-1])

                if any(elem.name.endswith(ext) for ext in [".wav", ".mp3", ".ogg"]):
                    current_sound_dict[key_name] = pygame.mixer.Sound(assets_path + elem.name)
                    continue

                if elem.name == "index.json":
                    with open(assets_path + elem.name) as index_sound:
                        sound_dict = json.load(index_sound)

                    current_data_dict |= sound_dict
                    continue

                raise InvalidFileFormatError(f"{elem.name.split('.')[-1]} is not a supported data file format")

    @classmethod
    def _cache(cls,
               surf_dict: dict = None,
               data_dict: dict = None) -> None:

        if not cls.data["engine"]["resource"]["surface"]["caching"]["enabled"]:
            return

        if "image" not in cls.data:
            return

        if surf_dict is None:
            surf_dict = cls.image
            data_dict = cls.data["image"]

        for image_key in data_dict:
            if image_key in surf_dict:
                if isinstance(surf_dict[image_key], dict):
                    cls._cache(surf_dict[image_key], data_dict[image_key])

                if "cached" in data_dict[image_key] and data_dict[image_key]["cached"] is True:
                    surf_dict[image_key] = cls._cache_image(surf_dict[image_key], data_dict[image_key])

    @classmethod
    def set_volume(cls,
                   master_volume: float = None,
                   sound_dict: dict = None,
                   data_dict: dict = None) -> None:

        if master_volume is None:
            master_volume = cls.data["engine"]["resource"]["sound"]["master_volume"]

        if sound_dict is None:
            sound_dict = cls.sound
            data_dict = cls.data["sound"]

        for key in sound_dict:
            if isinstance(sound_dict[key], dict):
                cls.set_volume(master_volume,
                               sound_dict[key],
                               data_dict[key])
                continue

            individual_sound_volume = data_dict[key] if key in data_dict else 1
            sound_dict[key].set_volume(master_volume*individual_sound_volume)

    @classmethod
    def _cache_image(cls,
                     surf: pygame.Surface,
                     surf_dict_param: dict[str, ...]) -> CachedSurface:

        if "cache_size" in surf_dict_param:
            cache_size = surf_dict_param["cache_size"]
        else:
            cache_size = cls.data["engine"]["resource"]["surface"]["caching"]["default_size"]

        return CachedSurface(surf, cache_size)
