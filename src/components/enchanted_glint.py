from components import ComponentBase, Texture
from data.flag import get_flag
from image import generate_flag_on_image
from os import path


ASSET_ENCHANTED_GLINT_ITEM = "assets/images/components/enchanted_glint/enchanted_glint_item.png"
ASSET_ENCHANTED_GLINT_ENTITY = "assets/images/components/enchanted_glint/enchanted_glint_entity.png"


class ComponentEnchantedGlint(ComponentBase):
    def generate_textures(self):
        textures = []
        base_path = path.join("textures", "misc")
        
        flag = get_flag(self.options.get("flag", ""))
        
        # item
        textures.append(Texture(
            path.join(base_path, "enchanted_glint_item.png"),
            generate_flag_on_image(flag, ASSET_ENCHANTED_GLINT_ITEM)
        ))
        
        # entity
        textures.append(Texture(
            path.join(base_path, "enchanted_glint_entity.png"),
            generate_flag_on_image(flag, ASSET_ENCHANTED_GLINT_ENTITY)
        ))
        
        return textures