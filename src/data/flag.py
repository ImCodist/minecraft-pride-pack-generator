"""
Data structure for flags aswell as helper functions for retrieving that data.
"""

import os
import json

from PIL import Image


FLAGS_DIRECTORY = "assets/flags"

DEFAULT_FLAG_ID = "rf-traditional"
DEFAULT_FLAG_ICON_VERTICAL = True

CACHE_FLAG_DATA = True


cached_flag_data = {}


class FlagData():
    def __init__(self, id: str):
        self.id = id

        self.name = self.id

        self.colors = []
        self.colors_no_overlays = []

        self.overlays = [None, None, None] # left, middle, right

        self.vertical_icon = DEFAULT_FLAG_ICON_VERTICAL

    def load_json_data(self, json_data: dict):
        # get basic flag metadata
        self.name = json_data.get("name", self.id)
        self.vertical_icon = json_data.get("vertical_icon", DEFAULT_FLAG_ICON_VERTICAL)

        # get flag colors
        self.colors = json_data.get("colors", [])
        self.colors_no_overlays = json_data.get("colors_no_overlays", [])
        if len(self.colors) == 0:
            # for the objectively wrong people (this is a joke)
            self.colors = json_data.get("colours", [])

    def load_overlays(self, flag_folder: str):
        file_ext = ".png"
        overlay_path = os.path.join(flag_folder, "overlay")

        side_ext = ["_left", "", "_right"]
        for i in range(3):
            path = overlay_path + side_ext[i] + file_ext
            if os.path.exists(path):
                self.overlays[i] = Image.open(path)


def get_flags() -> dict[str, FlagData]:
    # TODO: i've heard globals suck but im not educated enough to know why, itd be nice to fix this use one day
    global cached_flag_data

    if CACHE_FLAG_DATA and cached_flag_data:
        return cached_flag_data

    # get all flags in the flag directory alongside their data
    flag_data = {}
    for flag_id in os.listdir(FLAGS_DIRECTORY):
        root = os.path.join(FLAGS_DIRECTORY, flag_id)

        # create the flags data
        new_flag_data = FlagData(flag_id)

        # load the json file for the flag
        json_path = os.path.join(root, "flag.json")
        if os.path.exists(json_path):
            json_file = open(json_path, "r")

            json_data: dict = json.load(json_file)
            new_flag_data.load_json_data(json_data)

        # load each overlay for the flag
        new_flag_data.load_overlays(root)

        flag_data[new_flag_data.id] = new_flag_data

    if CACHE_FLAG_DATA:
        cached_flag_data = flag_data

    return flag_data

def get_flag(id: str) -> FlagData:
    flags = get_flags()

    flag = flags.get(id, None)
    if not flag:
        flag = flags.get(DEFAULT_FLAG_ID, None)

    return flag