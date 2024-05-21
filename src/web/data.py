"""
Returns a data the player may need to show to the user.
For example, a list of flags.
Has no visual front end.
"""


from data import get_flags
from flask import Blueprint


bp = Blueprint("data", __name__)


@bp.route("/data/flags")
def data_flags():
    parsed_flag_data = {}
    
    flags = get_flags()
    for flag_id in get_flags():
        flag_data = flags[flag_id]
        
        parsed_flag_data[flag_id] = {
            "name": flag_data.name,
        }
    
    return parsed_flag_data