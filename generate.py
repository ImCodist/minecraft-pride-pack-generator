import flags
import package
from PIL import Image, ImageOps, ImageColor, ImageDraw
import math


ASSET_XP_BAR_PROGRESS = "assets/images/modules/experience_bar/experience_bar_progress.png"
ASSET_XP_BAR_PROGRESS_BACKGROUND = "assets/images/modules/experience_bar/experience_bar_background.png"

ASSET_HEART_FULL = "assets/images/modules/heart/full.png"
ASSET_HEART_HALF = "assets/images/modules/heart/half.png"
ASSET_HEART_HARDCORE_FULL = "assets/images/modules/heart/hardcore_full.png"
ASSET_HEART_HARDCORE_HALF = "assets/images/modules/heart/hardcore_half.png"

ASSET_HEART_SHINE_OVERLAY = "assets/images/modules/heart/shine_overlay.png"

ASSET_ENCHANTED_GLINT_ITEM = "assets/images/modules/enchanted_glint/enchanted_glint_item.png"
ASSET_ENCHANTED_GLINT_ENTITY = "assets/images/modules/enchanted_glint/enchanted_glint_entity.png"

ASSET_FLAG_BASE = "assets/images/flag_base.png"

COLOR_BLACK = ImageColor.getrgb("#000000")
COLOR_WHITE = ImageColor.getrgb("#FFFFFF")

BLACK_THRESHOLD = 64


def generate_flag_on_texture(flag: flags.FlagData, texture: str, size = None, position = None, overlay: str = None) -> Image.Image:
    main_image = Image.open(texture)
    color_images = []
    
    if size == None:
        size = main_image.size
    if position == None:
        position = (0, 0)
    
    for color in flag.colors:
        color_hex = color
        
        # make sure theres a # at the beginning cuz thats important i guess?
        if not color_hex.startswith("#"):
            color_hex = "#" + color_hex
        
        color_hex_final = ImageColor.getrgb(color_hex)
        
        # make sure the black colors arent too dark as that causes problems
        if color_hex_final[0] < BLACK_THRESHOLD and color_hex_final[1] < BLACK_THRESHOLD and color_hex_final[2] < BLACK_THRESHOLD:
            color_hex_final = (
                color_hex_final[0] + BLACK_THRESHOLD,
                color_hex_final[1] + BLACK_THRESHOLD,
                color_hex_final[2] + BLACK_THRESHOLD
            )
        
        # color the image
        image_layers = main_image.split()
        
        image_grayscale = ImageOps.grayscale(main_image)
        image_colored = ImageOps.colorize(image_grayscale, COLOR_BLACK, color_hex_final)
        
        if len(image_layers) >= 3:
            image_colored.putalpha(image_layers[3])
        
        # add to the list
        color_images.append(image_colored)
    
    final_image = Image.new("RGBA", main_image.size)
    
    color_image_width = size[0] / len(flag.colors)
    
    i = 0
    for color_image in color_images:
        # create the mask
        mask_image = Image.new("1", final_image.size)
        
        mask_image_x = round(color_image_width * i)
        
        mask_image_draw = ImageDraw.Draw(mask_image)
        mask_image_draw.rectangle([mask_image_x + position[0], position[1], mask_image_x + color_image_width + position[0], mask_image.height + position[1]], True)
        
        # put the colored image on the final image using the mask
        final_image.paste(color_image, (0, 0), mask_image)

        i += 1
    
    if overlay:
        overlay_image = Image.open(overlay)
        final_image.alpha_composite(overlay_image)
    
    return final_image


def generate_xp_bar(flag: flags.FlagData) -> Image.Image:
    return generate_flag_on_texture(flag, ASSET_XP_BAR_PROGRESS)

def generate_xp_bar_background(flag: flags.FlagData) -> Image.Image:
    return generate_flag_on_texture(flag, ASSET_XP_BAR_PROGRESS_BACKGROUND)


def generate_hearts(flag: flags.FlagData) -> dict:
    hearts = {}
    
    heart_size = (7, 7)
    heart_pos = (1, 1)
    heart_overlay = ASSET_HEART_SHINE_OVERLAY
    
    hearts["full"] = generate_flag_on_texture(flag, ASSET_HEART_FULL, heart_size, heart_pos, heart_overlay)
    hearts["half"] = generate_flag_on_texture(flag, ASSET_HEART_HALF, heart_size, heart_pos, heart_overlay)
    
    hearts["hardcore_full"] = generate_flag_on_texture(flag, ASSET_HEART_HARDCORE_FULL, heart_size, heart_pos)
    hearts["hardcore_half"] = generate_flag_on_texture(flag, ASSET_HEART_HARDCORE_HALF, heart_size, heart_pos)
    
    return hearts


def generate_enchanted_glint(flag: flags.FlagData):
    return [
        generate_flag_on_texture(flag, ASSET_ENCHANTED_GLINT_ITEM),
        generate_flag_on_texture(flag, ASSET_ENCHANTED_GLINT_ENTITY)
    ]


def generate_flag_preview(flag: flags.FlagData):
    return generate_flag_on_texture(flag, ASSET_FLAG_BASE)


def generate_package(
    xp_bar_flag: flags.FlagData = None,
    xp_bar_bg_flag: flags.FlagData = None,
    hearts_flag: flags.FlagData = None,
    enchanted_glint_flag: flags.FlagData = None
):
    package_data = package.PackageData()
    
    if xp_bar_flag:
        package_data.xp_bar = generate_xp_bar(xp_bar_flag)
    if xp_bar_bg_flag:
        package_data.xp_bar_bg = generate_xp_bar_background(xp_bar_bg_flag)
    
    if hearts_flag:
        package_data.hearts = generate_hearts(hearts_flag)
    
    if enchanted_glint_flag:
        glints = generate_enchanted_glint(enchanted_glint_flag)
        package_data.enchanted_glint = glints[0]
        package_data.enchanted_glint_entity = glints[1]
    
    return package_data