"""
Includes various datatypes used in functions.
Aswell as some helpful functions for getting data.
"""


from io import BytesIO
from zipfile import ZipFile
import os
import json


ASSET_PACK_ICON = "assets/images/pack.png"

FLAGS_DIRECTORY = "assets/flags"
DEFAULT_FLAG_ID = "traditional"
CACHE_FLAG_DATA = True


cached_flag_data = {}


class FlagData():
    def __init__(self, id: str):
        self.id = id
        
        self.name = self.id
        self.colors = []
        
        self.vertical_icon = True
    
    def load_json_data(self, json_data: dict):
        # get basic flag metadata
        self.name = json_data.get("name", self.id)
        self.vertical_icon = json_data.get("vertical_icon", True)
        
        # get flag colors
        self.colors = json_data.get("colors", [])
        if len(self.colors) == 0:
            # for the objectively wrong people (this is a joke)
            self.colors = json_data.get("colours", [])


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
                
                texture_path = os.path.join("assets", "minecraft", texture.path)
                
                zip_file.writestr(texture_path, texture_bytes.getvalue())
        
        # add pack icon
        zip_file.write(ASSET_PACK_ICON, "pack.png")
        
        # add pack metadata
        pack_format = 22
        pack_description = "funny pride pack"
        
        metadata = {
            "pack": {
                "pack_format": pack_format,
                "description": pack_description
            }
        }
        
        metadata_string = json.dumps(metadata)
        metadata_bytes = BytesIO(bytes(metadata_string, "ascii"))
        
        zip_file.writestr("pack.mcmeta", metadata_bytes.getvalue())
        
        return zip_bytes


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