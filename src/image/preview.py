"""
Contains functions to generate previews of components.
"""


from PIL import Image

from components import ComponentBase
from components.experience_bar import ComponentExperienceBar
from components.hearts import ComponentHearts
from components.enchanted_glint import ComponentEnchantedGlint


ASSET_HEART_CONTAINER = "assets/images/previews/heart_container.png"

ASSET_GLINT_ITEM = "assets/images/previews/glint_item.png"
ASSET_GLINT_ITEM_MASK = "assets/images/previews/glint_item_mask.png"


PREVIEW_UPSCALE_SIZE = 5


def generate_preview_component(component: ComponentBase):
    if component.__class__ == ComponentExperienceBar().__class__:
        return generate_preview_xp_bar(component)
    elif component.__class__ == ComponentHearts().__class__:
        return generate_preview_hearts(component)
    elif component.__class__ == ComponentEnchantedGlint().__class__:
        return generate_preview_e_glint(component)

    return generate_preview_generic(component)


def generate_preview_generic(component: ComponentBase):
    component.generate()
    preview_image = component.textures[0].image
    return preview_image


def generate_preview_xp_bar(component: ComponentExperienceBar):
    component.generate()
    
    preview_image_front = component.textures[0].image
    
    preview_image_back = None
    if len(component.textures) > 1:
        preview_image_back = component.textures[1].image
    
    preview_image = Image.new(preview_image_front.mode, (preview_image_front.size[0], (preview_image_front.size[1] * 2) + 2))
    
    front_pos_y = 0
    if not preview_image_back:
        front_pos_y = 4
    
    preview_image.alpha_composite(preview_image_front, (0, front_pos_y))
    if preview_image_back:
        preview_image.alpha_composite(preview_image_back, (0, preview_image_front.size[1] + 2))
    
    preview_image = preview_image.resize(
        (preview_image.size[0] * PREVIEW_UPSCALE_SIZE, 
         preview_image.size[1] * PREVIEW_UPSCALE_SIZE),
        Image.Resampling.NEAREST
    )
    
    return preview_image

def generate_preview_hearts(component: ComponentHearts):
    component.generate()
    
    preview_image = Image.new("RGBA", (120, 9))
    
    heart_container = Image.open(ASSET_HEART_CONTAINER)
    heart_image = component.textures[0].image
    
    hearts = 10
    for heart_i in range(hearts):
        heart_pos = (19 + (8 * heart_i), 0)
        preview_image.alpha_composite(heart_container, heart_pos)
        preview_image.alpha_composite(heart_image, heart_pos)
    
    preview_image = preview_image.resize(
        (preview_image.size[0] * PREVIEW_UPSCALE_SIZE, 
         preview_image.size[1] * PREVIEW_UPSCALE_SIZE),
        Image.Resampling.NEAREST
    )
    
    return preview_image

def generate_preview_e_glint(component: ComponentEnchantedGlint):
    component.generate()
    
    glint_item = Image.open(ASSET_GLINT_ITEM)
    
    glint_item_mask = Image.open(ASSET_GLINT_ITEM_MASK)
    glint_item_mask = glint_item_mask.convert("1")

    glint_overlay = component.textures[0].image
    glint_overlay = glint_overlay.crop((0, 0, glint_item.size[0], glint_item.size[1]))
    glint_overlay.putalpha(125)

    preview_image = Image.new("RGBA", glint_item.size)
    preview_image.paste(glint_item)
    
    masked_overlay = Image.new("RGBA", glint_item.size)
    masked_overlay.paste(glint_overlay, None, glint_item_mask)
    
    preview_image.alpha_composite(masked_overlay)
    
    preview_image = preview_image.resize(
        (preview_image.size[0] * PREVIEW_UPSCALE_SIZE, 
         preview_image.size[1] * PREVIEW_UPSCALE_SIZE),
        Image.Resampling.NEAREST
    )
    
    return preview_image