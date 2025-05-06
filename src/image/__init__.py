"""
Contains functions components use to generate their retrospective textures.
"""


from typing import Union
from data.flag import FlagData
from PIL import Image, ImageColor, ImageOps, ImageDraw


BLACK_THRESHOLD = 64
GRADIENT_STEPS = 8

ASSET_PACK_ICON = "assets/images/pack.png"


def move_toward(start, end, percent):
    # percent is 0.0 (at the start) or 1.0 (at the end)
    return start + ((end - start) * percent)


def generate_flag_on_image(flag: FlagData, image: Union[Image.Image, str],
                           size: tuple = None, position: tuple = None,
                           overlay: Union[Image.Image, str] = None, vertical = False,
                           gradient: bool = False, multi: int = 1, flag_overlay = False
                           ) -> Image.Image:
    # be sure a valid flag is given
    if flag == None:
        return None

    # be sure the flag actually has color
    if len(flag.colors) == 0:
        return None

    # get the colors to use
    colors_to_use = flag.colors
    if not flag_overlay and len(flag.colors_no_overlays) > 0:
        colors_to_use = flag.colors_no_overlays

    # load images if they are provided as file paths
    if type(image) is str:
        image = Image.open(image)
    if type(overlay) is str:
        overlay = Image.open(overlay)

    # set the active image to be the input image
    active_image = image

    # get the flags colors and convert them to a color tuple
    color_array = []
    for color_input in colors_to_use:
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

        color_array.append(color)

    # multiply the amount of colors (aka the amount of times the flag shows) on the texture
    if multi > 1:
        new_color_array = color_array * multi
        color_array = new_color_array

    # create a gradient out of the color array if asked for
    if gradient:
        i = 0
        gradient_color_array = []
        for color in color_array:
            i += 1

            # add the initial starting color
            gradient_color_array.append(color)

            next_color_index = i
            if next_color_index >= len(color_array):
                # end at the final color
                break

            next_color = color_array[next_color_index]
            if next_color == color:
                for e in range(GRADIENT_STEPS - 2):
                    gradient_color_array.append(color)

                continue

            # move towards the next colors value by X gradient steps
            for e in range(GRADIENT_STEPS - 1):
                percent = (e + 1) / GRADIENT_STEPS
                new_color = (
                    move_toward(color[0], next_color[0], percent),
                    move_toward(color[1], next_color[1], percent),
                    move_toward(color[2], next_color[2], percent)
                )

                gradient_color_array.append(new_color)

        # replace the color array with the gradiented version
        color_array = gradient_color_array

    # generate a recolored version of the input image per color
    color_images = []
    for color in color_array:
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

    flag_segment_size = flag_segment_size / len(color_array)

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

    # apply the flag specific overlay
    if flag_overlay:
        # TODO: make the position of each overlay actually do something
        for flag_overlay_image in flag.overlays:
            if flag_overlay_image == None:
                continue

            # make sure the position and overlay of the flag overlay can fit in the sprite
            pre_overlay_image = Image.new("RGBA", flag_overlay_image.size)
            pre_overlay_image.paste(flag_overlay_image)
            if not vertical:
                # rotate and flip the overlay if the flag is to be displayed rotated
                pre_overlay_image = pre_overlay_image.rotate(-90)
                pre_overlay_image = pre_overlay_image.transpose(Image.FLIP_LEFT_RIGHT)

            # get the mask for the flag overlay to use
            mask_for_overlay_image = None
            if image.mode != "P":
                mask_for_overlay_image = image

            # apply the mask onto the flag overlay
            final_overlay_image = Image.new("RGBA", image.size)
            final_overlay_image.paste(
                pre_overlay_image.resize(image.size, Image.Resampling.NEAREST),
                None, mask_for_overlay_image
            )

            active_image.alpha_composite(final_overlay_image)

    if overlay:
        active_image.alpha_composite(overlay)

    return active_image


def generate_pack_png(flag: FlagData = None):
    icon_overlay = Image.open(ASSET_PACK_ICON)
    icon_underlay = Image.new("RGBA", icon_overlay.size, "#FFF")

    final_icon = generate_flag_on_image(
        flag, icon_underlay,
        size=(105, 105), position=(12, 12),
        overlay=icon_overlay, vertical=flag.vertical_icon,
        flag_overlay=True
    )

    return final_icon