"""
Data structure for packages / resource packs.
Aswell as the code needed to package them into a final pack.
"""


from io import BytesIO
from zipfile import ZipFile
from os import path
import json


ASSET_PACK_ICON = "assets/images/pack.png"


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


