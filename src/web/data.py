"""
Returns a data the player may need to show to the user.
For example, a list of flags.
Has no visual front end.
"""


from data.flag import get_flags
from flask import Blueprint

from main import version_formatted, git_info


bp = Blueprint("data", __name__)


@bp.route("/data/version")
def data_version():
    git_sha = git_info.get("commit", "")
    
    data = {
        "version": version_formatted,
        "git_branch": git_info.get("refs", ""),
        "git_sha": git_sha
    }
    
    if len(git_sha) >= 7:
        data["git_sha_short"] = git_sha[0:7]
    else:
        data["git_sha_short"] = git_sha
    
    data["full"] = data.get("version")
    
    addon = "+"
    if data.get("git_branch", None) and data["git_branch"] != "main":
        data["full"] += addon + data.get("git_branch")
        addon = "."
    if data.get("git_sha_short", None):
        data["full"] += addon + data.get("git_sha_short")
    
    return data


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