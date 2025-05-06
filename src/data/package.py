"""
Data structure for packages / resource packs.
Aswell as the code needed to package them into a final pack.
"""


from io import BytesIO
from zipfile import ZipFile
from os import path
from data.flag import get_flag
from image import generate_pack_png
import json


PACK_FILE_NAME = "Pride Textures.zip"
PACK_DESCRIPTION = "Makes a variety of Minecraft's textures into pride flags."

PACK_MINIMUM_FORMAT = 18
PACK_MAXIMUM_FORMAT = 55


class PackageData():
    def __init__(self, components: list):
        self.components = components

    def package(self):
        # create the new zip in memory
        zip_bytes = BytesIO()
        zip_file = ZipFile(zip_bytes, "w")

        # generate each components textures and save them into the zip
        for component in self.components:
            component.generate()

            # save each texture into the zip
            for texture in component.textures:
                if not texture.image:
                    continue

                texture_bytes = BytesIO()
                texture.image.save(texture_bytes, format="PNG")
                texture_bytes.seek(0)

                texture_path = path.join("assets", "minecraft", texture.path)

                zip_file.writestr(texture_path, texture_bytes.getvalue())

        # generate pack icon
        component_flags = []

        # get the flag that occurs the most to use for the pack icon
        icon_flag_to_use = None
        for component in self.components:
            component_flag = component.options.get("flag", None)
            if component_flag:
                component_flags.append(component_flag)

        if len(component_flags) > 0:
            icon_flag_to_use = max(set(component_flags), key=component_flags.count)

        # generate and add the pack icon to the zip
        icon_flag = get_flag(icon_flag_to_use)

        final_icon = generate_pack_png(icon_flag)

        icon_bytes = BytesIO()
        final_icon.save(icon_bytes, format="PNG")
        icon_bytes.seek(0)

        zip_file.writestr("pack.png", icon_bytes.getvalue())

        # add pack metadata
        metadata = {
            "pack": {
                "pack_format": PACK_MINIMUM_FORMAT,
                "supported_formats": [PACK_MINIMUM_FORMAT, PACK_MAXIMUM_FORMAT],
                "description": PACK_DESCRIPTION
            }
        }

        metadata_string = json.dumps(metadata)
        metadata_bytes = BytesIO(bytes(metadata_string, "ascii"))

        zip_file.writestr("pack.mcmeta", metadata_bytes.getvalue())

        return zip_bytes


