from components import ComponentBase, Texture
from data.flag import get_flag
from image import generate_flag_on_image
from os import path


ASSET_HEARTS_DIR = "assets/images/components/heart/"


class ComponentHearts(ComponentBase):
    def generate_textures(self):
        textures = []
        base_path = path.join("textures", "gui", "sprites", "hud", "heart")

        flag = get_flag(self.options.get("flag", ""))

        use_vertical = self.options.get("horizontal", "") != "true"

        heart_names = [
            "full", "half",
            "hardcore_full", "hardcore_half"
        ]

        for heart_name in heart_names:
            file_name = heart_name + ".png"

            texture = Texture(
                path.join(base_path, file_name),
                generate_flag_on_image(
                    flag,
                    path.join(ASSET_HEARTS_DIR, file_name),

                    size=(7, 7), position=(1.5, 1),
                    overlay=path.join(ASSET_HEARTS_DIR, "shine_overlay.png"),

                    vertical=use_vertical,
                    flag_overlay=True
                )
            )

            textures.append(texture)

        return textures
