"""
Contains functions components use to generate their retrospective textures.
"""


from typing import Union
from data.flag import FlagData
from PIL import Image, ImageColor, ImageOps, ImageDraw


BLACK_THRESHOLD = 64


def generate_flag_on_image(flag: FlagData, image: Union[Image.Image, str], 
                           size: tuple = None, position: tuple = None, 
                           overlay: Union[Image.Image, str] = None, vertical = False
                           ) -> Image.Image:
    # be sure a valid flag is given
    if flag == None:
        return None
    
    # load images if they are provided as file paths
    if type(image) is str:
        image = Image.open(image)
    if type(overlay) is str:
        overlay = Image.open(overlay)
    
    # set the active image to be the input image
    active_image = image
    
    # generate a recolored version of the input image per color
    color_images = []
    for color_input in flag.colors:
        # parse color input
        if type(color_input) is str and not color_input.startswith("#"):
            color_input = "#" + color_input
        
        color = ImageColor.getrgb(color_input)
        
        # if the color is too black make it not too black
        # TODO: look into if theres a better way of doing this
        if color[0] < BLACK_THRESHOLD and color[1] < BLACK_THRESHOLD and color[2] < BLACK_THRESHOLD:
            color = (
                color[0] + BLACK_THRESHOLD,
                color[1] + BLACK_THRESHOLD,
                color[2] + BLACK_THRESHOLD
            )
        
        # recolor the image
        # split the image into its seperate layers to get the alpha layer (if it exists)
        image_layers = active_image.split()
        
        # grayscale the image and color it
        image_grayscaled = ImageOps.grayscale(active_image)
        image_colored = ImageOps.colorize(image_grayscaled, "#000", color)
        
        # add the alpha layer back if it exists
        if len(image_layers) >= 4:
            image_colored.putalpha(image_layers[3])
        
        color_images.append(image_colored)
    
    # decide the area where the flag will be placed
    flag_size = active_image.size
    flag_position = (0, 0)
    if type(size) is tuple:
        flag_size = size
    if type(position) is tuple:
        flag_position = position
    
    # place each color image part in segments to form the flag
    final_image = Image.new("RGBA", active_image.size)
    
    flag_segment_size = flag_size[0]
    if vertical:
        flag_segment_size = flag_size[1]
    
    flag_segment_size = flag_segment_size / len(flag.colors)
    
    i = 0
    for color_image in color_images:
        # get the positions and sizes of everything
        cur_segment_offset = flag_segment_size * i
        
        cur_segment_position = (flag_position[0], flag_position[1])
        cur_segment_size = (flag_size[0], flag_size[1])
        if not vertical:
            cur_segment_position = (cur_segment_position[0] + cur_segment_offset, cur_segment_position[1])
            cur_segment_size = (cur_segment_position[0] + flag_segment_size, cur_segment_position[1] + cur_segment_size[1])
        else:
            cur_segment_position = (cur_segment_position[0], cur_segment_position[1] + cur_segment_offset)
            cur_segment_size = (cur_segment_position[0] + cur_segment_size[0], cur_segment_position[1] + flag_segment_size)
        
        # create a mask
        mask_image = Image.new("1", final_image.size)
        mask_image_draw = ImageDraw.Draw(mask_image)
        mask_image_draw.rectangle((cur_segment_position[0], cur_segment_position[1], cur_segment_size[0], cur_segment_size[1]), True)
        
        # reconstruct the image with the flag segments
        final_image.paste(color_image, (0, 0), mask_image)
        
        i += 1
    
    active_image = final_image
    
    if overlay:
        active_image.alpha_composite(overlay)
    
    return active_image