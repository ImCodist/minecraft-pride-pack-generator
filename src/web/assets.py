"""
Returns assets for different things that arent in static.
Has no visual front end.
"""


from data.flag import get_flags, get_flag
from web.generate import parse_request_args, get_components_from_args_dict
from flask import Blueprint, request, send_file
from PIL import Image
from image import generate_flag_on_image, generate_pack_png
from image.preview import generate_preview_component
from io import BytesIO
from os import path


ASSET_FLAG_BASE = "assets/images/site/flag_base.png"
ASSET_FALLBACK_FLAG = "assets/images/site/flag_fallback.png"
CACHE_FLAG_ICONS = True


cached_flag_icons = {}



def get_flag_icons() -> list[Image.Image]:
    # TODO: globals suck yadayadayada refer to the data package's todo
    global cached_flag_icons
    
    if cached_flag_icons:
        return cached_flag_icons
    
    flag_icons = {}
    
    flag_icon_base = Image.open(ASSET_FLAG_BASE)

    flags = get_flags()
    for flag in flags:
        flag_data = flags[flag]
        
        flag_icon = generate_flag_on_image(
            flag_data, flag_icon_base, 
            size=(28, 18), position=(1, 6),
            vertical=flag_data.vertical_icon
        )
        flag_icons[flag] = flag_icon
    
    cached_flag_icons = flag_icons
    
    return flag_icons

def get_flag_icon(id: str) -> Image.Image:
    flag_icons = get_flag_icons()
    return flag_icons.get(id, None)



bp = Blueprint("assets", __name__)


@bp.route("/assets/flags")
def assets_flags():
    flag_id = request.args.get("flag", "")

    flags = get_flags()
    if flag_id in flags.keys():
        # get the flags unique icon
        flag_icon = get_flag_icon(flag_id)
        
        if flag_icon:
            # save the icon to bytes
            flag_bytes = BytesIO()
            flag_icon.save(flag_bytes, format="PNG")
            flag_bytes.seek(0)
            
            return send_file(flag_bytes, mimetype="image/png")
    
    return send_file(path.abspath(ASSET_FALLBACK_FLAG))

@bp.route("/assets/packpng")
def assets_packpng():
    flag_id = request.args.get("flag", "")
    
    flag = get_flag(flag_id)
    pack_png = generate_pack_png(flag)
    
    pack_png_bytes = BytesIO()
    pack_png.save(pack_png_bytes, format="PNG")
    pack_png_bytes.seek(0)
    
    return send_file(pack_png_bytes, mimetype="image/png")

@bp.route("/assets/preview")
def assets_preview():
    parsed_args = parse_request_args(request.args)
    components = get_components_from_args_dict(parsed_args)
    
    # only use the first component given, as there should only ever be a single given component
    component_to_preview = None
    if len(components) > 0:
        component_to_preview = components[0]
    
    if not component_to_preview:
        return "No component data given."
    
    component_preview = generate_preview_component(component_to_preview)
    if not component_preview:
        return "Component does not have a preview."
    
    component_preview_bytes = BytesIO()
    component_preview.save(component_preview_bytes, format="PNG")
    component_preview_bytes.seek(0)
    
    return send_file(component_preview_bytes, mimetype="image/png")