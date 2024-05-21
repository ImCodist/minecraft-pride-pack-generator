from components import ComponentBase, Texture
from data import get_flag
from generation import generate_flag_on_image
from os import path


ASSET_EXPERIENCE_BAR_PROGRESS = "assets/images/components/experience_bar/experience_bar_progress.png"
ASSET_EXPERIENCE_BAR_BACKGROUND = "assets/images/components/experience_bar/experience_bar_background.png"


class ComponentExperienceBar(ComponentBase):
    def generate_textures(self):
        textures = []
        base_path = path.join("textures", "gui", "sprites", "hud")
        
        # get the main flag to use when drawing
        main_flag = get_flag(self.options.get("flag", ""))
        
        # generate the progress image
        progress_image = generate_flag_on_image(main_flag, ASSET_EXPERIENCE_BAR_PROGRESS)
        textures.append(
            Texture(path.join(base_path, "experience_bar_progress.png"), progress_image)
        )
        
        # generate the bg image if requested
        if self.options.get("change_bg", "") == "true":
            background_flag = None
            
            # get the unique background flag if requested
            if self.options.get("unique_bg", "") == "true":
                background_flag = get_flag(self.options.get("bg_flag", ""))
            
            if not background_flag:
                background_flag = main_flag
            
            background_image = generate_flag_on_image(background_flag, ASSET_EXPERIENCE_BAR_BACKGROUND)
            textures.append(
                Texture(path.join(base_path, "experience_bar_background.png"), background_image)
            )
        
        return textures