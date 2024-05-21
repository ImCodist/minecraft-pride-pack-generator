"""
Returns assets for different things that arent in static.
Has no visual front end.
"""


from data import get_flags
from flask import Blueprint, request, send_file
from PIL import Image
from generation import generate_flag_on_image
from io import BytesIO


ASSET_FLAG_BASE = "assets/images/site/flag_base.png"
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
def data_flags():
    flag_id = request.args.get("flag", "")

    flags = get_flags()
    if flag_id in flags.keys():
        # get the flags unique icon
        flag_icon = get_flag_icon(flag_id)
        
        # save the icon to bytes
        flag_bytes = BytesIO()
        flag_icon.save(flag_bytes, format="PNG")
        flag_bytes.seek(0)
        
        return send_file(flag_bytes, mimetype="image/png")
    
    return flag_id