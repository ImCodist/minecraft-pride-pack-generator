import zipfile
import os
import uuid
import shutil
import json
from PIL import Image


ASSET_PACK_PNG = "assets/images/pack.png"

DESCRIPTION = "awesome pride textures"

TEMP_DIRECTORY = ".temp"
OUTPUT_DIRECTORY = ".output"


class PackageData():
    def __init__(self):
        self.xp_bar: Image.Image = None
        self.xp_bar_bg: Image.Image = None
        
        self.hearts: dict = None
        
        self.enchanted_glint: Image.Image = None
        self.enchanted_glint_entity: Image.Image = None
    
    def package(self, pack_extra_description: str = None):
        pack_id = str(uuid.uuid4())
        
        # setup the folder structure
        pack_path = os.path.join(TEMP_DIRECTORY, pack_id)
        
        assets_path = os.path.join(pack_path, "assets", "minecraft")
        os.makedirs(assets_path)
        
        # add all assets
        
        # create the mcmeta
        meta_file_path = os.path.join(pack_path, "pack.mcmeta")
        
        meta_data = {
            "pack": {
                "pack_format": 22,
                "description": DESCRIPTION
            }
        }
        if pack_extra_description:
            meta_data["pack"]["description"] += " [" + pack_extra_description + "]"
        
        json_encoded = json.dumps(meta_data)
        
        meta_file = open(meta_file_path, "w")
        meta_file.write(json_encoded)
        meta_file.close()
        
        # create the pack png
        pack_png_path = os.path.join(pack_path, "pack.png")
        shutil.copyfile(ASSET_PACK_PNG, pack_png_path)
        
        # add the xp bar sprites
        if self.xp_bar or self.xp_bar_bg:
            xp_bar_root_path = os.path.join(assets_path, "textures", "gui", "sprites", "hud")
            os.makedirs(xp_bar_root_path)
            
            if self.xp_bar:
                xp_bar_path = os.path.join(xp_bar_root_path, "experience_bar_progress.png")
                self.xp_bar.save(xp_bar_path)
            if self.xp_bar_bg:
                xp_bar_bg_path = os.path.join(xp_bar_root_path, "experience_bar_background.png")
                self.xp_bar_bg.save(xp_bar_bg_path)
        
        # add the hearts sprites
        if self.hearts:
            hearts_root_path = os.path.join(assets_path, "textures", "gui", "sprites", "hud", "heart")
            os.makedirs(hearts_root_path)

            for heart in self.hearts:
                heart_image = self.hearts[heart]
                
                heart_path = os.path.join(hearts_root_path, heart + ".png")
                heart_image.save(heart_path)  
        
        # add the enchanted glint sprites
        if self.enchanted_glint:
            enchanted_glint_root_path = os.path.join(assets_path, "textures", "misc")
            os.makedirs(enchanted_glint_root_path)
            
            enchanted_glint_path = os.path.join(enchanted_glint_root_path, "enchanted_glint_item.png")
            self.enchanted_glint.save(enchanted_glint_path)  
            
            enchanted_glint_entity_path = os.path.join(enchanted_glint_root_path, "enchanted_glint_entity.png")
            self.enchanted_glint_entity.save(enchanted_glint_entity_path) 
        
        # setup the archive
        if not os.path.exists(OUTPUT_DIRECTORY):
            os.makedirs(OUTPUT_DIRECTORY)
        
        zip_path = os.path.join(OUTPUT_DIRECTORY, pack_id + ".zip")
        zip_file = zipfile.ZipFile(zip_path, "w")
        
        for root, dirs, files in os.walk(pack_path):
            true_root = os.path.relpath(root, pack_path)
            for file in files:
                zip_file.write(
                    os.path.join(root, file), 
                    os.path.join(true_root, file),
                )
        
        # remove the temp folder
        if os.path.exists(TEMP_DIRECTORY):
            shutil.rmtree(TEMP_DIRECTORY)
        
        return zip_path